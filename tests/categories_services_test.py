from unittest import TestCase
from unittest.mock import patch
import services.categories_services as cs
import categories_tests_data as ctd
import users_router_test as urt
from fastapi import HTTPException
import common.responses as responses
import mariadb as mdb




class CategoriesServicesShould(TestCase):
    def test_readCategoryParams_non_private_unlocked(self):
        result = cs.read_category_params(
            ctd.FAKE_CATEGORY_PARAMS_FROM_DB_NON_PRIVATE_UNLOCKED
        )

        expected = (10, "Pesho", "2023-10-30 09:00:00", "non_private", "unlocked")

        self.assertEqual(expected, result)

    def test_readCategoryParams_private_locked(self):
        result = cs.read_category_params(ctd.FAKE_CATEGORY_PARAMS_FROM_DB_PRIVATE_LOCKED)

        expected = (10, "Pesho", "2023-10-30 09:00:00", "private", "locked")

        self.assertEqual(expected, result)

    def test_readTopicParams_unlocked(self):
        with patch(
            "services.categories_services.find_user_by_id", return_value="Tosho"
        ):
            result = cs.read_topic_params(ctd.FAKE_TOPIC_PARAMS_FROM_DB_UNLOCKED)

            expected = (
                11,
                "Razer",
                "2023-10-30 09:05:00",
                "Very good computer products",
                17,
                "Tosho",
                0,
                "unlocked",
            )

            self.assertEqual(expected, result)

    def test_readTopicParams_locked(self):
        with patch(
            "services.categories_services.find_user_by_id", return_value="Tosho"
        ):
            result = cs.read_topic_params(ctd.FAKE_TOPIC_PARAMS_FROM_DB_LOCKED)

            expected = (
                11,
                "Razer",
                "2023-10-30 09:05:00",
                "Very good computer products",
                17,
                "Tosho",
                0,
                "locked",
            )

            self.assertEqual(expected, result)

    def test_convertStatus_private(self):
        result = cs.convert_status("private")
        expected = 1

        self.assertEqual(expected, result)

    def test_convertStatus_non_private(self):
        result = cs.convert_status("non_private")
        expected = 0

        self.assertEqual(expected, result)

    def test_convertReadWriteAccess_str_write(self):
        result = cs.convert_read_write_access("write")

        expected = 1

        self.assertEqual(expected, result)

    def test_convertReadWriteAccess_str_read(self):
        result = cs.convert_read_write_access("read")

        expected = 0

        self.assertEqual(expected, result)

    def test_convertReadWriteAccess_int_1(self):
        result = cs.convert_read_write_access(1)

        expected = "write"

        self.assertEqual(expected, result)

    def test_convertReadWriteAccess_int_0(self):
        result = cs.convert_read_write_access(0)

        expected = "read"

        self.assertEqual(expected, result)

    def test_findUserById(self):
        with patch(
            "services.categories_services.read_query", return_value=[("Tosho",)]
        ):
            result = cs.find_user_by_id(10)

            expected = "Tosho"

            self.assertEqual(expected, result)

    def test_getAllCategories_user_admin_page_1(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_CATEGORIES_PAGE_1_RAW,
        ):
            result = cs.get_all_categories(urt.fake_registered_admin(), None, 1)

            expected = ctd.ALL_FAKE_CATEGORIES_PAGE_1_RESULT

            self.assertEqual(expected, result)

    def test_getAllCategories_user_admin_page_2(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_CATEGORIES_PAGE_2_RAW,
        ):
            result = cs.get_all_categories(urt.fake_registered_admin(), None, 2)

            expected = ctd.ALL_FAKE_CATEGORIES_PAGE_2_RESULT

            self.assertEqual(expected, result)

    def test_getAllCategories_user_admin_namefiltered(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_CATEGORIES_FILTERED_NAME_CAR_RAW,
        ):
            result = cs.get_all_categories(urt.fake_registered_admin(), "car", 1)

            expected = ctd.ALL_FAKE_CATEGORIES_FILTERED_NAME_CAR_RESULT

            self.assertEqual(expected, result)

    def test_getAllCategories_user_not_admin_filtered(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_CATEGORIES_FILTERED_NAME_BO_RAW,
        ):
            result = cs.get_all_categories(urt.fake_registered_user(), "bo", 1)

            expected = ctd.ALL_FAKE_CATEGORIES_FILTERED_NAME_BO_RESULT

            self.assertEqual(expected, result)

    def test_getAllCategories_no_user(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_CATEGORIES_NON_PRIVATE_RAW,
        ):
            result = cs.get_all_categories(None, None, 1)

            expected = ctd.ALL_FAKE_CATEGORIES_NON_PRIVATE_RESULT

            self.assertEqual(expected, result)

    def test_getTopicsByCatId_admin_page_1(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_TOPICS_PAGE_1_RAW,
        ), patch("services.categories_services.find_user_by_id", return_value="Kolio"):
            result = cs.get_topics_by_cat_id(
                1, urt.fake_registered_admin(), None, "asc", 1
            )

            expected = ctd.ALL_FAKE_TOPICS_PAGE_1_RESULT

            self.assertEqual(expected, result)

    def test_getTopicsByCatId_admin_page_2(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_TOPICS_PAGE_2_RAW,
        ), patch("services.categories_services.find_user_by_id", return_value="Kolio"):
            result = cs.get_topics_by_cat_id(
                1, urt.fake_registered_admin(), None, "asc", 2
            )

            expected = ctd.ALL_FAKE_TOPICS_PAGE_2_RESULT

            self.assertEqual(expected, result)

    def test_getTopicsByCatId_user_filtered(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_TOPICS_FILTERED_ALFA_RAW,
        ), patch("services.categories_services.find_user_by_id", return_value="Kolio"):
            result = cs.get_topics_by_cat_id(
                1, urt.fake_registered_user(), "alfa", "asc", 1
            )

            expected = ctd.ALL_FAKE_TOPICS_FILTERED_ALFA_RETURN

            self.assertEqual(expected, result)

    def test_getTopicsByCatId_user_sorted_desc_page_2(self):
        with patch(
            "services.categories_services.read_query",
            return_value=ctd.ALL_FAKE_TOPICS_SORTED_DESC_PAGE_2_RAW,
        ), patch("services.categories_services.find_user_by_id", return_value="Kolio"):
            result = cs.get_topics_by_cat_id(
                1, urt.fake_registered_user(), "alfa", "asc", 1
            )

            expected = ctd.ALL_FAKE_TOPICS_SORTED_DESC_PAGE_2_RESULT

            self.assertEqual(expected, result)

    def test_getTopicsByCatId_no_topics(self):
        with patch(
            "services.categories_services.read_query", return_value=ctd.EMPTY_LIST
        ):
            result = cs.get_topics_by_cat_id(
                7, urt.fake_registered_user(), "alfa", "asc", 1
            )

            expected = ctd.EMPTY_LIST

            self.assertEqual(expected, result)

    def test_createNewCategory_creates_successfully(self):
        with patch(
            "services.categories_services.insert_query", return_value=ctd.FAKE_LASTROWID
        ):
            result = cs.create_new_category(ctd.FAKE_CATEGORY_FOR_INSERT, 2)

            expected = ctd.CREATE_CATEGORY_SUCCESSFUL_RETURN

            self.assertEqual(
                (expected.id, expected.access_status, expected.name),
                (result.id, result.access_status, result.name),
            )

    def test_createNewCategory_raises_HTTPException(self):
        with patch("services.categories_services.insert_query", return_value=0):
            try:
                cs.create_new_category(ctd.FAKE_CATEGORY_FOR_INSERT, 2)
            except HTTPException as e:
                self.assertEqual(e.status_code, responses.CONFLICT().status_code)

    def test_changeCategoryPrivacy_changes_successfully(self):
        with patch("services.categories_services.update_query", return_value=1), \
            patch("services.categories_services.convert_status", return_value=1):
            result = cs.change_category_privacy(17, "private")

            expected = ctd.FAKE_CHANGE_CATEGORY_PRIVACY_RESULT

            self.assertEqual(200, result.status_code)
            self.assertEqual(expected, result.body.decode("utf-8"))

    def test_changeCategoryPrivacy_raises_HTTPException(self):
        with patch("services.categories_services.update_query", return_value=0), \
            patch("services.categories_services.convert_status", return_value=1):

            expected = ctd.FAKE_CHANGE_CATEGORY_PRIVACY_EXCEPTION_STRING

            with self.assertRaises(HTTPException) as h:
                cs.change_category_privacy(cat_id=17, privacy_status="private")
            
            self.assertEqual(404, h.exception.status_code)
            self.assertEqual(expected, h.exception.detail)

    def test_giveReadAccessToUser_gives_read_access(self):
        with patch("services.categories_services.update_query", return_value=1):

            result = cs.give_read_access_to_user(user_id=6, cat_id=9)

            expected = ctd.FAKE_GIVE_READ_ACCESS_RETURN

            self.assertEqual(200, result.status_code)
            self.assertEqual(expected, result.body.decode("utf-8"))

    def test_giveReadAccessToUser_raises_HTTPException(self):
        with patch("services.categories_services.update_query", return_value=0):
            
            expected = ctd.FAKE_GIVE_READ_ACCESS_EXCEPTION_STRING

            with self.assertRaises(HTTPException) as h:
                cs.give_read_access_to_user(user_id=6, cat_id=9)
            
            self.assertEqual(404, h.exception.status_code)
            self.assertEqual(expected, h.exception.detail)
    
    def test_giveWriteAccessToUser_gives_Write_access(self):
        with patch("services.categories_services.update_query", return_value=1):

            result = cs.give_write_access_to_user(user_id=6, cat_id=9)

            expected = ctd.FAKE_GIVE_WRITE_ACCESS_RETURN

            self.assertEqual(200, result.status_code)
            self.assertEqual(expected, result.body.decode("utf-8"))
    
    def test_giveWriteAccessToUser_raises_HTTPException(self):
        with patch("services.categories_services.update_query", return_value=0):
            
            expected = ctd.FAKE_GIVE_WRITE_ACCESS_EXCEPTION_STRING

            with self.assertRaises(HTTPException) as h:
                cs.give_read_access_to_user(user_id=6, cat_id=9)
            
            self.assertEqual(404, h.exception.status_code)
            self.assertEqual(expected, h.exception.detail)
    
    def test_lockCategoryById_locks_category(self):
        with patch("services.categories_services.update_query", return_value=1):
            
            result = cs.lock_category_by_id(cat_id=10)
            
            expected = ctd.FAKE_LOCK_CATEGORY_SUCCESSFUL_STRING

            self.assertEqual(200, result.status_code)
            self.assertEqual(expected, result.body.decode("utf-8"))

    def test_lockCategoryById_raises_HTTPExeption(self):
        with patch("services.categories_services.update_query", return_value=0):
            
            expected = ctd.FAKE_LOCK_CATEGORY_EXCEPTION_STRING

            with self.assertRaises(HTTPException) as h:
                cs.lock_category_by_id(cat_id=10)
            
            self.assertEqual(404, h.exception.status_code)
            self.assertEqual(expected, h.exception.detail)
    
    def test_revokeAccess_revokes_successfully(self):
        with patch("services.categories_services.update_query", return_value=1):

            expected = ctd.FAKE_REVOKE_ACCESS_SUCCESSFUL_STRING

            result = cs.revoke_access(user_id=6, cat_id=8)

            self.assertEqual(200, result.status_code)
            self.assertEqual(expected, result.body.decode("utf-8"))

    def test_revokeAccess_raises_HTTPExeption(self):
        with patch("services.categories_services.update_query", return_value=0):

            expected = ctd.FAKE_REVOKE_ACCESS_EXCEPTION_STRING

            with self.assertRaises(HTTPException) as h:
                cs.revoke_access(user_id=6, cat_id=8)

            self.assertEqual(404, h.exception.status_code)
            self.assertEqual(expected, h.exception.detail)