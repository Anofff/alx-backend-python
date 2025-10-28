#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos"""
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "gpl"}},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"

            client = GithubOrgClient("test")
            result = client.public_repos()

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected boolean"""
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    [
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure the mock to return different payloads based on URL
        def side_effect(url):
            mock_response = Mock()
            if "orgs/google" in url and "repos" not in url:
                mock_response.json.return_value = cls.org_payload
            elif "orgs/google/repos" in url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """Integration test for public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()

        # This should return the actual repo names from the fixture
        self.assertEqual(repos, self.expected_repos)


if __name__ == "__main__":
    unittest.main()
