import json
import sys
import requests
from urllib.request import urlretrieve
import uuid
import os


def format_img_number(num):
    if num % 30 == 0:
        return num
    else:
        return 30 * (num // 30 + 1)


if __name__ == '__main__':
    base_url = 'https://image.baidu.com/search/acjson'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    data = {
        'tn': 'resultjson_com',
        'word': '',
        'pn': 0
    }

    result_dir = 'cxk'

    if os.path.exists(result_dir):
        print(f"当前目录已存在文件夹{result_dir},请移除该文件夹后重新运行本程序")
        sys.exit()  # 正常退出当前程序
    else:
        os.mkdir(f'{result_dir}')

    keyword_list = ['蔡徐坤鸡']
    page_number = 30  # 每页图片的数量
    start_page = 1
    end_page = 0
    # int()不能将带有小数点的字符串转化为整数类型。
    # 可以在int()里加入float(),先强制转换为浮点型，再转换为整数型。
    img_number = int(float(input("\033[1;31m请输入您想要爬取的ikun表情包数量:\033[0m")))
    if img_number <= 0:
        print("数量格式有误")
    else:
        print(f"\033[1;32m本程序即将为您爬取{format_img_number(img_number)}张表情包\033[0m")
        end_page = format_img_number(img_number)//30

    for keyword in keyword_list:
        os.mkdir(f'{result_dir}/{keyword}')
        cnt = 1
        for pn in range(start_page * page_number, end_page * page_number + 1, page_number):
            data['word'] = keyword
            data['pn'] = pn

            response = requests.get(url=base_url, params=data, headers=headers)

            try:
                # json.decoder.JSONDecodeError: Invalid \escape报错解决
                json_str = response.text.replace("\\'", "")

                json_data = json.loads(json_str)['data']
                json_data.pop()  # 删除末尾的空元素

                for obj in json_data:
                    img_src = obj['middleURL']
                    print(f'\033[1;34m正在爬取第{cnt}张ikun表情包\033[0m  {img_src}')
                    urlretrieve(url=img_src, filename=f'./{result_dir}/{keyword}/{uuid.uuid1()}.gif')
                    cnt = cnt + 1
            except Exception as e:
                print(f"捕获到异常:{e}")

    print("\033[1;31m爬取完毕!!!\033[0m")
