'''
author = 李雄涛
data = 2020/3/14
当前py文件的作用：画一个验证码
'''

# 定义一个验证码的类
import os
from io import BytesIO
from random import randint

from PIL import Image, ImageDraw, ImageFont

from blogback.settings import BASE_DIR

list1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9','0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
    , 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class VerifyCode:
    # 定义画布的宽度和高度，以及验证码字符数
    def __init__(self, width=106, height=35, size=4):
        self.width = width
        self.height = height
        self.size = size
        # 初始化验证码字符
        self.__code = ''
        # 初始化画笔为空
        self.pen = None

    def generate(self):
        # 给一个画布，宽度，高度，和颜色
        im = Image.new('RGB', (self.width, self.height), self.__rand_color(150))
        self.pen = ImageDraw.Draw(im)
        # 生成验证码字符串
        self.rand_string()
        # 画验证码
        self.__draw_code()
        # 干扰线
        self.__draw_line()
        # 画干扰点
        self.__draw_point()
        # 返回验证码图片
        # 缓冲区？？？？
        buf = BytesIO()
        # 将验证码保存为png到缓冲区
        im.save(buf, 'png')
        # 获取图片的二进制
        res = buf.getvalue()
        buf.close()
        return res

    # 画布的底色
    def __rand_color(self, min=0, max=255):
        # 'RGB'三种随机的红绿蓝
        return randint(min, max), randint(min, max), randint(min, max)

    # 验证码字符串
    def rand_string(self):
        self.__code = ''
        for i in range(self.size):
            ele = randint(0,35)
            self.__code += list1[ele]

    # 画验证码
    def __draw_code(self):
        # 加载字体
        path = os.path.join(BASE_DIR, 'static/font/SIMLI.TTF')
        font = ImageFont.truetype(path, size=25, encoding='utf-8')
        # 计算字符的宽度
        width = (self.width - 25) // self.size
        for i in range(0, self.size):
            x = 13 + width * i
            self.pen.text((x,6),self.__code[i],font=font,fill=self.__rand_color(0,150))


    def __draw_point(self):
        for i in range(100):
            self.pen.point((randint(1,self.width-1),randint(1,self.height-1)),self.__rand_color(151,200))

    def __draw_line(self):
        for i in range(5):
            self.pen.line([(randint(1, self.width-1), randint(1, self.height-1)), (randint(1, self.width-1), randint(1, self.height-1))], fill=self.__rand_color(201,255), width=2)

    #外部可以调用
    @property
    def code(self):
        return self.__code

#单例属性
vc = VerifyCode()
# res = vc.generate()
# print(vc.code)
# if __name__ == '__main__':
#     pass