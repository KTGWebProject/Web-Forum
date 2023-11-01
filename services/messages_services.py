from datetime import datetime
from data.database import read_query, insert_query
from models.message import Message, MessageResponseModelConversation, MessageResponseModelChat
from fastapi import HTTPException, status
from common import responses



async def get_messages(user_id: int, sort: bool, paginated: bool, page:int):
    conversations_with = read_query(
        '''select distinct m.id_author, u.id_recipient 
        from messages m 
        join users_has_messages u on m.id_message = u.id_message 
        join users us on u.id_recipient = us.id_user 
        where m.id_author = ? or u.id_recipient = ?''',
        (user_id, user_id))
    
    counterparties =[]
    for party in conversations_with:
        author_id, recipient_id = party
        if author_id != user_id:
            counterparties.append(author_id)
        if recipient_id != user_id:
            counterparties.append(recipient_id)
    clean_counterparties = set(counterparties)
    sql_query = '''select m.id_message, us1.username, us.username, m.subject, m.content, m.created_on, m.id_parent_message
        from messages m join users_has_messages u on m.id_message = u.id_message 
        join users us1 on m.id_author = us1.id_user 
        join users us on u.id_recipient = us.id_user 
        where (m.id_author = ? and u.id_recipient = ?) or 
        (m.id_author = ? and u.id_recipient = ?) order by m.id_message'''
    
    if sort:
        sql_query += ' Desc'
    
    if paginated:
        sql_query += ' LIMIT 10 OFFSET ?0'
    
    conversations = []
    for counterparty in clean_counterparties:
        params = [user_id, counterparty, counterparty, user_id]
        if paginated:
            params.append(page-1)
        conversations.append([MessageResponseModelConversation.get_response(*row) for row in
                              read_query(sql_query, tuple(params))])
    
    return conversations
        
async def get_messages_user(**kwargs):
    user_id = kwargs.pop("user_id")
    paginated = kwargs.pop("paginated") 
    sort = kwargs.pop("sort")
    page = kwargs.pop("page") 
    full_conversations = []
    for value in kwargs.values():
        find_subjects = '''select distinct m.subject 
            from messages m join users_has_messages u on m.id_message = u.id_message 
            join users us1 on m.id_author = us1.id_user 
            join users us on u.id_recipient = us.id_user 
            where (m.id_author = ? and us.username = ?) or (us1.username = ? and u.id_recipient = ?) 
            '''     
    
        subjects = read_query(find_subjects, (user_id, value, value, user_id)) 
        
            
        second_sql_query = '''select m.id_message, us1.username, us.username, m.subject, m.content, m.created_on, m.id_parent_message 
            from messages m join users_has_messages u on m.id_message = u.id_message 
            join users us1 on m.id_author = us1.id_user 
            join users us on u.id_recipient = us.id_user 
            where m.subject=? and ((m.id_author = ? and us.username = ?) or (us1.username = ? and u.id_recipient = ?))  
            order by m.id_message'''
        
        if sort:
            second_sql_query += ' Desc'
        
        if paginated:
            limit = 3
            offset = limit*(page - 1)
            second_sql_query += f' LIMIT {limit} OFFSET {offset}'
        
        conversations = []
        
        params = [user_id, value, value, user_id]
        for subject in subjects:
            final_params = [subject[0]]
            final_params.extend(params)    
            conversations.append([MessageResponseModelConversation.get_response(*row) for row in
                                read_query(second_sql_query, tuple(final_params))])
        
        full_conversations.append(conversations)
    return full_conversations   

async def get_chat_service(user_id: int, since:datetime):
    sql_query = '''select m.id_message, us.username, m.subject, m.content, m.created_on, m.id_parent_message 
        from messages m 
        join users_has_messages u on m.id_message = u.id_message 
        join users us on m.id_author = us.id_user 
        where m.created_on >=? and u.id_recipient =?'''
    
    return [MessageResponseModelChat.get_response_chat(*row) 
            for row in read_query(sql_query,(datetime.strptime(str(since), "%Y-%m-%d %H:%M:%S"), user_id))]
        
        
async def post_message(user_id: int, message: Message, recipients: set[str]):
    usernames_lst = sorted(list(recipients))
    find_user_ids_sql_query = '''select id_user 
        from users 
        where username = ?'''
    if len(usernames_lst)>1:
        find_user_ids_sql_query += ' or username = ?'*(len(usernames_lst) -1)    
   
    counterparties = read_query(find_user_ids_sql_query, tuple(usernames_lst))     
    if not counterparties:
        raise HTTPException(responses.NotFound().status_code, detail="No such user(s)") 
    if message.id_parent_message is not None:
        reply_to_check = read_query('select id_message from messages where id_message=?',(message.id_parent_message,))
    else:
        reply_to_check = None
    if not message.created_on:
        created_on = datetime.utcnow()
    else:
        created_on = message.created_on
    if not reply_to_check:
        sql_insert_message='''insert into messages(content, created_on, subject, id_author) values(?,?,?,?)'''
        sql_params =(message.content, created_on, message.subject, user_id)
    else:
        sql_insert_message='''insert into messages(content, created_on, subject, id_parent_message, id_author) values(?,?,?,?,?)'''
        sql_params =(message.content, created_on, message.subject, message.id_parent_message, user_id)
    message_id = insert_query(sql_insert_message, sql_params)
    
    for counterparty in counterparties:
        insert_query('insert into users_has_messages (id_recipient, id_message) values(?,?)', (counterparty[0], message_id))
    return message_id

    
    
    
    
        