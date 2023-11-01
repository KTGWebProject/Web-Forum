from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock
from common import auth
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
import common.responses as responses
from fastapi.testclient import TestClient
from main import app
from models.message import Message

fixed_now = datetime(2025, 10, 25, 13, 42, 20)
fake_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#Below Test show only that correct responses are returned as the logic relates solely to querying the database

def generate_fake_messages_db():
    counter = 1
    content = "Message"+f'{counter}'
    fake_db = []
    inner_list = []
    while counter <3:
        id = counter
        author = "author"+f'{counter}'
        recipient = "recipient"+f'{counter}'
        content = "Message"+f'{counter}'
        created_on = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if counter<15:
            subject = "No subject"
        else: 
            subject = "Has subject"
        id_parent_message = 0
        message = {
            "id": id,
            "content": content,
            "created_on": created_on,
            "subject": subject,
            "id_parent_message": id_parent_message,
            "author": author,
            "recipient": recipient
        } 
        inner_list.append(message)
        fake_db.append(inner_list)
        counter += 1
    return fake_db

def generate_fake_messages_db_chat():
    counter = 1
    content = "Message"+f'{counter}'
    fake_db = []
    while counter <3:
        id = counter
        author = "author"+f'{counter}'
        content = "Message"+f'{counter}'
        created_on = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        if counter<15:
            subject = "No subject"
        else: 
            subject = "Has subject"
        id_parent_message = 0
        message = {
            "id": id,
            "content": content,
            "created_on": created_on,
            "subject": subject,
            "id_parent_message": id_parent_message,
            "author": author
        } 
        fake_db.append(message)
        counter += 1
    return fake_db



def fake_registered_user():
    registered_user = Mock()
    registered_user.id = 1
    registered_user.username = "username"
    registered_user.password = fake_pwd_context.hash("2Wsx3edc+")
    registered_user.is_admin = 0
    return registered_user

def generate_fake_access_token(fake_user_for_test):
    fake_access_token_expires = fixed_now + \
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    fake_access_data = {"sub": fake_user_for_test.username,
                               "is_admin": fake_user_for_test.is_admin, "exp": fake_access_token_expires}
    fake_access_token = jwt.encode(
        fake_access_data, auth.SECRET_KEY, algorithm=auth.ALGORITHM)
    return fake_access_token

def generate_fake_message():
    fake_message = {"message":{"content": "blah blah", "subject": "test", "id_parent_message":15}, "recipients":["Kaloyan"]}
    return fake_message
    

class MessagesRouterShould(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def test_getMessages_returnsValidMessages(self):
            fake_db = generate_fake_messages_db()
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_messages', return_value=fake_db):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {"sort": True, "paginated": False, "page": 1}
                
                # Act
                response = self.client.get(
                    "/messages", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(fake_db, response.json())
    
    def test_getMessages_returnsEmptyList_noMessages(self):
            fake_db = []
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_messages', return_value=fake_db):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {"sort": True, "paginated": False, "page": 1}
                
                # Act
                response = self.client.get(
                    "/messages", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(fake_db, response.json())
    
    def test_getConversationsUsers_returnsValidConversations(self):
            fake_db = generate_fake_messages_db()
            output = [[[fake_db[0][0]]]]
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_messages_user', return_value=output):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {"sort": True, "paginated": False, "page": 1,"username":"username1"}
                
                
                # Act
                response = self.client.get(
                    "/messages/specified", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(output, response.json())
    
    def test_getConversationsUsers_returnsEmptyList_noMessages(self):
            output = []
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_messages_user', return_value=output):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {"sort": True, "paginated": False, "page": 1,"username":"username1"}
                
                
                # Act
                response = self.client.get(
                    "/messages/specified", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(output, response.json())
    
    def test_getChat_returnsValidMessages(self):
            fake_db = generate_fake_messages_db_chat()
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_chat_service', return_value=fake_db):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {'since': datetime(2023, 10, 25, 13, 42, 20)}
                
                # Act
                response = self.client.get(
                    "/messages/chat", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(fake_db, response.json())
    
    def test_getChat_returnsEmpty_noMessages(self):
            fake_db = []
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                    patch('routers.messages.get_chat_service', return_value=fake_db):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                params = {'since': datetime(2023, 10, 25, 13, 42, 20)}
                
                # Act
                response = self.client.get(
                    "/messages/chat", headers=headers, params=params)
                
                #Assert:
                self.assertEqual(200, response.status_code)
                self.assertEqual(fake_db, response.json())
    
    def test_postMessage_postsMessage_returnsMessgeID(self):
            fake_message = generate_fake_message()
            with patch('routers.messages.auth.get_current_user', return_value=fake_registered_user()), \
                patch('routers.messages.post_message', return_value=30):
                # Arrange
                fake_user_for_test = fake_registered_user()
                fake_access_token = generate_fake_access_token(fake_user_for_test)
                headers = {'Authorization': f'Bearer {fake_access_token}'}
                
                # Act
                response = self.client.post(
                    "/messages", headers=headers, json=fake_message)
                
                #Assert:
                self.assertEqual(201, response.status_code)
                self.assertEqual(30, response.json())
    