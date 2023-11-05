from data.database import read_query, insert_query, update_query
from models.topic import Topic, TopicResponse
from models.user import User
from models.reply import Reply


def view_all_topics(
        search_in_title: [str],
        include_topics: bool = True,
        include_replies: bool = True,
        sort_by_date: bool = False,
        paginated: bool = True,
        user: User | None = None,
        default_page: int = 1
        ) -> list[Topic|Reply] | list:
    data = []
    params = [f'%{x}%' for x in search_in_title] if search_in_title else []

    if user and user.is_admin:
        topics_query =  '''SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, 
                        (select username from users where id_user = t.id_author) as id_author,
                        (SELECT count(*) from replies WHERE topics_id_topic = t.id_topic) as replies, t.is_locked 
                        FROM topics t 
                        '''
        replies_query = '''SELECT * FROM replies '''
    
        if search_in_title:
            topics_query += 'WHERE'
            replies_query += 'WHERE'
        topics_query += ' or '.join(" t.title like ?" for _ in search_in_title)
        replies_query += ' or '.join(" content like ?" for _ in search_in_title)
        
        if sort_by_date:
            topics_query += 'ORDER BY created_on DESC'
            replies_query += 'ORDER BY created_on DESC'

        if paginated:
            topics_query += ' LIMIT 10 OFFSET ?0'
            replies_query += ' LIMIT 10 OFFSET ?0'
            params.append(default_page - 1)
    
        if include_topics: 
            data.extend([Topic.from_query_result(*row) for row in read_query(topics_query, tuple(params))])
        if include_replies: 
            data.extend([Reply.from_query_result(*row) for row in read_query(replies_query, tuple(params))])
        
        return data
    else:
        if not search_in_title:
            search_in_title = ['']
        topic_params = []
        reply_params = []
        topic_params.extend([' AND ' + ' or '.join(f' t.title like "%{x}%"' for x in search_in_title),
                            user if user else 'NULL',
                            ' AND ' + ' or '.join(f' t.title like "%{x}%"' for x in search_in_title)
                            ])
        reply_params.extend([' AND ' + ' or '.join(f" content like '%{x}%'" for x in search_in_title),
                            user if user else 'NULL',
                            ' AND ' + ' or '.join(f" content like '%{x}%'" for x in search_in_title)
                            ])
        topics_query =  f'''
            (SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, 
            (select username from users where id_user = t.id_author) as id_author,
            (SELECT count(*) FROM replies WHERE topics_id_topic = t.id_topic) AS replies, t.is_locked 
            FROM topics t where (t.id_category) NOT IN (SELECT categories_id_category FROM private_categories)
            {topic_params[0]} )
            UNION 
            (SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, 
            (select username from users where id_user = t.id_author) as id_author,
            (SELECT count(*) FROM replies WHERE topics_id_topic = t.id_topic) AS replies, t.is_locked 
            FROM topics t WHERE (t.id_category, {topic_params[1]}) IN (SELECT categories_id_category, users_id_user FROM private_categories)
            {topic_params[2]} )
            '''
        replies_query = f'''
            (SELECT r.id_reply, r.content, r.topics_id_topic, r.users_id_user, r.created_on, r.is_best FROM replies r 
            JOIN topics t ON t.id_topic = r.topics_id_topic
            WHERE (t.id_category) NOT IN (SELECT categories_id_category FROM private_categories) 
            {reply_params[0]} )
            UNION
            (SELECT r.id_reply, r.content, r.topics_id_topic, r.users_id_user, r.created_on, r.is_best FROM replies r 
            JOIN topics t ON t.id_topic = r.topics_id_topic
            WHERE (t.id_category, {reply_params[1]}) IN (SELECT categories_id_category, users_id_user FROM private_categories) 
            {reply_params[2]} )'''

        if sort_by_date:
            topics_query += 'ORDER BY created_on DESC'
            replies_query += 'ORDER BY created_on DESC'
    
        if paginated:
            topics_query += (f' LIMIT 10 OFFSET {default_page - 1}0')
            replies_query += (f' LIMIT 10 OFFSET {default_page - 1}0')
    

        if include_topics: 
            data.extend([Topic.from_query_result(*row) for row in read_query(topics_query)])
        if include_replies: 
            data.extend([Reply.from_query_result(*row) for row in read_query(replies_query)])

        return data

def get_topic_by_id(id: int) -> Topic | None:
    data = read_query(
                '''SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, t.id_author, NULL AS replies, t.is_locked 
                FROM topics t 
                WHERE t.id_topic = ?;''',
                (id,)
                )
    topic = next((Topic.from_query_result(*row) for row in data), None)

    if topic:
        topic = get_topic_replies(topic)
        return topic
    return None

def get_topic_replies(topic: Topic) -> Topic:
    replies = read_query('''
                SELECT r.content AS Reply, u.username AS User, r.created_on AS 'Post date', 
                (SELECT count(*) FROM votes v WHERE v.replies_id_reply = r.id_reply AND v.is_upvote=1) AS Upvotes, 
                (SELECT count(*) FROM votes dv WHERE dv.replies_id_reply = r.id_reply AND dv.is_upvote=-1) AS Downvotes,
                r.is_best AS 'Best Reply', r.id_reply, r.topics_id_topic
                FROM replies r
                JOIN users u ON u.id_user = r.users_id_user
                WHERE r.topics_id_topic = ?''',
                (topic.id,)
                )        
    topic.replies = [TopicResponse.replies_from_query_results(*row) for row in replies]
    return topic

def topic_is_in_a_private_category(topic: Topic):
    '''check topic's category status'''
    result = read_query('''SELECT categories_id_category
                        FROM private_categories 
                        WHERE categories_id_category = ?''', (topic.category_id,))
    
    return next(((row) for row in result), None)

def user_has_write_access(topic: Topic, user: User):
    '''check if the user has write access if a category is private'''
    result = read_query('''
                        SELECT categories_id_category, users_id_user, has_write_access 
                        FROM private_categories 
                        WHERE categories_id_category = ? AND users_id_user = ?''',
                        (topic.category_id, user.id))
    if result and result[0][-1] == 1:
        return True
    return False

def create_topic(topic: Topic) -> Topic: 
    topic.id = insert_query('''
                INSERT INTO topics (title, created_on, text, id_category, id_author, is_locked) 
                VALUES (?, ?, ?, ?, ?, ?)''', 
                (topic.title, topic.created_on, topic.text, topic.category_id, topic.author_id, topic.is_locked)
                )
    return Topic.from_query_result(
            topic.id, 
            topic.title,
            topic.created_on,
            topic.text, 
            topic.category_id,
            topic.author_id,
            topic.replies,
            topic.is_locked
            )

def edit_topic(
        topic: Topic, 
        new_title: str | None = None, 
        new_text: str | None = None
    ) -> Topic:
    if not new_title:
        new_title = topic.title
    if not new_text:
        new_text = topic.text

    update_query('update topics set title = ?, text = ?  where title LIKE ?;',
                     (new_title, new_text, topic.title))
    
    topic.title, topic.text = new_title, new_text 

    return topic

def lock_topic(id: int) -> bool:
    result = update_query('UPDATE topics SET is_locked = 1 where id_topic = ?;', (id, ))

    return result == 0

def _count_topics(category_id: int):

    return next((el for el in read_query('SELECT count(*) FROM topics WHERE id_category = ?',
                (category_id,))), 0)