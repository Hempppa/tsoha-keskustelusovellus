from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def add_area(name):
    db.session.execute(text("INSERT INTO areas (names, deleted) VALUES (:name, FALSE)"), {"name":name})
    db.session.commit()

def add_discussion(name, area, writer):
    db.session.execute(text("INSERT INTO discussions (names, area, starter, created_at, deleted) VALUES (:name, :area, :writer, NOW(), FALSE)"), {"name":name, "area": area, "writer":writer})
    db.session.commit()

def add_message(writer, content, discussion):
    db.session.execute(text("INSERT INTO messages (writer, discussion, content, created_at, deleted) VALUES (:writer, :discussion, :content, NOW(), FALSE)"), {"writer":writer, "discussion":discussion, "content":content,})
    db.session.commit()

def add_user(user, password):
    new_pass = generate_password_hash(password)
    try:
        db.session.execute(text("INSERT INTO users (names, passwords, admins, deleted) VALUES (:name, :password, FALSE, FALSE)"), {"name":user, "password":new_pass})
        db.session.commit()
        return True
    except:
        return False

def change_user_pass(user, password):
    new_pass = generate_password_hash(password)
    db.session.execute(text("UPDATE users SET passwords=:password WHERE names=:name"), {"name":user, "password":new_pass})
    db.session.commit()

def make_admin(user):
    db.session.execute(text("UPDATE users SET admins=TRUE WHERE names=:name"), {"name":user})
    db.session.commit()

def add_friend(user1, user2):
    result = db.session.execute(text("SELECT * FROM friendlist WHERE user1=:user1 AND user2=:user2"), {"user1":user1, "user2":user2})
    if result.fetchone() == None:
        db.session.execute(text("INSERT INTO friendlist (user1, user2, deleted) VALUES (:user1, :user2, FALSE)"), {"user1":user1, "user2":user2})
    else:
        db.session.execute(text("UPDATE friendlist SET deleted=FALSE WHERE user1=:user1 AND user2=:user2"), {"user1":user1, "user2":user2})
    db.session.commit()

def remove_friend(user1, user2):
    db.session.execute(text("UPDATE friendlist SET deleted=TRUE WHERE (user1=:name1 AND user2=:name2) OR (user1=:name2 AND user2=:name1)"), {"name1":user1, "name2":user2})
    db.session.commit()

def add_directmessage(user1, user2, message):
    db.session.execute(text("INSERT INTO directmessages (user1, user2, content, created_at, deleted) VALUES (:user1, :user2, :message, NOW(), FALSE)"), {"user1":user1, "user2":user2, "message":message})
    db.session.commit()

def delete_area(id):
    db.session.execute(text("UPDATE areas SET deleted=TRUE WHERE id=:id"), {"id":id})
    db.session.commit()

def delete_user(user):
    db.session.execute(text("UPDATE users SET deleted=TRUE WHERE names=:name"), {"name":user})
    db.session.execute(text("UPDATE friendlist SET deleted=TRUE WHERE user1=:name OR user2=:name"), {"name":user})
    db.session.commit()

def delete_message(id):
    db.session.execute(text("UPDATE messages SET deleted=TRUE WHERE id=:id"), {"id":id})
    db.session.commit()

def delete_directmessage(id):
    db.session.execute(text("UPDATE directmessages SET deleted=TRUE WHERE id=:id"), {"id":id})
    db.session.commit()

def add_admin(name):
    db.session.execute(text("UPDATE users SET admins=TRUE WHERE names=:name"), {"name":name})
    db.session.commit()

def remove_admin(name):
    db.session.execute(text("UPDATE users SET admins=FALSE WHERE names=:name"), {"name":name})
    db.session.commit()