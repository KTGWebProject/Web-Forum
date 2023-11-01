import users_router_test as usrt
import common.responses as resp
from fastapi import HTTPException
from unittest.mock import Mock
import datetime
from models.categories import CategoryResponseModel, Category
from models.topic import Topic

ALL_FAKE_CATEGORIES = [
    {
        "category_name": "Airplanes",
        "created_on": "2023-10-21T21:36:59",
        "privacy_status": "private",
    },
    {
        "category_name": "Boats",
        "created_on": "2023-10-21T18:46:10",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cars",
        "created_on": "2023-10-21T18:41:51",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Clothes",
        "created_on": "2023-10-23T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Computers",
        "created_on": "2023-10-24T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cooking",
        "created_on": "2023-10-26T11:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Fishing",
        "created_on": "2023-10-21T18:49:02",
        "privacy_status": "private",
    },
    {
        "category_name": "Hiking",
        "created_on": "2023-10-26T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Hunting",
        "created_on": "2023-10-21T18:49:12",
        "privacy_status": "private",
    },
    {
        "category_name": "IT Education",
        "created_on": "2023-10-26T10:00:00",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Jobs",
        "created_on": "2023-10-22T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Motorcycles",
        "created_on": "2023-10-21T18:48:23",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Music",
        "created_on": "2023-10-25T21:36:59",
        "privacy_status": "non_private",
    },
]


FAKE_CATEGORIES_FILTER_BOA = [
    {
        "category_name": "Boats",
        "created_on": "2023-10-21T18:46:10",
        "privacy_status": "non_private",
    }
]

FAKE_CATEGORIES_ALL_PAGE1_ASC = [
    {
        "category_name": "Airplanes",
        "created_on": "2023-10-21T21:36:59",
        "privacy_status": "private",
    },
    {
        "category_name": "Boats",
        "created_on": "2023-10-21T18:46:10",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cars",
        "created_on": "2023-10-21T18:41:51",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Clothes",
        "created_on": "2023-10-23T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Computers",
        "created_on": "2023-10-24T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cooking",
        "created_on": "2023-10-26T11:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Fishing",
        "created_on": "2023-10-21T18:49:02",
        "privacy_status": "private",
    },
    {
        "category_name": "Hiking",
        "created_on": "2023-10-26T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Hunting",
        "created_on": "2023-10-21T18:49:12",
        "privacy_status": "private",
    },
    {
        "category_name": "IT Education",
        "created_on": "2023-10-26T10:00:00",
        "privacy_status": "non_private",
    },
]

FAKE_CATEGORIES_ALL_PAGE2_ASC = [
    {
        "category_name": "Jobs",
        "created_on": "2023-10-22T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Motorcycles",
        "created_on": "2023-10-21T18:48:23",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Music",
        "created_on": "2023-10-25T21:36:59",
        "privacy_status": "non_private",
    },
]

FAKE_CATEGORIES_USER_PAGE1_ASC = [
    {
        "category_name": "Boats",
        "created_on": "2023-10-21T18:46:10",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cars",
        "created_on": "2023-10-21T18:41:51",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Clothes",
        "created_on": "2023-10-23T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Computers",
        "created_on": "2023-10-24T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Cooking",
        "created_on": "2023-10-26T11:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Fishing",
        "created_on": "2023-10-21T18:49:02",
        "privacy_status": "private",
    },
    {
        "category_name": "Hiking",
        "created_on": "2023-10-26T21:36:59",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Hunting",
        "created_on": "2023-10-21T18:49:12",
        "privacy_status": "private",
    },
    {
        "category_name": "IT Education",
        "created_on": "2023-10-26T10:00:00",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Jobs",
        "created_on": "2023-10-22T21:36:59",
        "privacy_status": "non_private",
    },
]

FAKE_CATEGORIES_USER_PAGE2_ASC = [
    {
        "category_name": "Motorcycles",
        "created_on": "2023-10-21T18:48:23",
        "privacy_status": "non_private",
    },
    {
        "category_name": "Music",
        "created_on": "2023-10-25T21:36:59",
        "privacy_status": "non_private",
    },
]

ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC = [
    {
        "id": 9,
        "title": "Alfa Romeo",
        "created_on": "2023-10-21T21:21:26",
        "text": "Julia is one of the pretiest models!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 16,
        "title": "AUDI",
        "created_on": "2023-10-21T21:28:26",
        "text": "Middle brand. Cars are very difficult for repair.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 17,
        "title": "BMW B57 Engine",
        "created_on": "2023-10-21T21:29:26",
        "text": "The best diesel engine!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 11,
        "title": "BMW E60",
        "created_on": "2023-10-21T21:23:26",
        "text": "E60 one of the best!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 12,
        "title": "BMW M8",
        "created_on": "2023-10-21T21:24:26",
        "text": "M8 is a great car to drive!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 15,
        "title": "Dacia Duster",
        "created_on": "2023-10-21T21:27:26",
        "text": "The best car for the village!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 8,
        "title": "Ferrari",
        "created_on": "2023-10-21T21:20:26",
        "text": "All Ferrari cars are great!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 10,
        "title": "Ferrari F812",
        "created_on": "2023-10-21T21:22:26",
        "text": "F812 Berlinetta has a great sound!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 14,
        "title": "Mercedes AMG GT",
        "created_on": "2023-10-21T21:26:26",
        "text": "AMG GT 63SEperformance WWOOOOW",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 13,
        "title": "Mercedes S 500",
        "created_on": "2023-10-21T21:25:26",
        "text": "W221, a great car!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 21,
        "title": "New Toyota Supra",
        "created_on": "2023-10-21T21:33:26",
        "text": "Toyota/BMW project car",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 19,
        "title": "Pagani",
        "created_on": "2023-10-21T21:31:26",
        "text": "A dream...",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 18,
        "title": "Renault/Mercedes",
        "created_on": "2023-10-21T21:30:26",
        "text": "Renault make engines for Mercedes 180,200 models.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 20,
        "title": "Toyota Land Cruiser",
        "created_on": "2023-10-21T21:32:26",
        "text": "The ultimate SUV",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE1 = [
    {
        "id": 9,
        "title": "Alfa Romeo",
        "created_on": "2023-10-21T21:21:26",
        "text": "Julia is one of the pretiest models!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 16,
        "title": "AUDI",
        "created_on": "2023-10-21T21:28:26",
        "text": "Middle brand. Cars are very difficult for repair.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 17,
        "title": "BMW B57 Engine",
        "created_on": "2023-10-21T21:29:26",
        "text": "The best diesel engine!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 11,
        "title": "BMW E60",
        "created_on": "2023-10-21T21:23:26",
        "text": "E60 one of the best!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 12,
        "title": "BMW M8",
        "created_on": "2023-10-21T21:24:26",
        "text": "M8 is a great car to drive!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 15,
        "title": "Dacia Duster",
        "created_on": "2023-10-21T21:27:26",
        "text": "The best car for the village!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 8,
        "title": "Ferrari",
        "created_on": "2023-10-21T21:20:26",
        "text": "All Ferrari cars are great!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 10,
        "title": "Ferrari F812",
        "created_on": "2023-10-21T21:22:26",
        "text": "F812 Berlinetta has a great sound!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 14,
        "title": "Mercedes AMG GT",
        "created_on": "2023-10-21T21:26:26",
        "text": "AMG GT 63SEperformance WWOOOOW",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 13,
        "title": "Mercedes S 500",
        "created_on": "2023-10-21T21:25:26",
        "text": "W221, a great car!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_ASC_PAGE2 = [
    {
        "id": 21,
        "title": "New Toyota Supra",
        "created_on": "2023-10-21T21:33:26",
        "text": "Toyota/BMW project car",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 19,
        "title": "Pagani",
        "created_on": "2023-10-21T21:31:26",
        "text": "A dream...",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 18,
        "title": "Renault/Mercedes",
        "created_on": "2023-10-21T21:30:26",
        "text": "Renault make engines for Mercedes 180,200 models.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 20,
        "title": "Toyota Land Cruiser",
        "created_on": "2023-10-21T21:32:26",
        "text": "The ultimate SUV",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_PAGE1 = [
    {
        "id": 20,
        "title": "Toyota Land Cruiser",
        "created_on": "2023-10-21T21:32:26",
        "text": "The ultimate SUV",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 18,
        "title": "Renault/Mercedes",
        "created_on": "2023-10-21T21:30:26",
        "text": "Renault make engines for Mercedes 180,200 models.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 19,
        "title": "Pagani",
        "created_on": "2023-10-21T21:31:26",
        "text": "A dream...",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 21,
        "title": "New Toyota Supra",
        "created_on": "2023-10-21T21:33:26",
        "text": "Toyota/BMW project car",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 13,
        "title": "Mercedes S 500",
        "created_on": "2023-10-21T21:25:26",
        "text": "W221, a great car!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 14,
        "title": "Mercedes AMG GT",
        "created_on": "2023-10-21T21:26:26",
        "text": "AMG GT 63SEperformance WWOOOOW",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 10,
        "title": "Ferrari F812",
        "created_on": "2023-10-21T21:22:26",
        "text": "F812 Berlinetta has a great sound!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 8,
        "title": "Ferrari",
        "created_on": "2023-10-21T21:20:26",
        "text": "All Ferrari cars are great!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 15,
        "title": "Dacia Duster",
        "created_on": "2023-10-21T21:27:26",
        "text": "The best car for the village!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 12,
        "title": "BMW M8",
        "created_on": "2023-10-21T21:24:26",
        "text": "M8 is a great car to drive!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

ALL_FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_PAGE2 = [
    {
        "id": 11,
        "title": "BMW E60",
        "created_on": "2023-10-21T21:23:26",
        "text": "E60 one of the best!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 17,
        "title": "BMW B57 Engine",
        "created_on": "2023-10-21T21:29:26",
        "text": "The best diesel engine!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 16,
        "title": "AUDI",
        "created_on": "2023-10-21T21:28:26",
        "text": "Middle brand. Cars are very difficult for repair.",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 9,
        "title": "Alfa Romeo",
        "created_on": "2023-10-21T21:21:26",
        "text": "Julia is one of the pretiest models!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

FAKE_TOPICS_BY_FAKE_CATEGORY_ID1_CARS_DESC_TT_BMW = [
    {
        "id": 12,
        "title": "BMW M8",
        "created_on": "2023-10-21T21:24:26",
        "text": "M8 is a great car to drive!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 11,
        "title": "BMW E60",
        "created_on": "2023-10-21T21:23:26",
        "text": "E60 one of the best!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
    {
        "id": 17,
        "title": "BMW B57 Engine",
        "created_on": "2023-10-21T21:29:26",
        "text": "The best diesel engine!",
        "category_id": 1,
        "author_id": "Kolio",
        "replies": 0,
        "is_locked": False,
    },
]

FAKE_PRIVILEGED_USRS_CAT_ID8 = [
    {"username": "Shahin", "access_level": "write"},
    {"username": "Andrew", "access_level": "read"},
]

FAKE_TOKEN_ADMIN = usrt.generate_fake_access_token(usrt.fake_registered_admin())
FAKE_HEADERS_TOKEN_ADMIN = {"Authorization": f"Bearer {FAKE_TOKEN_ADMIN}"}
FAKE_TOKEN_USER = usrt.generate_fake_access_token(usrt.fake_registered_user())
FAKE_HEADERS_TOKEN_USER = {"Authorization": f"Bearer {FAKE_TOKEN_USER}"}

FAKE_CATEGORY = {
    "id": 17,
    "name": "Cooking",
    "privacy_status": "non_private",
    "access_status": "unlocked",
}
FAKE_CONFLICT_HTTPException = HTTPException(
    status_code=resp.CONFLICT().status_code,
    detail=f"Category with name 'Cooking' already exists!",
)

FAKE_CHANGE_CATEGORY_PRIVACY_TO_PRIVATE_RETURN = (
    "Category '17' changed status to 'private'."
)
NO_CATEGORY_OR_SAME_STATUS = (
    "Category with id '42' doesnt exist or it's status is already private!"
)
SUCCESSFUL_GIVING_READ_ACCESS = "User '5' can now read topics in category '8'."
UNSUCCESSFUL_GIVING_READ_or_WRITE_ACCESS = (
    "Category with id '42' is not private or user with id '35' is not valid user!"
)
SUCCESSFUL_GIVING_WRITE_ACCESS = "User '5' can now write topics in category '8'."
SUCCESSFUL_LOCK_CATEGORY = "Category '6' was locked."
UNSUCCESSFUL_LOCK_CATEGORY = (
    "Category with id '44' doesnt exists or it's already locked!"
)
SUCCESSFUL_REVOKE_USER_ACCESS = (
    "User with id:'6' lost his access to category with id:'8'."
)
UNSUCCESSFUL_REVOKE_USER_ACCESS = (
    "Category with id '44' was not private or user with id '45' didn't have access!"
)

ALL_FAKE_CATEGORIES_PAGE_1_RAW = [
    (10, "Airplanes", datetime.datetime(2023, 10, 21, 21, 36, 59), 1, 1),
    (6, "Boats", datetime.datetime(2023, 10, 21, 18, 46, 10), 0, 0),
    (1, "Cars", datetime.datetime(2023, 10, 21, 18, 41, 51), 0, 0),
    (12, "Clothes", datetime.datetime(2023, 10, 23, 21, 36, 59), 0, 0),
    (13, "Computers", datetime.datetime(2023, 10, 24, 21, 36, 59), 0, 0),
    (17, "Cooking", datetime.datetime(2023, 10, 26, 11, 36, 59), 0, 0),
    (8, "Fishing", datetime.datetime(2023, 10, 21, 18, 49, 2), 1, 1),
    (15, "Hiking", datetime.datetime(2023, 10, 26, 21, 36, 59), 0, 0),
    (9, "Hunting", datetime.datetime(2023, 10, 21, 18, 49, 12), 1, 0),
    (16, "IT Education", datetime.datetime(2023, 10, 26, 10, 0), 0, 0),
]

ALL_FAKE_CATEGORIES_PAGE_1_RESULT = [
    CategoryResponseModel(
        category_name="Airplanes",
        created_on=datetime.datetime(2023, 10, 21, 21, 36, 59),
        privacy_status="private",
    ),
    CategoryResponseModel(
        category_name="Boats",
        created_on=datetime.datetime(2023, 10, 21, 18, 46, 10),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Cars",
        created_on=datetime.datetime(2023, 10, 21, 18, 41, 51),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Clothes",
        created_on=datetime.datetime(2023, 10, 23, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Computers",
        created_on=datetime.datetime(2023, 10, 24, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Cooking",
        created_on=datetime.datetime(2023, 10, 26, 11, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Fishing",
        created_on=datetime.datetime(2023, 10, 21, 18, 49, 2),
        privacy_status="private",
    ),
    CategoryResponseModel(
        category_name="Hiking",
        created_on=datetime.datetime(2023, 10, 26, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Hunting",
        created_on=datetime.datetime(2023, 10, 21, 18, 49, 12),
        privacy_status="private",
    ),
    CategoryResponseModel(
        category_name="IT Education",
        created_on=datetime.datetime(2023, 10, 26, 10, 0),
        privacy_status="non_private",
    ),
]

ALL_FAKE_CATEGORIES_FILTERED_NAME_CAR_RAW = [
    (1, "Cars", datetime.datetime(2023, 10, 21, 18, 41, 51), 0, 0)
]
ALL_FAKE_CATEGORIES_FILTERED_NAME_CAR_RESULT = [
    CategoryResponseModel(
        category_name="Cars",
        created_on=datetime.datetime(2023, 10, 21, 18, 41, 51),
        privacy_status="non_private",
    )
]

ALL_FAKE_CATEGORIES_FILTERED_NAME_BO_RAW = [
    (6, "Boats", datetime.datetime(2023, 10, 21, 18, 46, 10), 0, 0),
    (11, "Jobs", datetime.datetime(2023, 10, 22, 21, 36, 59), 0, 0),
]
ALL_FAKE_CATEGORIES_FILTERED_NAME_BO_RESULT = [
    CategoryResponseModel(
        category_name="Boats",
        created_on=datetime.datetime(2023, 10, 21, 18, 46, 10),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Jobs",
        created_on=datetime.datetime(2023, 10, 22, 21, 36, 59),
        privacy_status="non_private",
    ),
]

ALL_FAKE_CATEGORIES_PAGE_2_RAW = [
    (11, "Jobs", datetime.datetime(2023, 10, 22, 21, 36, 59), 0, 0),
    (7, "Motorcycles", datetime.datetime(2023, 10, 21, 18, 48, 23), 0, 0),
    (14, "Music", datetime.datetime(2023, 10, 25, 21, 36, 59), 0, 0),
]

ALL_FAKE_CATEGORIES_PAGE_2_RESULT = [
    CategoryResponseModel(
        category_name="Jobs",
        created_on=datetime.datetime(2023, 10, 22, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Motorcycles",
        created_on=datetime.datetime(2023, 10, 21, 18, 48, 23),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Music",
        created_on=datetime.datetime(2023, 10, 25, 21, 36, 59),
        privacy_status="non_private",
    ),
]

ALL_FAKE_CATEGORIES_NON_PRIVATE_RAW = [
    (6, "Boats", datetime.datetime(2023, 10, 21, 18, 46, 10), 0, 0),
    (1, "Cars", datetime.datetime(2023, 10, 21, 18, 41, 51), 0, 0),
    (12, "Clothes", datetime.datetime(2023, 10, 23, 21, 36, 59), 0, 0),
    (13, "Computers", datetime.datetime(2023, 10, 24, 21, 36, 59), 0, 0),
    (17, "Cooking", datetime.datetime(2023, 10, 26, 11, 36, 59), 0, 0),
    (15, "Hiking", datetime.datetime(2023, 10, 26, 21, 36, 59), 0, 0),
    (16, "IT Education", datetime.datetime(2023, 10, 26, 10, 0), 0, 0),
    (11, "Jobs", datetime.datetime(2023, 10, 22, 21, 36, 59), 0, 0),
    (7, "Motorcycles", datetime.datetime(2023, 10, 21, 18, 48, 23), 0, 0),
    (14, "Music", datetime.datetime(2023, 10, 25, 21, 36, 59), 0, 0),
]
ALL_FAKE_CATEGORIES_NON_PRIVATE_RESULT = [
    CategoryResponseModel(
        category_name="Boats",
        created_on=datetime.datetime(2023, 10, 21, 18, 46, 10),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Cars",
        created_on=datetime.datetime(2023, 10, 21, 18, 41, 51),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Clothes",
        created_on=datetime.datetime(2023, 10, 23, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Computers",
        created_on=datetime.datetime(2023, 10, 24, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Cooking",
        created_on=datetime.datetime(2023, 10, 26, 11, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Hiking",
        created_on=datetime.datetime(2023, 10, 26, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="IT Education",
        created_on=datetime.datetime(2023, 10, 26, 10, 0),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Jobs",
        created_on=datetime.datetime(2023, 10, 22, 21, 36, 59),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Motorcycles",
        created_on=datetime.datetime(2023, 10, 21, 18, 48, 23),
        privacy_status="non_private",
    ),
    CategoryResponseModel(
        category_name="Music",
        created_on=datetime.datetime(2023, 10, 25, 21, 36, 59),
        privacy_status="non_private",
    ),
]

ALL_FAKE_TOPICS_PAGE_1_RAW = [
    (
        9,
        "Alfa Romeo",
        datetime.datetime(2023, 10, 21, 21, 21, 26),
        "Julia is one of the pretiest models!",
        1,
        2,
        0,
        0,
    ),
    (
        16,
        "AUDI",
        datetime.datetime(2023, 10, 21, 21, 28, 26),
        "Middle brand. Cars are very difficult for repair.",
        1,
        2,
        0,
        0,
    ),
    (
        17,
        "BMW B57 Engine",
        datetime.datetime(2023, 10, 21, 21, 29, 26),
        "The best diesel engine!",
        1,
        2,
        0,
        0,
    ),
    (
        11,
        "BMW E60",
        datetime.datetime(2023, 10, 21, 21, 23, 26),
        "E60 one of the best!",
        1,
        2,
        0,
        0,
    ),
    (
        12,
        "BMW M8",
        datetime.datetime(2023, 10, 21, 21, 24, 26),
        "M8 is a great car to drive!",
        1,
        2,
        0,
        0,
    ),
    (
        15,
        "Dacia Duster",
        datetime.datetime(2023, 10, 21, 21, 27, 26),
        "The best car for the village!",
        1,
        2,
        0,
        0,
    ),
    (
        8,
        "Ferrari",
        datetime.datetime(2023, 10, 21, 21, 20, 26),
        "All Ferrari cars are great!",
        1,
        2,
        0,
        0,
    ),
    (
        10,
        "Ferrari F812",
        datetime.datetime(2023, 10, 21, 21, 22, 26),
        "F812 Berlinetta has a great sound!",
        1,
        2,
        0,
        0,
    ),
    (
        14,
        "Mercedes AMG GT",
        datetime.datetime(2023, 10, 21, 21, 26, 26),
        "AMG GT 63SEperformance WWOOOOW",
        1,
        2,
        0,
        0,
    ),
    (
        13,
        "Mercedes S 500",
        datetime.datetime(2023, 10, 21, 21, 25, 26),
        "W221, a great car!",
        1,
        2,
        0,
        0,
    ),
]
ALL_FAKE_TOPICS_PAGE_1_RESULT = [
    Topic(
        id=9,
        title="Alfa Romeo",
        created_on=datetime.datetime(2023, 10, 21, 21, 21, 26),
        text="Julia is one of the pretiest models!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=16,
        title="AUDI",
        created_on=datetime.datetime(2023, 10, 21, 21, 28, 26),
        text="Middle brand. Cars are very difficult for repair.",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=17,
        title="BMW B57 Engine",
        created_on=datetime.datetime(2023, 10, 21, 21, 29, 26),
        text="The best diesel engine!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=11,
        title="BMW E60",
        created_on=datetime.datetime(2023, 10, 21, 21, 23, 26),
        text="E60 one of the best!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=12,
        title="BMW M8",
        created_on=datetime.datetime(2023, 10, 21, 21, 24, 26),
        text="M8 is a great car to drive!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=15,
        title="Dacia Duster",
        created_on=datetime.datetime(2023, 10, 21, 21, 27, 26),
        text="The best car for the village!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=8,
        title="Ferrari",
        created_on=datetime.datetime(2023, 10, 21, 21, 20, 26),
        text="All Ferrari cars are great!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=10,
        title="Ferrari F812",
        created_on=datetime.datetime(2023, 10, 21, 21, 22, 26),
        text="F812 Berlinetta has a great sound!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=14,
        title="Mercedes AMG GT",
        created_on=datetime.datetime(2023, 10, 21, 21, 26, 26),
        text="AMG GT 63SEperformance WWOOOOW",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=13,
        title="Mercedes S 500",
        created_on=datetime.datetime(2023, 10, 21, 21, 25, 26),
        text="W221, a great car!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
]

ALL_FAKE_TOPICS_PAGE_2_RAW = [
    (
        21,
        "New Toyota Supra",
        datetime.datetime(2023, 10, 21, 21, 33, 26),
        "Toyota/BMW project car",
        1,
        2,
        0,
        0,
    ),
    (
        19,
        "Pagani",
        datetime.datetime(2023, 10, 21, 21, 31, 26),
        "A dream...",
        1,
        2,
        0,
        0,
    ),
    (
        18,
        "Renault/Mercedes",
        datetime.datetime(2023, 10, 21, 21, 30, 26),
        "Renault make engines for Mercedes 180,200 models.",
        1,
        2,
        0,
        0,
    ),
    (
        20,
        "Toyota Land Cruiser",
        datetime.datetime(2023, 10, 21, 21, 32, 26),
        "The ultimate SUV",
        1,
        2,
        0,
        0,
    ),
]
ALL_FAKE_TOPICS_PAGE_2_RESULT = [
    Topic(
        id=21,
        title="New Toyota Supra",
        created_on=datetime.datetime(2023, 10, 21, 21, 33, 26),
        text="Toyota/BMW project car",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=19,
        title="Pagani",
        created_on=datetime.datetime(2023, 10, 21, 21, 31, 26),
        text="A dream...",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=18,
        title="Renault/Mercedes",
        created_on=datetime.datetime(2023, 10, 21, 21, 30, 26),
        text="Renault make engines for Mercedes 180,200 models.",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
    Topic(
        id=20,
        title="Toyota Land Cruiser",
        created_on=datetime.datetime(2023, 10, 21, 21, 32, 26),
        text="The ultimate SUV",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    ),
]

ALL_FAKE_TOPICS_FILTERED_ALFA_RAW = [
    (
        9,
        "Alfa Romeo",
        datetime.datetime(2023, 10, 21, 21, 21, 26),
        "Julia is one of the pretiest models!",
        1,
        2,
        0,
        0,
    )
]
ALL_FAKE_TOPICS_FILTERED_ALFA_RETURN = [
    Topic(
        id=9,
        title="Alfa Romeo",
        created_on=datetime.datetime(2023, 10, 21, 21, 21, 26),
        text="Julia is one of the pretiest models!",
        category_id=1,
        author_id="Kolio",
        replies=0,
        is_locked=False,
    )
]


ALL_FAKE_TOPICS_SORTED_DESC_PAGE_2_RAW = [(11, 'BMW E60', datetime.datetime(2023, 10, 21, 21, 23, 26), 'E60 one of the best!', 1, 2, 0, 0), (17, 'BMW B57 Engine', datetime.datetime(2023, 10, 21, 21, 29, 26), 'The best diesel engine!', 1, 2, 0, 0), (16, 'AUDI', datetime.datetime(2023, 10, 21, 21, 28, 26), 'Middle brand. Cars are very difficult for repair.', 1, 2, 0, 0), (9, 'Alfa Romeo', datetime.datetime(2023, 10, 21, 21, 21, 26), 'Julia is one of the pretiest models!', 1, 2, 0, 0)]
ALL_FAKE_TOPICS_SORTED_DESC_PAGE_2_RESULT = [Topic(id=11, title='BMW E60', created_on=datetime.datetime(2023, 10, 21, 21, 23, 26), text='E60 one of the best!', category_id=1, author_id='Kolio', replies=0, is_locked=False), Topic(id=17, title='BMW B57 Engine', created_on=datetime.datetime(2023, 10, 21, 21, 29, 26), text='The best diesel engine!', category_id=1, author_id='Kolio', replies=0, is_locked=False), Topic(id=16, title='AUDI', created_on=datetime.datetime(2023, 10, 21, 21, 28, 26), text='Middle brand. Cars are very difficult for repair.', category_id=1, author_id='Kolio', replies=0, is_locked=False), Topic(id=9, title='Alfa Romeo', created_on=datetime.datetime(2023, 10, 21, 21, 21, 26), text='Julia is one of the pretiest models!', category_id=1, author_id='Kolio', replies=0, is_locked=False)]
EMPTY_LIST = []
FAKE_LASTROWID = 24
FAKE_CATEGORY_FOR_INSERT = Category(name="Fitness", privacy_status="non_private", access_status="unlocked")
CREATE_CATEGORY_SUCCESSFUL_RETURN = Category(id=24, name='Fitness', created_on=datetime.datetime.now(), privacy_status='non_private', access_status='unlocked')
FAKE_CHANGE_CATEGORY_PRIVACY_RESULT = "Category '17' changed status to 'private'."
FAKE_CHANGE_CATEGORY_PRIVACY_EXCEPTION_STRING = "Category with id '17' doesnt exist or it's status is already private!"
FAKE_GIVE_READ_ACCESS_RETURN = "'User '6' can now read topics in category '9'."
FAKE_GIVE_READ_ACCESS_EXCEPTION_STRING = "Category with id '9' is not private or user with id '6' is not valid user!"
FAKE_GIVE_WRITE_ACCESS_RETURN = "'User '6' can now write topics in category '9'."
FAKE_GIVE_WRITE_ACCESS_EXCEPTION_STRING = "Category with id '9' is not private or user with id '6' is not valid user!"
FAKE_LOCK_CATEGORY_SUCCESSFUL_STRING = "Category '10' was locked."
FAKE_LOCK_CATEGORY_EXCEPTION_STRING = "Category with id '10' doesnt exists or it's already locked!"
FAKE_REVOKE_ACCESS_SUCCESSFUL_STRING = "User with id:'6' lost his access to category with id:'8'."
FAKE_REVOKE_ACCESS_EXCEPTION_STRING = "Category with id '8' was not private or user with id '6' didn't have access!"

FAKE_CATEGORY_PARAMS_FROM_DB_NON_PRIVATE_UNLOCKED = (
    10,
    "Pesho",
    "2023-10-30 09:00:00",
    0,
    0,
)
FAKE_CATEGORY_PARAMS_FROM_DB_PRIVATE_LOCKED = (10, "Pesho", "2023-10-30 09:00:00", 1, 1)
FAKE_TOPIC_PARAMS_FROM_DB_UNLOCKED = (
    11,
    "Razer",
    "2023-10-30 09:05:00",
    "Very good computer products",
    17,
    33,
    0,
    0,
)
FAKE_TOPIC_PARAMS_FROM_DB_LOCKED = (
    11,
    "Razer",
    "2023-10-30 09:05:00",
    "Very good computer products",
    17,
    33,
    1,
    0,
)