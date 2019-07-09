import MySQLdb


def base():
    db = MySQLdb.connect("*********", "*********", "*********", "*********", charset='utf8')
    return db


def databases():
    db = base()
    try:
        db.ping()
    except:
        db = MySQLdb.connect("*********", "*********", "*********", "*********", charset='utf8')
    return db
