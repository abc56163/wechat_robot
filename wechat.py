import os
import MySQLdb
import itchat
import threading
from threading import *
import time
import jieba

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
jieba.load_userdict(base_dir+'/dict.txt')

db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')


def mysql_connection(db):
    try:
        db.ping()
    except:
        db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')
    return db


EXPR_DONT_UNDERSTAND = '未匹配到关键词'
cursor = mysql_connection(db).cursor()


class WeChat(Thread):
    def __init__(self):
        super().__init__()
        self.cursor = mysql_connection(db).cursor()
        pass

    def database_search(self, msg):
        text = ''
        try:
            seg_list = jieba.cut(msg, cut_all=False)
            print(jieba.lcut(msg, cut_all=False))
            t = True
            while t:
                cursor.execute('select * from 58_robot_2 where keyword LIKE "{}";'.format(next(seg_list)))
                a = cursor.fetchall()
                if a != ():
                    text = a[0][2]
                    t = False
            return text
        except StopIteration:
            text = EXPR_DONT_UNDERSTAND
            return text

    def run(self):
        @itchat.msg_register('Text')
        def reply(msg):
            text = msg.text.replace(' ', '')
            print(msg)
            info = self.database_search(text)
            # print('From:',text,'\n'+'To:',info)
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            try:
                cursor.execute('insert into 58_robot_3 (im, time, question, answer) values ("Wecht", "{}", "{}", "{}")'
                               .format(msg_time, text, info))
                db.commit()
            except:
                db.rollback()
            # with open('wechat_msg_log1.txt','a') as wc:
            #     wc.write('{}{}{}'.format(msg_time+'\n','From:'+text,'\n'+'To:'+info+'\n'))
            # user = msg['User']
            # print(msg)
            # print('%s %s'%(user['UserName'],msg.text))
            # text = msg.text
            # info = get_reponse(text)
            myusername = itchat.get_friends(update=True)[0]["UserName"]
            if not msg['FromUserName'] == myusername and info != EXPR_DONT_UNDERSTAND:
                itchat.send(info, msg['FromUserName'])
            else:
                pass

        @itchat.msg_register('Text', isGroupChat=True)
        def group_reply(msg):
            text = msg.text
            info = self.database_search(text)
            print('From:', text, '\n' + 'To:', info)
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                cursor.execute('insert into 58_robot_3 (im, time, question, answer) values ("Wecht", "{}", "{}", "{}")'
                               .format(msg_time, text, info))
                db.commit()
            except:
                db.rollback()
            # with open('wechat_msg_group_log1.txt', 'a') as wc:
            #     wc.write('{}{}{}'.format(msg_time + '\n', 'From:' + text, '\n' + 'To:' + info + '\n'))
            # print(msg['User']['UserName'])
            print(text)
            myusername = itchat.get_friends(update=True)[0]["UserName"]
            if not msg['User']['UserName'] == myusername and info != EXPR_DONT_UNDERSTAND:
                itchat.send(info, msg['User']['UserName'])


def main():
    t1 = WeChat()
    t2 = WeChat()
    t3 = WeChat()
    t4 = WeChat()
    t5 = WeChat()
    t6 = WeChat()
    t7 = WeChat()
    t8 = WeChat()
    for t in [t1,t2,t3,t4,t5,t6,t7,t8]:
        t.start()
        t.join()


if __name__ == '__main__':
    main()
    itchat.auto_login(True)
    itchat.run()
