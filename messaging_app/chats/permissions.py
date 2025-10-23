from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants to access conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is part of the conversation participants
        return request.user in obj.participants.all()
