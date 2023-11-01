from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock
from common import auth
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import common.responses as responses
from fastapi.testclient import TestClient
from main import app
import services.messages_services as messages_services
from models.message import MessageResponseModelConversation, MessageResponseModelChat, Message


def generate_fake_messages_db():
    counter = 1
    content = "Message"+f'{counter}'
    fake_db = []
    while counter <=3:
        id = counter
        author = "author"+f'{counter}'
        recipient = "recipient"+f'{counter}'
        content = "Message"+f'{counter}'
        created_on = datetime.utcnow()
        if counter<15:
            subject = "No subject"
        else: 
            subject = "Has subject"
        id_parent_message = 0
        message = (
            id,
            author,
            recipient,
            subject,
            content,
            created_on,
            id_parent_message
            ) 
        fake_db.append(message)
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
        created_on = datetime.utcnow()
        if counter<15:
            subject = "No subject"
        else: 
            subject = "Has subject"
        id_parent_message = 0
        message = (
            id,
            author,
            subject,
            content,
            created_on,
            id_parent_message            
        ) 
        fake_db.append(message)
        counter += 1
    return fake_db

def generate_fake_response_db(fake_db):
    fake_response = []
    inner_list = []
    for item in fake_db:
        id, author, recipient, subject, content, created_on, id_parent_message = item
        inner_list.append(MessageResponseModelConversation.get_response(id, author, recipient, subject, content, created_on, id_parent_message))
    fake_response.append(inner_list)
    return fake_response

def generate_fake_response_db_chat(fake_db):
    fake_response = []
    for item in fake_db:
        id, author, subject, content, created_on, id_parent_message = item
        fake_response.append(MessageResponseModelChat.get_response_chat(id, author, subject, content, created_on, id_parent_message))
    return fake_response

def generate_fake_message():
    fake_message = Message(content = "blah blah", subject = "test", id_parent_message = 15)
    return fake_message

FAKE_RECIPIENTS = ["Kaloyan"]

class MessagesServicesShould(IsolatedAsyncioTestCase):
    
    async def test_getMessages_returnsCorrectMessages_userExists_correctParams(self):
        # Arrange
        fake_db = generate_fake_messages_db()
        fake_response = generate_fake_response_db(fake_db)
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [[(1,2),(2,1),(1,2)], fake_db]
            # act
            response = await messages_services.get_messages(user_id = 1, sort = True, paginated = True, page = 1)
            # Assert
            self.assertEqual(fake_response, response)
            
    async def test_getMessages_returnsEmpty_noMessages_userExists_correctParams(self):
        # Arrange
        fake_db = []
        fake_response = []
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [[], fake_db]
            # act
            response = await messages_services.get_messages(user_id = 1, sort = True, paginated = True, page = 1)
            # Assert
            self.assertEqual(fake_response, response)
    
    async def test_getMessagesUser_returnsCorrectMessages_userExists_correctParams(self):
        # Arrange
        fake_db = generate_fake_messages_db()
        fake_response = [generate_fake_response_db(fake_db)]
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [[("No subject")*3], fake_db]
            # act
            response = await messages_services.get_messages_user(user_id = 1, sort = True, paginated = True, page = 1, username='test')
            # Assert
            self.assertEqual(fake_response, response)
    
    async def test_getMessagesUser_returnsEmpty_NoMessages_userExists_correctParams(self):
        # Arrange
        fake_db = []
        fake_response = [[[]]]
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [[("No subject")*3], fake_db]
            # act
            response = await messages_services.get_messages_user(user_id = 1, sort = True, paginated = True, page = 1, username='test')
            # Assert
            self.assertEqual(fake_response, response)
    
    async def test_getChat_returnsEmpty_noMessagesReceived(self):
        # Arrange
        fake_db = []
        fake_response = []
        with patch('services.messages_services.read_query', return_value= fake_db):
            # Act
            response = await messages_services.get_chat_service(user_id = 1, since=datetime.utcnow().replace(microsecond=0))
            # Assert
            self.assertEqual(fake_response, response)
    
    async def test_postMessages_postsMessage_validParams(self):
        # Arrange
        fake_response = 10
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [[(5,)], [(3,)]]
            with patch ('services.messages_services.insert_query') as insert_func:
                insert_func.side_effect = [10, None]
                # Act
                fake_message = generate_fake_message()
                response = await messages_services.post_message(1,fake_message, FAKE_RECIPIENTS)
                # Assert
                self.assertEqual(fake_response, response)
    
    async def test_raisesNotFound_invalidRecipient(self):
        # Arrange
        fake_response = 10
        with patch('services.messages_services.read_query') as read_func:
            read_func.side_effect = [HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user(s)"), [(3,)]]
            with patch ('services.messages_services.insert_query') as insert_func:
                insert_func.side_effect = [10, None]
                
                #Act
                fake_message = generate_fake_message()
                with self.assertRaises(HTTPException) as context:
                    await messages_services.post_message(1,fake_message, [])
                # Assert
                self.assertEqual(404, context.exception.status_code)
                self.assertEqual("No such user(s)", context.exception.detail)