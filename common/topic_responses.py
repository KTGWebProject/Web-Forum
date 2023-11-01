import datetime as dt
from models.topic import Topic, TopicResponse

view_all_topics_response = {
    200: {
        'description': 'Successful Response', 
        'content': 
            {'application/json': 
                {'example': [Topic(
                        id=0, 
                        title="string", 
                        created_on=dt.datetime.utcnow(), 
                        text="stringstri", 
                        category_id=0, 
                        author_id=0,
                        replies=[ ],
                        is_locked=False)]}
        }}}

create_topic_response = {
    201: {
        'description': 'Created', 
        'content': 
            {'application/json': 
                {'example': 
                    Topic(
                        id=0, 
                        title="string", 
                        created_on=dt.datetime.utcnow(), 
                        text="stringstri", 
                        category_id=0, 
                        author_id=0,
                        replies=[ ],
                        is_locked=False)}
            }},
    400: {
        'description': 'Bad request', 
        'content': 
            {'application/json': 
                {'example': 'Topic with that name already exists!'}
        }},
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'User has no write access to that category!'}
        }}
}


count_topics_response = {
    200: {
        'description': 'Successful Response', 
        'content': 
            {'application/json': 
                {'example': 0}
        }}
}

view_topic_by_id_response = {
    200: {
        'description': 'Successful Response', 
        'content': 
            {'application/json': 
                {'example': [Topic(
                        id=0, 
                        title="string", 
                        created_on=dt.datetime.utcnow(), 
                        text="stringstri", 
                        category_id=0, 
                        author_id=0,
                        replies=[TopicResponse(
                            content='string', 
                            username='string', 
                            created=dt.datetime.utcnow(),
                            upvotes=0,
                            downvotes=0,
                            is_best=False)],
                        is_locked=False)]}
        }},
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Topic not found!'}
        }}
}

edit_topic_response = {
    201: {
        'description': 'Edited Successfully', 
        'content': 
            {'application/json': 
                {'example': 
                    Topic(
                        id=0, 
                        title="string", 
                        created_on=dt.datetime.utcnow(), 
                        text="stringstri", 
                        category_id=0, 
                        author_id=0,
                        replies=[ ],
                        is_locked=False)}
            }},
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'You are not the author of this topic!'}
        }},
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Topic not found!'}
        }},
    406: 
        {
        'description': 'Locked', 
        'content': 
            {'application/json': 
                {'example': 'The topic is locked and cannot be modified!'}
        }}
}

lock_topic_response = {
    208: {
        'description': 'Already Locked', 
        'content': 
            {'application/json': 
                {'example': 'Topic already locked!'}
        }},
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'You are not admin!'}
        }},
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Topic not found!'}
        }}

}