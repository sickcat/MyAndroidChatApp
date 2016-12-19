from settings import settings
from tornado import ioloop, gen
from tornado_mysql import pools
import torndb
import time

def database(fun, sql):
    try:
        db = torndb.Connection(host=settings["db_host"],
            database=settings['db_database'],
            user=settings["db_user"],
            password=settings["db_password"],
            time_zone=settings["db_time_zone"])
        if fun == 0:
            return db.query(sql)
        else:
            db.execute(sql)
            return None
    except Exception as e:
        print e
        time.sleep(2)
        print "-----------Connect Error Try Again..."
        database(fun, sql)

def checkuser(user_id, password):
    print "checkuser"
    if len(database(0, "select * from user where user_id='{0}' and password='{1}'".format(user_id, password))) == 0:
        return False
    else:
        return True

def FindUserByName(user_name):
    print "finduserbyname"
    if len(database(0, "select * from user where user_name='{0}'".format(user_name))) == 0:
        return False
    else:
        return True

def InsertUser(user_id, password, config, user_name):
    print "insert"
    database(1, "insert into user(user_id, password, config, user_name) values('{0}', '{1}', '{2}', '{3}')".format(
        torndb.MySQLdb.escape_string(user_id),
        torndb.MySQLdb.escape_string(password),
        torndb.MySQLdb.escape_string(config),
        torndb.MySQLdb.escape_string(user_name)))

def GetNewUserId():
    count = len(database(0, "select user_id from user"))
    count = 100000 + count
    return str(count)

def GetUserById(user_id):
    return database(0, "select * from user where user_id='{0}'".format(user_id))

def getContext(user_id):
    return database(0, "SELECT * from friend where user_id_1='{0}' or user_id_2='{0}'".format(user_id))

def InsertMsg(from_user, to_user, msg, msg_at, msg_type, sended = 0):
    database(1, "INSERT into msg(from_user, to_user, msg, msg_at, type, sended) values('{0}', '{1}', '{2}', '{3}', {4}, {5})".format(
        from_user, to_user, torndb.MySQLdb.escape_string(msg), msg_at, msg_type, sended))
    return database(0, "select LAST_INSERT_ID()")
def GetMsg(msg_id, from_user):
    return database(0, "select * from msg where msg_id={0} and to_user={1}".format(msg_id, from_user))
def GetUnsendedMsg(user_id):
    return database(0, "select * from msg where to_user='{0}' and sended=0".format(user_id))
