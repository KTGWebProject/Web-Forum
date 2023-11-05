from data.database import read_query, insert_query, update_query
from models.reply import Reply
from models.topic import Topic
from models.user import User


def create_reply(reply: Reply) -> Reply:
    reply.id = insert_query('''insert into replies(content, topics_id_topic, users_id_user, created_on, is_best) 
                    select ?, ?, ?, ?, ?
                    from topics 
                    where id_topic = ? and is_locked = 0;''', 
                    (reply.content, reply.topic_id, reply.user_id, reply.created_on, reply.is_best, 
                     reply.topic_id)
                     )
    return reply

def get_reply_by_id(topic_id: int, reply_id: int) -> Reply:
    result = read_query('SELECT * FROM replies WHERE topics_id_topic = ? and id_reply = ?;',
                        (topic_id, reply_id)
                        )
    reply = next((Reply.from_query_result(*el) for el in result), None)
    if reply: reply.upvotes, reply.downvotes = _count_votes(reply.id)
    
    return  reply

def topic_is_locked(reply_id) -> bool:
    result = read_query(''' SELECT is_locked FROM topics  WHERE id_topic = ?;''', (reply_id, ))
    return result[0][0] == 1

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


def edit_reply(reply: Reply, new_content: str) -> bool:
    result = update_query('UPDATE replies SET content = ? WHERE id_reply = ?;',
                          (new_content, reply.id)
                          )
    return result == 1

def topic_exists(topic_id) -> Topic:
    result = read_query('''SELECT t.id_topic, t.title, t.created_on, t.text, t.id_category, t.id_author,
            (SELECT count(*) from replies WHERE topics_id_topic = t.id_topic) as replies, t.is_locked 
            FROM topics t WHERE t.id_topic = ?''', 
            (topic_id,)
            )
    return next((Topic.from_query_result(*el) for el in result), None)

def topic_has_best_reply(topic: Topic) -> bool:
    result = read_query('select count(*) from replies where is_best=1 and topics_id_topic=?',
                        (topic.id,)
                        )[0]
    return result[0] == 1

def choose_best(reply: Reply, topic_id: int) -> Reply:
    result = update_query('UPDATE replies SET is_best=1 WHERE id_reply=? and topics_id_topic =?;', 
                          (reply.id, topic_id)
                          )
    return reply if result == 1 else None

def check_user_vote_for_reply(user_id: int, reply: Reply, vote:int):
    result = next((el[0] for el in read_query(
        'SELECT is_upvote FROM ktg_forum_api.votes WHERE users_id_user=? and replies_id_reply=?;',
        (user_id, reply.id))), None)

    if not result and vote == 0:
        return
    if not result:
        return new_vote(user_id, reply, vote)
    if result in (1, -1) and vote == 0:
        return remove_vote(reply, user_id)
    if result in (1, -1) and vote in (1, -1):
        return update_vote(user_id, reply, vote)

def new_vote(user_id: int, reply: Reply, vote: int):
    result = insert_query(
        'insert into votes (replies_id_reply, users_id_user, is_upvote) values (?, ?, ?);',
        (reply.id, user_id, vote)
        )
    return _count_votes(reply.id)

def update_vote(user_id: int, reply: Reply, vote: int):
    result = update_query('update votes set is_upvote = ? where replies_id_reply = ? and users_id_user = ?;',
                          (vote, reply.id, user_id)
                          )
    return _count_votes(reply.id)

def remove_vote(reply: Reply, user_id: int):
    result = update_query('delete from votes where replies_id_reply = ? and users_id_user = ?;',
                           (reply.id, user_id)
                           )
    return _count_votes(reply.id)

def _count_votes(reply_id: int):
    result = next((el for el in read_query('''SELECT count(v.is_upvote) AS Upvotes, 
                            (SELECT count(dv.is_upvote) 
                            FROM votes dv WHERE dv.replies_id_reply=? AND dv.is_upvote = -1) AS Downvotes
                            FROM  votes v WHERE v.replies_id_reply=? AND v.is_upvote = 1;''',
                            (reply_id, reply_id))), None)
    return result