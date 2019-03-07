import jieba
import os
jieba.load_userdict(os.path.dirname(__file__)+'/dict.txt')
import MySQLdb
import itchat
import threading
from threading import *
import time


db = MySQLdb.connect("localhost", "root", "Abcd520025@", "study", charset='utf8')
cursor = db.cursor()
EXPR_DONT_UNDERSTAND = '未匹配到关键词'

class WeChat(Thread):
    def __init__(self):
        super().__init__()
        pass


    def database_search(self, msg):
        try:
            cursor.execute('select * from robot where keyword LIKE "%s"' % msg)
            a = cursor.fetchall()
            text = a[0][2]
            return text
        except:
            try:
                seg_list = jieba.cut(msg, cut_all=False)
                t = True
                while t:
                    cursor.execute('select * from robot where keyword LIKE "%{}%"'.format(next(seg_list)))
                    a = cursor.fetchall()
                    if a != ():
                        text = a[0][2]
                        t = False
                return text
            except:

                text = EXPR_DONT_UNDERSTAND
                return text






    def run(self):
        @itchat.msg_register('Text')
        def reply(msg):
            text = msg.text
            print(msg)
            info = self.database_search(text)
            print('From:',text,'\n'+'To:',info)
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            with open('wechat_msg_log.txt','a') as wc:
                wc.write('{}{}{}'.format(msg_time+'\n','From:'+text,'\n'+'To:'+info+'\n'))
            # user = msg['User']
            # print(msg)
            # print('%s %s'%(user['UserName'],msg.text))
            # text = msg.text
            # info = get_reponse(text)
            myUserName = itchat.get_friends(update=True)[0]["UserName"]
            if not msg['FromUserName'] == myUserName or info != EXPR_DONT_UNDERSTAND:
                itchat.send(info, msg['FromUserName'])
            else:
                pass

        @itchat.msg_register('Text', isGroupChat=True)
        def group_reply(msg):
            text = msg.text
            info = self.database_search(text)
            print('From:', text, '\n' + 'To:', info)
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open('wechat_msg_group_log.txt', 'a') as wc:
                wc.write('{}{}{}'.format(msg_time + '\n', 'From:' + text, '\n' + 'To:' + info + '\n'))
            print(msg['User']['UserName'])
            print(text)
            myUserName = itchat.get_friends(update=True)[0]["UserName"]
            if not msg['User']['UserName'] == myUserName:
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
