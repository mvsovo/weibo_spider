# weibo_spider

------

前一段时间重装了系统，没想到一些代码没备份完全... 导致很多麻烦，所以打算以后陆续把之前写过的代码或者以后要写的搞github上了。(

------

此项目功能爬取`weibo.cn`的信息，支持高级搜索，基于`python3.7`, 数据存储用`mysql`。

------

### 使用方法

配置好环境后，建立数据库，运行`wb.sql` 

代码`wb_sp.py` 中

```python
cookie = {
            #这里替换成自己cookie
       } 

#url2 替换为高级搜索所得到的url (注意最后的是page={}
url2 = 'https://weibo.cn/search/mblog/?keyword=滴滴顺风车+乐清&sort=hot&page={}'.format(i)

```

根据爬取的要求确定 （爬评论还是爬微博？爬多少条评论）变量`num`

```python
  if BeautifulSoup(p_req.text, 'lxml').find('div', class_='pa', id='pagelist') != None:
                            num = int(BeautifulSoup(p_req.text, 'lxml').find('div', class_='pa', id='pagelist').find_all('input')[0]['value'])
                        else:
                            num = 1
                        if num > 1000:
                            num = 1000
```

