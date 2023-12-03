from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def confirm_user_pass(name, password):
    result = db.session.execute(text("SELECT passwords FROM users WHERE names=:name AND deleted=FALSE"), {"name":name})
    user_pass = result.fetchone()
    if user_pass == None:
        return False
    return check_password_hash(user_pass[0], password)

def get_areas():
    result = db.session.execute(text("SELECT id, names FROM areas WHERE deleted=FALSE"))
    return result.fetchall()

def get_area_by_id(id):
    result = db.session.execute(text("SELECT id, names FROM areas WHERE id=:id AND deleted=FALSE"), {"id": id})
    return result.fetchone()

def get_area_by_name(name):
    result = db.session.execute(text("SELECT id, names FROM areas WHERE names=:name AND deleted=FALSE"), {"name": name})
    return result.fetchone()

def get_discussions_by_area(name):
    result = db.session.execute(text("SELECT id, names, area, starter, created_at FROM discussions WHERE area=:name AND deleted=FALSE"), {"name": name})
    return result.fetchall()

def get_discussion_by_id(id):
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE id=:id AND deleted=FALSE"), {"id": id})
    return result.fetchone()

def get_discussion_by_writer(name):
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE starter=:name AND deleted=FALSE ORDER BY created_at"), {"name":name})
    return result.fetchall()

def get_discussion_by_name(name):
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE names=:name AND deleted=FALSE"), {"name": name})
    return result.fetchone()

def get_discussion_by_search(query, id1):
    result = db.session.execute(text("SELECT discussion FROM messages WHERE content LIKE :query AND deleted=FALSE"), {"query":"%"+query+"%"})
    dsc_names = result.fetchall()
    from_msg = []
    for discussion in dsc_names:
        from_msg.append(get_discussion_by_name(discussion[0]))
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE names LIKE :query AND deleted=FALSE"), {"query":"%"+query+"%"})
    from_dsc = result.fetchall()
    for discussion in from_dsc:
        if discussion not in from_msg:
            from_msg.append(discussion)
    if id1 != None:
        area = get_area_by_id(id1)
        final = []
        for discussion in from_msg:
            if discussion.area == area.names:
                final.append(discussion)
    else:
        final = from_msg
    return final

def get_message_by_search(query, id2):
    discussion = get_discussion_by_id(id2)
    result = db.session.execute(text("SELECT id, writer, discussion, content, created_at FROM messages WHERE content LIKE :query AND discussion=:name AND deleted=FALSE"), {"query":"%"+query+"%", "name":discussion.names})
    return result.fetchall()

def get_messages_from_discussion(name):
    result = db.session.execute(text("SELECT id, writer, discussion, content, created_at, deleted FROM messages WHERE discussion=:name AND deleted=FALSE ORDER BY created_at DESC"), {"name": name})
    messages = result.fetchall()
    for message in messages:
        if not check_user_exist(message.writer):
            message = [message.id, "", message.discussion, message.content, message.created_at]
        if message.deleted == True:
            message = [message.id, "", message.discussion, "Deleted", message.created_at]
    return messages

def get_message_by_id(id):
    result = db.session.execute(text("SELECT id, writer, discussion, content, created_at from messages WHERE id=:id AND deleted=FALSE"), {"id":id})
    return result.fetchone()

def get_friends_by_user(name):
    result = db.session.execute(text("SELECT F1.user2 FROM friendlist F1,friendlist F2 WHERE F1.user1=:name AND F1.user1=F2.user2 AND F1.user2=F2.user1 AND F2.deleted=FALSE AND F1.deleted=FALSE"), {"name":name})
    return result.fetchall()

def get_friend_requests(name):
    requests = []
    result = db.session.execute(text("SELECT user1 FROM friendlist WHERE user2=:name AND deleted=FALSE"), {"name":name})
    potential = result.fetchall()
    friends = get_friends_by_user(name)
    for user in potential:
        if user not in friends:
            requests.append(user)
    return requests

def check_friend(user1, user2):
    result = db.session.execute(text("SELECT * FROM friendlist F1, friendlist F2 WHERE F1.user1=:user1 AND F1.user1=F2.user2 AND F1.user2=:user2 AND F1.user2=F2.user1 AND F1.deleted=FALSE AND F2.deleted=FALSE"), {"user1":user1, "user2":user2})
    if result.fetchone() == None:
        return False
    return True

def get_directmessages(user1, user2):
    result = db.session.execute(text("SELECT id, user1, user2, content, created_at FROM directmessages WHERE ((user1=:user1 AND user2=:user2) OR (user1=:user2 AND user2=:user1)) AND deleted=FALSE ORDER BY created_at DESC"), {"user1":user1, "user2":user2})
    return result.fetchall()

def get_directmessage_by_search(user1, user2, query):
    result = db.session.execute(text("SELECT id, user1, user2, content, created_at FROM directmessages WHERE (user1=:user1 AND user2=:user2 AND content LIKE :query AND deleted=FALSE) OR (user1=:user2 AND user2=:user1 AND content LIKE :query AND deleted=FALSE) ORDER BY created_at DESC"), {"query":"%"+query+"%", "user1":user1, "user2":user2})
    return result.fetchall()

def get_directmessage_by_id(id):
    result = db.session.execute(text("SELECT id, user1 from directmessages WHERE id=:id AND deleted=FALSE"), {"id":id})
    return result.fetchone()

def is_admin(name):
    result = db.session.execute(text("SELECT admins FROM users WHERE names=:name AND deleted=FALSE"), {"name":name})
    is_admin = result.fetchone()
    if is_admin == None:
        return False
    return is_admin[0]

def check_user_exist(name):
    result = db.session.execute(text("SELECT * FROM users WHERE names=:name AND deleted=FALSE"), {"name":name})
    if result.fetchone() == None:
        return False
    return True