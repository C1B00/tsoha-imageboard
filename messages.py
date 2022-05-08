from db import db
import users

def add_thread(image_file, image_file_name, title, message, board_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO threads (image_file, image_file_name, title, message, user_id, board_name, sent_at) VALUES (:image_file, :image_file_name, :title, :message, :user_id, :board_name, NOW()) RETURNING id"
        result = db.session.execute(sql, {"image_file":image_file, "image_file_name":image_file_name, "title":title, "message":message, "user_id":user_id, "board_name":board_name})
        thread_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return thread_id

def remove_thread(thread_id):
    sql = "DELETE FROM threads WHERE id=:thread_id"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

def show_all_threads(board_name):
    sql = "SELECT T.id, T.image_file, T.title, T.message, U.username, T.sent_at FROM threads T, users U WHERE T.board_name=:board_name AND U.id=T.user_id ORDER BY T.sent_at DESC"
    result = db.session.execute(sql, {"board_name":board_name})
    return result.fetchall()

def show_thread(thread_id):
    sql = "SELECT T.id, T.image_file, T.title, T.message, U.username, T.sent_at FROM threads T, users U WHERE T.id=:thread_id AND U.id=T.user_id ORDER BY T.sent_at DESC"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def add_reply(image_file, image_file_name, title, message, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO replies (image_file, image_file_name, title, message, user_id, thread_id, sent_at) VALUES (:image_file, :image_file_name, :title, :message, :user_id, :thread_id, NOW()) RETURNING id"
        result = db.session.execute(sql, {"image_file":image_file, "image_file_name":image_file_name, "title":title, "message":message, "user_id":user_id, "thread_id":thread_id})
        reply_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False
    return reply_id

def show_all_replies(thread_id):
    sql = "SELECT R.id, R.image_file, R.title, R.message, U.username, R.sent_at FROM threads T, replies R, users U WHERE R.thread_id=:thread_id AND T.id=R.thread_id AND U.id=R.user_id ORDER BY R.sent_at DESC"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def reply_count(thread_id):
    sql = "SELECT COUNT(*) FROM replies WHERE thread_id=:thread_id"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()[0]