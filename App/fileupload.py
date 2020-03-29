'''
author = 李雄涛
data = 2020/3/17
当前py文件的作用：文件上传封装类
'''

import os
from datetime import datetime
from random import randint


class FileUpload:
    def __init__(self,file,exts=('png','jpg','jpeg'),is_randomname=False):
        self.file = file
        self.exts = exts
        self.is_randomname = is_randomname

    #上传文件路径
    def Upload(self,dest):
        if not self.check_type():
            return -1
        if self.is_randomname:
            self.file.name = self.random_filename()
        else:
            self.file.name = self.file.name
        path = os.path.join(dest,self.file.name)
        self.write_file(path)
        return self.file.name

    #检查文件格式
    def check_type(self):
        ext = os.path.splitext(self.file.name)
        if len(ext) > 1:
            ext = ext[1].lstrip('.')
            if ext in self.exts:
                return True
        return False

    #检查文件的名字
    def random_filename(self):
        filename = datetime.now().strftime('%Y%m%d%H%M%S')+str(randint(1,10000))
        ext_name = os.path.splitext(self.file.name)

        ext = ext_name[1] if len(ext_name) >1 else ''
        filename += ext
        return filename


    #写入文件
    def write_file(self,path):
        with open(path,'wb') as fp:
            if self.file.multiple_chunks:
                for chunk in self.file.chunks():
                    fp.write(chunk)
            else:
                fp.write(self.file.read())





