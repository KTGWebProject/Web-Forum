from fastapi import HTTPException
from data.database import read_query, insert_query, update_query
from models.categories import Category, CategoryResponseModel, PrivilegedUsers
from models.topic import Topic
from models.user import User
from datetime import datetime
import common.responses as responses
from mariadb import _mariadb as mdb

def read_category_params(info):
    id, name, created_on, privacy_status, access_status = info

    if privacy_status == 0:
        privacy_status = "non_private"
    elif privacy_status == 1:
        privacy_status = "private"

    if access_status == 0:
        access_status = "unlocked"
    elif access_status == 1:
        access_status = "locked"

    info = id, name, created_on, privacy_status, access_status

    return info


def read_topic_params(info):
    id_topic, title, created_on, text, id_category, id_author, is_locked, replies, category_name = info

    if is_locked == 0:
        is_locked = "unlocked"
    elif is_locked == 1:
        is_locked = "locked"

    author_name = find_user_by_id(id_author)

    info = (
        id_topic,
        title,
        created_on,
        text,
        id_category,
        category_name,
        author_name,
        replies,
        is_locked,
    )

    return info


def convert_status(status: int | str):
    if isinstance(status, str):
        if status == "private":
            status = 1
        elif status == "non_private":
            status = 0
    elif isinstance(status, int):
        if status == 1:
            status = "private"
        elif status == 0:
            status = "non_private"
    return status

def convert_read_write_access(data):
    if isinstance(data, str):
        if data == "write":
            data = 1
        elif data == "read":
            data = 0
    elif isinstance(data, int):
        if data == 1:
            data = "write"
        elif data == 0:
            data = "read"
    return data
    
def find_user_by_id(id): 
    query_data = read_query("SELECT username FROM users where id_user = ?", (id,))
    author_name = (next((name for name in query_data), None))[0]

    return author_name


def get_all_categories(user: User = None, name_filter: str | None = None, page = int) -> list[Category] | None:
    query = None
    params = []
    if user:
        if user.is_admin == 1:
            query = """SELECT * FROM categories c"""
            
            if name_filter:
                query += " WHERE c.name LIKE ?"
                params.append(f"%{name_filter.lower()}%")
        else:
            query = """SELECT c.id_category, c.name, c.created_on, c.is_private, c.is_locked
                    FROM categories c
                    LEFT JOIN private_categories pc ON c.id_category = pc.categories_id_category
                    WHERE (pc.users_id_user = ? or c.is_private = 0)"""
            params.append(user.id)

            if name_filter:
                query += " AND c.name LIKE ?"
                params.append(f"%{name_filter.lower()}%")

    else:
        query = """SELECT c.id_category, c.name, c.created_on, c.is_private, c.is_locked
                FROM categories c
                WHERE c.is_private = 0"""

        if name_filter:
            query += " AND c.name LIKE ?"
            params.append(f"%{name_filter.lower()}%")

    query += ''' ORDER BY c.name ASC
                 LIMIT 10 OFFSET ?0'''
    params.append(page - 1)
    
    all_categories = [
        Category.from_query_result(*read_category_params(row))
        for row in read_query(query, tuple(params))
    ]

    return [
        CategoryResponseModel(
            category_id=cat.id,
            category_name=cat.name,
            created_on=cat.created_on,
            privacy_status=cat.privacy_status,
        )
        for cat in all_categories
    ]

def get_topics_by_cat_id(cat_id: int, user: User = None, title: str = None, sorting: str = None, page: int = 1):
    query = None
    params = None
    if user:
        if user.is_admin:
            query = ''' WITH category AS (SELECT * FROM categories c LEFT JOIN private_categories pc ON c.id_category = pc.categories_id_category
                        WHERE c.id_category = ?),
                        replies_count AS (SELECT topics_id_topic, COUNT(*) as replies_count FROM replies GROUP BY topics_id_topic)
                        SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, t.id_author, t.is_locked, COALESCE(rc.replies_count, 0) as replies_count, c.name
                        FROM topics t
                        JOIN category c ON t.id_category = c.id_category
                        LEFT JOIN replies_count rc ON t.id_topic = rc.topics_id_topic'''
            params = [cat_id]

            if title:
                query += " AND t.title LIKE ?"
                params.append(f"%{title}%")

        else:
            query = ''' WITH category AS (SELECT * FROM categories c
                        LEFT JOIN private_categories pc ON c.id_category = pc.categories_id_category
                        WHERE (pc.users_id_user = ? OR c.is_private = 0) AND c.id_category = ?),
                        replies_count AS (SELECT topics_id_topic, COUNT(*) as replies_count
                        FROM replies
                        GROUP BY topics_id_topic)
                        SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, t.id_author, t.is_locked, COALESCE(rc.replies_count, 0) as replies_count, c.name
                        FROM topics t
                        JOIN category c ON t.id_category = c.id_category
                        LEFT JOIN replies_count rc ON t.id_topic = rc.topics_id_topic'''

            params = [user.id, cat_id]
            
            if title:
                query += " WHERE t.title LIKE ?"
                params.append(f"%{title}%")
    else:
        query = ''' WITH category AS (SELECT id_category, name, created_on, is_private, is_locked
                    FROM categories WHERE is_private = 0 AND id_category = ?),
                    replies_count AS (SELECT topics_id_topic, COUNT(*) as replies_count 
                    FROM replies 
                    GROUP BY topics_id_topic)
                    SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, t.id_author, t.is_locked, COALESCE(rc.replies_count, 0) as replies_count, c.name
                    FROM topics t
                    JOIN category c ON t.id_category = c.id_category
                    LEFT JOIN replies_count rc ON t.id_topic = rc.topics_id_topic'''
        params = [cat_id]

        if title:
            query += " WHERE t.title LIKE ?"
            params.append(f"%{title}%")

    if sorting.upper() == "DESC":
        query += " ORDER BY t.title DESC"
    elif sorting == None or sorting.upper() == "ASC":
        query += " ORDER BY t.title ASC"

    query += " LIMIT 10 OFFSET ?0"
    params.append(page - 1)

    topics = [Topic.cat_from_query_result(*(read_topic_params(row)))for row in read_query(query, tuple(params))]

    return topics

def get_privileged_users(cat_id: int):
    query = ''' SELECT u.username, pc.has_write_access
                FROM users u
                JOIN private_categories pc ON u.id_user = pc.users_id_user
                JOIN categories c ON pc.categories_id_category = c.id_category
                WHERE c.id_category = ?'''
    params = [cat_id]
    
    privileged_users = [PrivilegedUsers.from_query_result(user[0], convert_read_write_access(user[1])) for user in read_query(query, tuple(params))]

    return privileged_users
    

def create_new_category(category: Category, user_id: int):
    query = "INSERT INTO categories (name, created_on, is_private, is_locked) VALUES (?, ?, ?, ?)"
    params = [category.name, datetime.utcnow()]

    if category.privacy_status == "private":
        params.append(1)
    else:
        params.append(0)
    if category.access_status == "locked":
        params.append(1)
    else:
        params.append(0)

    try:
        category.id = insert_query(query, tuple(params))
    except mdb.IntegrityError as i:
        raise HTTPException(status_code=responses.CONFLICT().status_code,detail=f"Category with name '{category.name}' already exists!",)

    category.created_on = params[1]

    if category.privacy_status == "private":
        insert_query(
            "INSERT INTO private_categories (categories_id_category, users_id_user, has_write_access) VALUES(?, ?, ?)",
            (category.id, user_id, 1),
        )

    return category


def change_category_privacy(cat_id: int, privacy_status: str):
    new_status = convert_status(privacy_status)
    query = """UPDATE categories SET is_private = ? WHERE id_category = ?"""
    params = [new_status, cat_id]

    query_result = update_query(query, tuple(params))

    if query_result == 0:
        raise HTTPException(
            status_code=responses.NotFound().status_code,
            detail=f"Category with id '{cat_id}' doesnt exist or it's status is already private!",
        )

    else:
        query = """DELETE FROM private_categories 
                WHERE categories_id_category = ?"""
        param = [cat_id,]
        update_query(query, tuple(param))

    return responses.OK(
        content=f"Category '{cat_id}' changed status to '{privacy_status}'."
    )


def give_read_access_to_user(user_id: int, cat_id: int):
    query = """INSERT INTO private_categories (categories_id_category, users_id_user, has_write_access)
                VALUES (?, ?, 0)
                ON DUPLICATE KEY UPDATE has_write_access = 0"""

    params = [cat_id, user_id]

    query_result = update_query(query, tuple(params))
    
    if query_result == 0:
        raise HTTPException(
            status_code=responses.NotFound().status_code,
            detail=f"Category with id '{cat_id}' is not private or user with id '{user_id}' is not valid user!",
        )
    else:
        return responses.OK(
            content=f"'User '{user_id}' can now read topics in category '{cat_id}'."
        )


def give_write_access_to_user(user_id: int, cat_id: int):
    query = """INSERT INTO private_categories (categories_id_category, users_id_user, has_write_access)
                VALUES (?, ?, 1)
                ON DUPLICATE KEY UPDATE has_write_access = 1"""

    params = [cat_id, user_id]

    query_result = update_query(query, tuple(params))

    if query_result == 0:
        raise HTTPException(
            status_code=responses.NotFound().status_code,
            detail=f"Category with id '{cat_id}' is not private or user with id '{user_id}' is not valid user!",
        )
    
    else:
        return responses.OK(
        content=f"'User '{user_id}' can now write topics in category '{cat_id}'."
    )

def lock_category_by_id(cat_id: int):
    query = ''' UPDATE categories
                SET is_locked = 1
                WHERE id_category = ?'''
    params = [cat_id]

    query_result = update_query(query, tuple(params))

    if query_result == 0:
        raise HTTPException(
            status_code=responses.NotFound().status_code,
            detail=f"Category with id '{cat_id}' doesnt exists or it's already locked!",
        )
    else:
        return responses.OK(content=f"Category '{cat_id}' was locked.")


def revoke_access(user_id: int, cat_id: int):
    query = """ DELETE FROM private_categories 
                WHERE categories_id_category = ? 
                AND users_id_user = ?"""

    params = [cat_id, user_id]

    query_result = update_query(query, params)
    
    if query_result == 0:
        raise HTTPException(
            status_code=responses.NotFound().status_code,
            detail=f"Category with id '{cat_id}' was not private or user with id '{user_id}' didn't have access!",
        )
    else:
        return responses.OK(content=f"User with id:'{user_id}' lost his access to category with id:'{cat_id}'.")
