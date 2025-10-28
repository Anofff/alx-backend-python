# Messaging App with JWT Authentication

A Django REST API messaging application with JWT authentication, custom permissions, pagination, and filtering.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication
- **Custom Permissions**: Only conversation participants can access messages
- **Pagination**: 20 messages per page with configurable page size
- **Filtering**: Filter messages by date range and user
- **RESTful API**: Full CRUD operations for conversations and messages

## 📋 Requirements

- Python 3.8+
- Django 5.2+
- Django REST Framework
- djangorestframework-simplejwt
- django-filter

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd messaging_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows
   # or
   source .venv/bin/activate     # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   # or
   pip install djangorestframework djangorestframework-simplejwt django-filter
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Authentication

### Get JWT Token
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Refresh Token
```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### Use Token in Requests
```bash
Authorization: Bearer <your_access_token>
```

## 📡 API Endpoints

### Authentication Endpoints
- `POST /api/token/` - Get JWT access and refresh tokens
- `POST /api/token/refresh/` - Refresh access token

### Conversation Endpoints
- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `PUT /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation

### Message Endpoints
- `GET /api/messages/` - List messages (with pagination and filtering)
- `POST /api/messages/` - Send new message
- `GET /api/messages/{id}/` - Get message details
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message

## 🔍 Filtering and Pagination

### Pagination
- Default: 20 messages per page
- Configurable: `?page=1&page_size=10`
- Maximum page size: 100

### Filtering
- **Date Range**: `?start_date=2024-01-01T00:00:00Z&end_date=2024-12-31T23:59:59Z`
- **User**: `?user=username`
- **Combined**: `?start_date=2024-01-01T00:00:00Z&user=testuser&page=1`

## 🧪 Testing

### Using Postman
1. Import the `postman_collection.json` file
2. Set the `base_url` variable to `http://localhost:8000`
3. Run the "Get JWT Token" request first
4. The access token will be automatically saved for other requests

### Using Python Test Script
```bash
python test_api.py
```

## 🏗️ Project Structure

```
messaging_app/
├── chats/
│   ├── __init__.py
│   ├── models.py              # User, Conversation, Message models
│   ├── views.py               # ViewSets with authentication & permissions
│   ├── urls.py                # API routes
│   ├── serializers.py         # Data serialization
│   ├── permissions.py         # Custom permission classes
│   ├── filters.py             # Message filtering
│   ├── pagination.py          # Pagination configuration
│   └── auth.py                # JWT helper functions
├── messaging_app/
│   ├── settings.py            # Django settings with JWT config
│   └── urls.py                # Main URL configuration
├── postman_collection.json    # Postman test collection
├── test_api.py               # Python test script
└── manage.py
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Custom Permissions**: `IsParticipantOfConversation` ensures users can only access their conversations
- **Global Authentication**: All endpoints require authentication by default
- **User Isolation**: Users can only see messages from conversations they participate in

## 📊 Example Usage

### Create a Conversation
```bash
POST /api/conversations/
Authorization: Bearer <token>
Content-Type: application/json

{
  "participants": [1, 2]
}
```

### Send a Message
```bash
POST /api/messages/
Authorization: Bearer <token>
Content-Type: application/json

{
  "conversation": "conversation-uuid",
  "message_body": "Hello! How are you?"
}
```

### Get Messages with Filtering
```bash
GET /api/messages/?start_date=2024-01-01T00:00:00Z&user=john&page=1&page_size=10
Authorization: Bearer <token>
```

## 🐛 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'django_filters'"**
   - Make sure you're in the virtual environment
   - Run: `source .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)

2. **"Authentication credentials were not provided"**
   - Make sure you're including the JWT token in the Authorization header
   - Format: `Authorization: Bearer <your_access_token>`

3. **"You do not have permission to perform this action"**
   - Check if you're a participant in the conversation
   - Verify the JWT token is valid and not expired

### Server Not Starting
- Check if port 8000 is available
- Try: `python manage.py runserver 0.0.0.0:8000`
- Check Django logs for errors

## 📝 API Response Examples

### Successful Authentication
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Paginated Messages Response
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/messages/?page=2",
  "previous": null,
  "results": [
    {
      "message_id": "uuid",
      "sender": {
        "user_id": "uuid",
        "username": "john",
        "email": "john@example.com",
        "role": "guest"
      },
      "message_body": "Hello!",
      "sent_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## 🎯 Testing Checklist

- [ ] JWT authentication working
- [ ] Custom permissions applied
- [ ] Pagination set to 20 messages/page
- [ ] Filtering by date and user enabled
- [ ] All endpoints tested with Postman
- [ ] Unauthorized access properly blocked
- [ ] Users can only access their own conversations

## 📞 Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.

