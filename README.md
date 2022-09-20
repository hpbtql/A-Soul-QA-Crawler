# A-Soul-QA-Crawler

一个爬取 A-SOUL 每周 QA 的爬虫

## 使用方法

1. 将项目保存至本地

```bash
git clone https://github.com/hpbtql/A-Soul-QA-Crawler.git
```

2. 运行`crawler.py`后等待结果即可

```bash
python crawler.py
```

该项目的所有文件中，仅有`crawler.py`是爬虫文件，其余文件可作为节省二次爬虫时间的缓存，均可直接删除。
缓存截止至【A-SOUL制作委员会的双周QA 9.6】

## 项目文件架构

```tree
A-Soul-QA-Crawler
│  articles_list.json       # QA列表，文件中包含所有的QA专栏信息
│  crawler.py               # 爬虫文件，本项目实际有用的文件
│  output.json              # 所有A-SOUL运营的回答合集，以JSON数组存储
│
├─articles                  # 所有的文章缓存
│      cv9967782.html       # 每篇文章的HTML网页文件，以CV号命名
│      ...
│
└─cuts                      # 所有回答的缓存
        9967782.json        # 每篇文章内所有回答的JSON文件，以CV号命名
        ...
```
