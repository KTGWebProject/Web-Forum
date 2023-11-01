import datetime as dt
from models.topic import Topic
from models.reply import Reply

create_reply_response = {
    201: {
        'description': 'Created', 
        'content': 
            {'application/json': 
                {'example': 
                    Reply(
                        id = 0, 
                        content = "string", 
                        topic_id = 0, 
                        user_id = 0,
                        created_on = dt.datetime.utcnow(),
                        is_best = False, 
                        upvotes = 0,
                        downvotes = 0)}
            }},
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'User has no write access to that category!'}
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


choose_best_reply_response = {
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'You are not the author of this topic!'}
        }}
    ,
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Topic/Reply not found!'}
        }},
    406: 
        {
        'description': 'Best Reply Exists', 
        'content': 
            {'application/json': 
                {'example': 'This topic already has a best reply!'}
        }},
    500: 
        {
        'description': 'Internal Server Error', 
        'content': 
            {'application/json': 
                {'example': 'Oops, something went wrong...!'}
        }}
}

vote_response = {
    200: {
        'description': 'Successful', 
        'content': 
            {'application/json': 
                {'example': 'No vote to remove'}
        }},
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Reply not found!'}
        }}
}

edit_reply_response = {
    403: {
        'description': 'Forbidden', 
        'content': 
            {'application/json': 
                {'example': 'You are not the author of this reply!'}
        }}
    ,
    404: {
        'description': 'Not Found', 
        'content': 
            {'application/json': 
                {'example': 'Topic/Reply not found!'}
        }},
    500: 
        {
        'description': 'Internal Server Error', 
        'content': 
            {'application/json': 
                {'example': 'Oops, something went wrong...!'}
        }}
    
}