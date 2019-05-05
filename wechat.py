import os
import MySQLdb
import itchat
import threading
from threading import *
import time
import jieba

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jieba.load_userdict(base_dir+'/dict.txt')

db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')


def mysql_connection(db):
    try:
        db.ping()
    except:
        db = MySQLdb.connect("localhost", "root", "Abcd520025@", "58dh", charset='utf8')
    return db


EXPR_DONT_UNDERSTAND = '未匹配到关键词'
supplement = "\n\n更多解决方案可以输入下列关键词:电话问题,电脑问题,网络问题来获取更多帮助!\n您也可以直接美式扫工位二维码或online在线提单来快速联系IT!"
cursor = mysql_connection(db).cursor()


class WeChat(Thread):
    def __init__(self):
        super().__init__()
        self.cursor = mysql_connection(db).cursor()
        pass

    def database_search(self, msg):
        text = ''
        if msg in ('电话问题', '电脑问题', '网络问题'):
            table = '58_robot_1'
            cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, msg))
            a = cursor.fetchall()
            if a != ():
                text = a[0][2]
            return text
        elif '关键词/' in msg:
            key = msg.split('/')[1]
            with open(base_dir + '/dict.txt', 'a') as k:
                k.write(key + ' ' + '2000' + '\n')
            jieba.add_word(key)
            des = ''
            text = '关键词已经添加' + des
            return text
        else:
            dict_list = []
            table = '58_robot_2'
            des = supplement
            print(jieba.lcut(msg, cut_all=False, HMM=False))
            for x in jieba.cut(msg, cut_all=False, HMM=False):
                dict_list.append(x)
            num_list = [len(o) for o in dict_list]
            if max(num_list) == 0:
                a = None
            else:
                seg = dict_list[num_list.index(max(num_list))]
                cursor.execute('select * from {} where keyword LIKE "{}";'.format(table, seg))
                a = cursor.fetchall()
            if a != ():
                text = a[0][2] + des
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
    for t in [t1, t2, t3, t4, t5, t6, t7, t8]:
        t.start()
        t.join()


if __name__ == '__main__':
    main()
    itchat.auto_login(True, enableCmdQR=True)
    itchat.run()
