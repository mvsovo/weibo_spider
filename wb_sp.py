
import traceback
import pymysql
from bs4 import BeautifulSoup
import random
import time
import requests
import re


class Weibo:
    cookie = {
        "cookie":''
    }
    agents = [
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    ]
    UA = random.choice(agents)
    header = {'User-Agent': UA}
    cnx = pymysql.connect(user='root', password='interesting', host='localhost', database='weibo',charset='utf8mb4')
    cur = cnx.cursor()


    def get_user_info(self):
        try:
            for i in range(1,83):    #页数
                pattern = r'\d+'
                url2 = 'https://weibo.cn/search/mblog/?keyword=乐清+滴滴顺风车&sort=hot&page={}'.format(i)  #复制的url
                print(url2)
                html2 = requests.get(url2, cookies=Weibo.cookie, headers=self.header)
                time.sleep(3)
                selector = BeautifulSoup(html2.text, 'lxml').find_all('div', class_='c')
                print(selector)
                print(len(selector))
                if len(selector) > 5:
                    for i in range(3, len(selector) - 2):
                        n = selector[i].find_all('div')
                        print(len(n))
                        if len(n) == 3:
                            user_name = n[0].find('a', class_='nk').get_text()
                            print(user_name)
                            weibos = n[2].get_text().split('  ')[0][5:]
                            weibos = weibos.encode('gbk', 'ignore')
                            weibos = str(weibos.decode('gbk', 'ignore'))
                            zhuanfa = n[0].find('span', class_='ctt').get_text()
                            all_num = n[2].find_all('a')
                            if all_num[-1].get_text() == '收藏':
                                num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                                p_url = all_num[-2]['href']
                            else:
                                num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                                p_url = all_num[-3]['href']
                            print(num_zan)
                            print(weibos)
                            others = n[2].find('span', class_='ct').get_text().split(' ')
                            if others[0]:
                                post_time = str(others[0])
                        elif len(n) == 1:
                            user_name = n[0].find('a', class_='nk').get_text()
                            zhuanfa = ''
                            print(user_name)
                            weibos = n[0].find('span', class_='ctt').get_text()
                            weibos = weibos.encode('gbk', 'ignore')
                            weibos = str(weibos.decode('gbk', 'ignore'))
                            all_num = n[0].find_all('a')
                            if all_num[-1].get_text() == '收藏':
                                num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                                p_url = all_num[-2]['href']
                            else:
                                num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                                p_url = all_num[-3]['href']
                            print(weibos)

                            others = n[0].find('span', class_='ct').get_text().split(' ')
                            if others[0]:
                                post_time = str(others[0])
                        elif len(n) == 2:
                            user_name = n[0].find('a', class_='nk').get_text()
                            print(user_name)

                            z = n[1].find_all('span')
                            if len(z) >= 2:
                                weibos = n[1].get_text().split('  ')[0][5:]
                                weibos = weibos.encode('gbk', 'ignore')
                                weibos = str(weibos.decode('gbk', 'ignore'))
                                all_num = n[1].find_all('a')
                                zhuanfa = n[0].find('span', class_='ctt').get_text()
                                if all_num[-1].get_text() == '收藏':
                                    num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                    num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                    num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                                    p_url = all_num[-2]['href']
                                else:
                                    num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                    num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                    num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                                    p_url = all_num[-3]['href']
                                print(num_zan)
                                print(weibos)
                            else:
                                str_t = n[0].find('span', class_='ctt').get_text()
                                weibos = str_t.encode('gbk', 'ignore')
                                weibos = str(weibos.decode('gbk', 'ignore'))
                                zhuanfa = ''
                                all_num = n[1].find_all('a')
                                if all_num[-1].get_text() == '收藏':
                                    num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                    num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                    num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                                    p_url = all_num[-2]['href']
                                else:
                                    num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                    num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                    num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                                    p_url = all_num[-3]['href']
                                print(num_zan)
                                print(weibos)

                            others = n[1].find('span', class_='ct').get_text().split(' ')
                            if others[0]:
                                post_time = str(others[0])
                        else:
                            continue

                        #评论
                        p_req = requests.get(p_url, cookies=Weibo.cookie, headers=self.header, timeout=10)
                        p_url = p_url[:-7]
                        time.sleep(2)
                        if BeautifulSoup(p_req.text, 'lxml').find('div', class_='pa', id='pagelist') != None:
                            num = int(BeautifulSoup(p_req.text, 'lxml').find('div', class_='pa', id='pagelist').find_all('input')[0]['value'])
                        else:
                            num = 1
                        if num > 100000:
                            num = 100000
                        for p in range(1, num + 1):

                            ur = p_url + '&page=%s' %str(p)

                           # print(p_url)
                            print(ur)
                            req = requests.get(ur, cookies=Weibo.cookie, headers=self.header)
                            time.sleep(2)
                            #print(req.text)
                            soup = BeautifulSoup(req.text, 'lxml').find_all('div', class_='c')
                            print(len(soup))
                            if len(soup) > 5:
                                for i in range(4, len(soup) - 1):
                                    if soup[i].find('span', class_='ctt') == None:
                                        sql = 'INSERT INTO wbs (`user_name`, `weibos`, `p_time`,`zhuanfa`, `num_zan`, `num_forwarding`, `num_comment`, `ctt`, `p_name`, `ping_time`)\
                                          VALUES (%(user_name)s, %(weibos)s, %(p_time)s, %(zhuanfa)s, %(num_zan)s, %(num_forwarding)s, %(num_comment)s, %(ctt)s, %(p_name)s, %(ping_time)s)'
                                        value = {
                                            'user_name': user_name,
                                            'weibos': weibos,
                                            'p_time': post_time,
                                            'zhuanfa': zhuanfa,
                                            'num_zan': num_zan,
                                            'num_forwarding': num_forwarding,
                                            'num_comment': num_comment,
                                            'ctt': '',
                                            'p_name': '',
                                            'ping_time': ''
                                        }
                                        self.cur.execute(sql, value)
                                        self.cnx.commit()
                                    else:
                                        ctt = soup[i].find('span', class_='ctt').get_text()
                                        print(ctt)
                                        p_name = soup[i].find_all('a')[0].get_text()
                                        print(p_name)
                                        ping_time = soup[i].find('span', class_='ct').get_text().split(' ')[0].strip()
                                        print(ping_time)
                                        sql = 'INSERT INTO gjc (`user_name`, `weibos`, `p_time`,`zhuanfa`, `num_zan`, `num_forwarding`, `num_comment`, `ctt`, `p_name`, `ping_time`)\
                                             VALUES (%(user_name)s, %(weibos)s, %(p_time)s, %(zhuanfa)s, %(num_zan)s, %(num_forwarding)s, %(num_comment)s, %(ctt)s, %(p_name)s, %(ping_time)s)'
                                        value = {
                                            'user_name': user_name,
                                            'weibos': weibos,
                                            'p_time': post_time,
                                            'zhuanfa': zhuanfa,
                                            'num_zan': num_zan,
                                            'num_forwarding': num_forwarding,
                                            'num_comment': num_comment,
                                            'ctt': ctt,
                                            'p_name': p_name,
                                            'ping_time': ping_time
                                        }
                                        self.cur.execute(sql, value)
                                        self.cnx.commit()


        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def start(self):
        Weibo.get_user_info(self)



if __name__ == '__main__':

    wb = Weibo()
    wb.start()
