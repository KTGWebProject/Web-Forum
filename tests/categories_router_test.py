from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
import users_router_test as urt
from fastapi.testclient import TestClient
from main import app
import categories_tests_data as ctd



class CategoriesRouterShould(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_viewCategories_show_categories_to_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_all_categories", return_value=ctd.FAKE_CATEGORIES_ALL_PAGE1_ASC):

            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            name = None # default
            page = 1 # default

            response = self.client.get("/categories", headers=token, params={"name": name, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_CATEGORIES_ALL_PAGE1_ASC, response.json())
    
    def test_viewCategories_shows_the_second_page(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_all_categories", return_value=ctd.FAKE_CATEGORIES_ALL_PAGE2_ASC):

            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            name = None # default
            page = 2

            response = self.client.get("/categories", headers=token, params={"name": name, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_CATEGORIES_ALL_PAGE2_ASC, response.json())

    def test_viewCategories_filters_by_name(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_all_categories", return_value=ctd.FAKE_CATEGORIES_FILTER_BOA):

            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            name = "boa"
            page = 1 # default

            response = self.client.get("/categories", headers=token, params={"name": name, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_CATEGORIES_FILTER_BOA, response.json())


    def test_viewCategories_show_categories_to_user(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()), \
            patch("routers.categories.categories_services.get_all_categories", return_value=ctd.FAKE_CATEGORIES_USER_PAGE1_ASC):
            
            token = ctd.FAKE_HEADERS_TOKEN_USER
            name = None # default
            page = 1 # default

            response = self.client.get("/categories", headers=token, params={"name": name, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_CATEGORIES_USER_PAGE1_ASC, response.json())

    def test_viewTopicsByCategoryId_when_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_topics_by_cat_id", return_value=ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE1):

            cat_id = 1
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            topic_title = None
            sorted = "asc" # default
            page = 1 # default

            response = self.client.get(f"categories/{cat_id}", headers=token, params={"token_title": topic_title, "sorted": sorted, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE1, response.json())

    def test_viewTopicsByCategoryId_second_admin_page(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_topics_by_cat_id", return_value=ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE2):

            cat_id = 1
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            topic_title = None # default
            sorted = "asc" # defajlt
            page = 2

            response = self.client.get(f"categories/{cat_id}", headers=token, params={"token_title": topic_title, "sorted": sorted, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE2, response.json())
    
    def test_viewTopicsByCategoryId_desc_second_admin_page(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_topics_by_cat_id", return_value=ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_PAGE2):

            cat_id = 1
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            topic_title = None # default
            sorted = "desc"
            page = 2

            response = self.client.get(f"categories/{cat_id}", headers=token, params={"token_title": topic_title, "sorted": sorted, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_PAGE2, response.json())

    def test_viewTopicsByCategoryId_desc_second_admin_page_TopicTitleFilter(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_topics_by_cat_id", return_value=ctd.FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_TT_BMW):

            cat_id = 1
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            topic_title = "bmw"
            sorted = "desc"
            page = 1

            response = self.client.get(f"categories/{cat_id}", headers=token, params={"token_title": topic_title, "sorted": sorted, "page": page})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_TT_BMW, response.json())
            
    def test_GetPrivilegedUsersByCat_when_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.get_privileged_users", return_value=ctd.FAKE_PRIVILEGED_USRS_CAT_ID8):

            cat_id = 8
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            
            response = self.client.get(f"categories/{cat_id}/privileged_users", headers=token)

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.FAKE_PRIVILEGED_USRS_CAT_ID8, response.json())

    def test_GetPrivilegedUsersByCat_raises_Unauthorized_when_not_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):

            cat_id = 8
            token = ctd.FAKE_HEADERS_TOKEN_USER
            
            response = self.client.get(f"categories/{cat_id}/privileged_users", headers=token)

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "You are not admin! You are not authorized to see privileged_users!"}, response.json()) 
    
    def test_createCategory_when_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.create_new_category", return_value=ctd.FAKE_CATEGORY):

            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            fake_category = ctd.FAKE_CATEGORY

            response = self.client.post("/categories", headers=token, json=fake_category)

            self.assertEqual(201, response.status_code)
            self.assertEqual(fake_category, response.json())

    def test_createCategory_raises_CONFLICT_onDuplicateNames(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.create_new_category", return_value=ctd.FAKE_CONFLICT_HTTPException):

            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            fake_category = ctd.FAKE_CATEGORY

            response = self.client.post("/categories", headers=token, json=fake_category)

            self.assertEqual({"detail": "Category with name 'Cooking' already exists!", "status_code": 409,"headers": None}, response.json(), )
    
    def test_createCategory_raises_Unauthorized_when_not_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):

            token = ctd.FAKE_HEADERS_TOKEN_USER
            fake_category = ctd.FAKE_CATEGORY

            response = self.client.post("/categories", headers=token, json=fake_category)

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "Not authorized to create Category!"}, response.json())

    def test_changePrivacy_returns_correctly(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.change_category_privacy", return_value=ctd.FAKE_CHANGE_CATEGORY_PRIVACY_TO_PRIVATE_RETURN):

            cat_id = 17
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            privacy_status = "private"

            response = self.client.put(f"/categories/{cat_id}/privacy", headers=token, params={"privacy_status": privacy_status})

            self.assertEqual(200, response.status_code)
            self.assertEqual("Category '17' changed status to 'private'.", response.json())

    def test_changePrivacy_raises_Unauthorized_when_not_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):

            cat_id = 17
            token = ctd.FAKE_HEADERS_TOKEN_USER
            privacy_status = "private"

            response = self.client.put(f"/categories/{cat_id}/privacy", headers=token, params={"privacy_status": privacy_status})

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "Not authorized to change the category status!"}, response.json())

    def test_changePrivacy_raises_NotFound_if_no_such_category(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.change_category_privacy", return_value = ctd.NO_CATEGORY_OR_SAME_STATUS):

            cat_id = len(ctd.ALL_FAKE_CATEGORIES) + 1
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN
            privacy_status = "private"

            response = self.client.put(f"/categories/{cat_id}/privacy", headers=token, params={"privacy_status": privacy_status})

            self.assertEqual("Category with id '42' doesnt exist or it's status is already private!", response.json())


    def test_giveUserReadAccess_gives_read_access(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.give_read_access_to_user", return_value = ctd.SUCCESSFUL_GIVING_READ_ACCESS):
            
            cat_id = 8
            user_id = 5
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.put(f"/categories/{cat_id}/access/read", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.SUCCESSFUL_GIVING_READ_ACCESS, response.json())
    
    def test_giveUserReadAccess_raises_Unauthorized_when_not_admin(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):
            
            cat_id = 8
            user_id = 5
            token = ctd.FAKE_HEADERS_TOKEN_USER

            response = self.client.put(f"/categories/{cat_id}/access/read", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "You are not admin! You are not authorized to give read access!"}, response.json())

    def test_giveUserReadAccess_raises_NotFound_if_wrong_cat_id_or_user_id(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.give_read_access_to_user", return_value = ctd.UNSUCCESSFUL_GIVING_READ_or_WRITE_ACCESS):
            
            cat_id = 42
            user_id = 35
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.put(f"/categories/{cat_id}/access/read", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(ctd.UNSUCCESSFUL_GIVING_READ_or_WRITE_ACCESS, response.json())

    def test_giveUserReadAccess_gives_write_access(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.give_write_access_to_user", return_value = ctd.SUCCESSFUL_GIVING_WRITE_ACCESS):
            
            cat_id = 8
            user_id = 5
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.put(f"/categories/{cat_id}/access/write", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.SUCCESSFUL_GIVING_WRITE_ACCESS, response.json())
    
    def test_giveUserReadAccess_raises_Unauthorized_when_not_admin(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):
            
            cat_id = 8
            user_id = 5
            token = ctd.FAKE_HEADERS_TOKEN_USER

            response = self.client.put(f"/categories/{cat_id}/access/write", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "You are not admin! You are not authorized to give write access!"}, response.json())

    def test_giveUserReadAccess_raises_NotFound_if_wrong_cat_id_or_user_id(self):
         with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.give_write_access_to_user", return_value = ctd.UNSUCCESSFUL_GIVING_READ_or_WRITE_ACCESS):
            
            cat_id = 42
            user_id = 35
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.put(f"/categories/{cat_id}/access/write", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(ctd.UNSUCCESSFUL_GIVING_READ_or_WRITE_ACCESS, response.json())

    def test_lockCategory_locks_category(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.lock_category_by_id", return_value = ctd.SUCCESSFUL_LOCK_CATEGORY):

            cat_id = 6
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.patch(f"categories/{cat_id}", headers=token, params={"cat_id": cat_id})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.SUCCESSFUL_LOCK_CATEGORY, response.json())

    def test_lockCategory_raises_Unauthorized_when_not_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):

            cat_id = 6
            token = ctd.FAKE_HEADERS_TOKEN_USER

            response = self.client.patch(f"categories/{cat_id}", headers=token, params={"cat_id": cat_id})

            self.assertEqual(401, response.status_code)
            self.assertEqual({"detail": "You are not admin! You are not authorized to lock categories!"}, response.json())

    def test_lockCategory_raises_NotFound_if_wrong_cat_id(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.lock_category_by_id", return_value = ctd.UNSUCCESSFUL_LOCK_CATEGORY):

            cat_id = 44
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.patch(f"categories/{cat_id}", headers=token, params={"cat_id": cat_id})

            self.assertEqual(ctd.UNSUCCESSFUL_LOCK_CATEGORY, response.json())

    def test_revokeUserAccess_revokes(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.revoke_access", return_value = ctd.SUCCESSFUL_REVOKE_USER_ACCESS):
            
            cat_id = 8
            user_id = 6
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.delete(f"categories/{cat_id}/access", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(200, response.status_code)
            self.assertEqual(ctd.SUCCESSFUL_REVOKE_USER_ACCESS, response.json())
    
    def test_revokeUserAccess_raises_Unauthorized_when_not_admin(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_user()):
            
            cat_id = 8
            user_id = 6
            token = ctd.FAKE_HEADERS_TOKEN_USER

            response = self.client.delete(f"categories/{cat_id}/access", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual({"detail":"You are not admin! You are not authorized to revoke user access!"}, response.json())
    
    def test_revokeUserAccess_NotFound_if_wrong_cat_id(self):
        with patch("common.auth.get_current_user", return_value=urt.fake_registered_admin()), \
            patch("routers.categories.categories_services.revoke_access", return_value = ctd.UNSUCCESSFUL_REVOKE_USER_ACCESS):
            
            cat_id = 44
            user_id = 45
            token = ctd.FAKE_HEADERS_TOKEN_ADMIN

            response = self.client.delete(f"categories/{cat_id}/access", headers=token, params={"cat_id": cat_id, "user_id": user_id})

            self.assertEqual(ctd.UNSUCCESSFUL_REVOKE_USER_ACCESS, response.json())
