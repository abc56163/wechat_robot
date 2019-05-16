import MySQLdb


def base():
    db = MySQLdb.connect("10.245.0.224", "root", "58ganji@123", "58dh", charset='utf8')
    return db


def databases():
    db = base()
    try:
        db.ping()
    except:
        db = MySQLdb.connect("10.245.0.224", "root", "58ganji@123", "58dh", charset='utf8')
    return db
