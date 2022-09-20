# %%
# 最后所有QA中A保存的位置
A_file_save_path = "./output.json"

# 使用本地QA列表的开关
USE_LOCAL_READLIST = False
# QA列表url
readlist_url = 'https://api.bilibili.com/x/article/list/web/articles?id=391547&jsonp=jsonp'
# QA列表保存的位置
readlist_file_save_path = "./articles_list.json"


# 自定义伪装请求标头
myHeaders = {
'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

# %%
# Notebook 适用，用于创建文件夹
# !rm -rf ./*
# !mkdir ./articles/
# !mkdir ./cuts/
# !ls

# %%
import os #检查文件路径
import time #用于延时
import re #正则表达式
import json
import requests #完成http相关请求



# %%
# 采集QA列表
try:
    r = requests.get(readlist_url, headers=myHeaders)
    r.raise_for_status()
    article_list = json.loads(r.text)
    length = len(article_list["data"]["articles"])
    with open(readlist_file_save_path, 'w', encoding='utf-8') as file:
        file.write(r.text)
    print(f"列表采集成功，共有{length}篇QA")
except Exception as ex: #捕获所有可能的异常
    print(f"列表采集出错，出错原因:{ex}")


# %%
class Bili_CV:
    """
    类描述：
        类的作用:此类可以处理与CV号相关的数据提取工作
    Attributes:
        cv: str,纯数字组成的CV号
        name: str,HTML无后缀的文件名
        path: str,HTML文件的路径
        content: str,HTML文件的内容
    """
    def __init__(self, cv):
        '''
        方法功能：根据CV号自动生成对应名称的HTML文件和结构树
        :param cv: CV号,str类型,无默认值
        '''
        self.cv = cv
        self.name = "cv" + cv            
        self.path = './articles/{}.html'.format(self.name)
        
        if os.path.isfile(self.path): #没有HTML文件则爬取
            self.content = self.read_local_html()
            print(f"{self.name}.html已存在，初始化完成")
        else:
            self.content = self.read_online_html()


    def read_online_html(self):
        '''
        方法功能：根据对象的CV号发出HTML请求以获取html文件
        :return: 布尔类型,True则表示获取成功
        '''
        url = 'https://www.bilibili.com/read/cv{}'.format(self.cv)
        try:
            r = requests.get(url, headers=myHeaders)
            r.raise_for_status() #抛异常处，返回HTTPError对象
            r.encoding = 'utf-8'
            with open(self.path, 'w', encoding='utf-8') as file:
                file.write(r.text) 
            time.sleep(5) #抓取一页后，休眠5秒再抓取下一页，防止被识别成爬虫而封IP
            print(f"{self.name}.html采集成功")
            return r.text
        except Exception as ex: #捕获所有可能的异常
            print(f"{self.name}.html采集出错，出错原因:{ex}")
            return ""

        
    def read_local_html(self):
        """
        方法功能：读取本地HTML文件
        :return: 返回str类型，HTML文件内容
        """
        with open(self.path, 'r', encoding='utf-8') as f:
            r = f.read()
        print("{}读取完毕".format(self.name))
        return r

# %%

def get_A(content):
    """
    方法功能：从HTML中截取QA中一它回复的内容
    :param content: str类型,表示需要提取A的文本
    :return: 返回str类型的数组,文本中的所有A
    """
    pattern = re.compile(r"A：</strong>.*?<figure")
    res = pattern.findall(content)
    return res

# %%
# 获取所有的QA文章并保存
QA_list = []
QA_list1 = []

for i in range(len(article_list["data"]["articles"])):
    cv_ele = Bili_CV(str(article_list["data"]["articles"][i]["id"]))

    single_file_path = "./cuts/" + str(cv_ele.cv) + ".json"
    single_item = get_A(cv_ele.content)

    if os.path.isfile(single_file_path): #没有文件则写入
        with open(single_file_path, 'w', encoding='utf8') as f:  #写入
            f.writelines("[")
            for i in single_item:
                f.writelines('"' + re.sub("<.*?>", "", str(i)[11:-11] + '",\n'))
            f.writelines("]")
    
    QA_list += single_item
    
    QA_list1.append(cv_ele)

print("已更新完毕")

# %%
# # 导出所有的A txt
# with open(A_file_save_path, 'w', encoding='utf8') as f:  #写入
#     for i in QA_list:
#         f.writelines(re.sub("<.*?>", "", str(i)[11:-11]+'\n'))

# %%
# 导出所有的A json
with open(A_file_save_path, 'w', encoding='utf8') as f:  #写入
    f.writelines("[\n")
    for i in QA_list:
        f.writelines('"' + re.sub("<.*?>", "", str(i)[11:-11] + '",\n'))
    f.writelines("]")

# %%
# NoteBook 适用，用于打包产生的文件
# !zip -r 1.zip ./*


