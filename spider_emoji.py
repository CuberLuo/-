from urllib.request import urlopen, Request, urlretrieve
from lxml import etree
import os
import shutil


def format_filename(filename):
    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in filename:
        if char in sets:
            filename = filename.replace(char, '')
    return filename


class Spider:
    def __init__(self):
        # 起始页码
        self.start_page = 1
        # 末页页码
        self.end_page = 12
        self.package_name = '表情包'

    def create_folder(self):
        # 创建保存图片的目录
        if os.path.exists(self.package_name):
            shutil.rmtree(self.package_name)
        os.mkdir(self.package_name)

    def get_img(self):
        for i in range(self.start_page - 1, self.end_page):
            page = i + 1
            if page == 1:
                base_url = "http://www.bbsnet.com/biaoqingbao"
            else:
                base_url = f"http://www.bbsnet.com/biaoqingbao/page/{page}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
            }
            request = Request(base_url, headers=headers)
            response = urlopen(request)
            content = response.read().decode('utf-8')

            tree = etree.HTML(content)
            img_src_list = tree.xpath('//div[@class="thumbnail"]/a/img/@src')
            img_name_list = tree.xpath('//div[@class="thumbnail"]/a/img/@alt')

            os.mkdir(f"./{self.package_name}/第{page}页")
            for j in range(len(img_name_list)):
                try:
                    img_name_list[j] = format_filename(img_name_list[j])
                    print(f"正在爬取第{page}页的第{j + 1}张图片: {img_name_list[j]}.gif  {img_src_list[j]}")
                    urlretrieve(url=img_src_list[j],
                                filename=rf"./{self.package_name}/第{page}页/{j + 1}-{img_name_list[j]}.gif")
                except Exception as e:
                    print(f"捕获到异常:{e}")


if __name__ == '__main__':
    spider = Spider()
    spider.create_folder()
    spider.get_img()
