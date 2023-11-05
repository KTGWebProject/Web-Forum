from json import JSONEncoder
from models.reply import Reply
from models.topic import Topic, TopicResponse
from models.categories import Category
from routers import (topics as tr, categories as cats)
from services import topics_services as ts
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Path, Query, Response
import common.responses as responses
from fastapi.testclient import TestClient
from main import app
import users_router_test as urt
import categories_tests_data as ctd

ake_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# mock_cat_service = Mock(spec='services.categories_services')
# mock_topic_service = Mock(spec='services.topics_services')
# tr.ts = mock_topic_service
# cats = mock_cat_service

def fake_admin_user():
    admin = {'username': "username",
            'password': "2Wsx3edc+",
            'is_admin': 1}
    return admin


def fake_usr():
    user = {'username': "username",
            'password': "2Wsx3edc+",
            'is_admin': 0}
    return user


def fake_cat():
    category = {'id': 1,
                'name': 'Fake category name',
                'created_on': None,
                'privacy_status': 'non_private',
                'access_status': 'unlocked'}
    return category

def fake_top():
    topic = {'id': 1,
            'title': 'I am fake',
            'created_on': datetime(2023, 10, 20, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S"),
            'text': 'Something meaningful',
            'category_id': 1, 
            'author_id': None,
            'replies': [],
            'is_locked': False}
    return topic

def fake_rep():
    reply = {'id': 1,
            'content': 'Fake content',
            'topic_id': 1,
            'user_id':  None,
            'created_on': datetime(2023, 11, 20, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S"),
            'is_best':  False, 
            'upvotes':  0,
            'downvotes': 0}            
    return reply



fake_user = fake_usr()
fake_admin = fake_admin_user()
fake_topic = fake_top()
fake_category = fake_cat()
fake_reply = fake_rep()

fake_topic1 = fake_top()
fake_topic1['id'] = 2 
fake_topic1['category_id'] = 1 
fake_topic1['title'] = 'I am fake as well'
fake_topic1['created_on'] = datetime(2023, 10, 21, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S")

fake_topic2 = fake_top()
fake_topic2['id'] = 3 
fake_topic2['category_id'] = 1 
fake_topic2['title'] = 'I am also fake'
fake_topic2['created_on'] = datetime(2023, 10, 22, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S")

fake_reply1 = fake_rep()
fake_reply1['id'] = 2
fake_reply1['content'] = 'Bullshirt content' 
fake_reply1['topic_id'] = 1
fake_reply1['created_on'] = datetime(2023, 11, 21, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S")

fake_reply2 = fake_rep()
fake_reply2['id'] = 3 
fake_reply2['content'] = 'Fork off content'
fake_reply2['topic_id'] = 1
fake_reply2['created_on'] = datetime(2023, 11, 22, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S")

fake_topic_response = {'id': 1,
    'topic_id': 1,
    'content': 'Bullshirt content', 
    'username': 'Fake username', 
    'created': datetime(2023, 11, 21, 14, 00, 00).strftime("%Y-%m-%dT%H:%M:%S"),
    'upvotes': 0,
    'downvotes': 0,
    'is_best': False}

fake_topic_with_replies = fake_top()
fake_topic_with_replies['id'] = 4
fake_topic_with_replies['replies'] = [fake_topic_response]



class TopicsRouterShould(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        
    
    def test_viewAllTopicsInACategory_raisesUnauthorisedErrorWithoutToken(self):
        # Arrange
        with (
            patch('common.auth.get_current_user', return_value=urt.fake_registered_user()),
            patch('services.topics_services.view_all_topics')): 
                                 
        # Act
            response = self.client.get("/topics")
        # Assert
            self.assertEqual(401, response.status_code)


    def test_viewAllTopicsInACategory_returnsEmtpyListWhenNoTopics(self):
        # Arrange
        with (
            patch('common.auth.get_current_user', return_value=urt.fake_registered_user()),
            patch('services.topics_services.view_all_topics', return_value = [])): 
            token = ctd.FAKE_HEADERS_TOKEN_USER                    
        # Act
            response = self.client.get("/topics", headers=token)
            expected = []
        # Assert

            self.assertEqual(200, response.status_code)
            self.assertListEqual(expected, response.json())


    def test_viewAllTopicsInACategory_returnsListWithTopics(self):
        # Arrange
        with (
            patch('common.auth.get_current_user', return_value=urt.fake_registered_user()), 
            patch('services.topics_services.view_all_topics', 
                  return_value=[fake_topic])):
            token = ctd.FAKE_HEADERS_TOKEN_USER      
        # Act
            response = self.client.get("/topics", headers=token)
            expected = [fake_topic]
        # Assert
            self.assertTrue(response.status_code == 200)
            self.assertEqual(expected, response.json())

    def test_viewTopic_returnsNotFound_ifTopicWithIdThatIsNotFound(self):
        # Arrange
        with (patch('routers.topics'), 
              patch('services.topics_services.get_topic_by_id', return_value=None)):           
        # Act
            response = self.client.get("/topics/3")
            
        # Assert
            self.assertEqual(404, response.status_code)
        

    def test_viewTopic_returnsTopic_ifTopicWithNoRepliesIsFound(self):
        # Arrange
        with (patch('routers.topics'), 
              patch('services.topics_services.get_topic_by_id', return_value=fake_topic)):           
        # Act
            response = self.client.get("/topics/1")
            expected = fake_topic

        # Assert
            self.assertEqual(200, response.status_code)
            self.assertEqual(expected, response.json())


    def test_viewTopic_returnsTopic_ifTopicWithRepliesIsFound(self):
        # Arrange
        with (patch('routers.topics'), 
              patch('services.topics_services.get_topic_by_id', return_value=fake_topic_with_replies)):           
        # Act
            response = self.client.get("/topics/4")
            expected = fake_topic_with_replies

        # Assert
            self.assertEqual(200, response.status_code)
            self.assertEqual(expected, response.json())

# post/ (create_topic()) creates and returns a new topic if successful
#   or return BadRequest if the topic title exists in the database (mariadb IntegrityError)
#   
    def test_postTopic_returnsTopic(self):
        # Arrange
        with (patch('common.auth.get_current_user', return_value=urt.fake_registered_admin()),
              patch('services.topics_services.user_has_write_access', return_value=True),
              patch('services.topics_services.create_topic', return_value=[])):

            token=ctd.FAKE_HEADERS_TOKEN_ADMIN
            data = {'title': 'I am fake',
                    'text': 'Something meaningful',
                    'category_id': 1}
        # Act       
            response = self.client.post('/topics/', headers=token, params=data)
            expected = fake_topic
        # Assert
            self.assertEqual(201, response.status_code)
            self.assertListEqual(expected, response.json())



# patch/{id} (edit_topic()) check if the topic exists
#   check return when you edit the title
#   check return when you edit the text
#   check return when you edit both

# get/count/{category_id} (topics_count()) returns correct count w/ and w/o topics

# put/{id} (lock_topic()) returns NotFound if topic doesn't exist
#   return 403_forbidden if the user is not admin
#   return 208_already_reported if the topic is already locked
#   return existing_topic when the operation was successful