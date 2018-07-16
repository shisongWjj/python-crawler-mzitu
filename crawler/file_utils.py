# 文件、目录工具库
import os
import shutil
from threading import Lock


class MyFileUtils:

    def __init__(self):
        self._lock = Lock()

    def rmdirs(self, path):
        """
        清理指定PATH下所有子目录及文件(含指定目录本身)
        :param path:
        :return:
        """
        # 作一个基本保护，避免误删除C盘文件
        if not path or path.lower().startswith('c:'):
            raise Exception('路径为空或者为C盘目录')
        # 清除目录
        if os.path.exists(path):
            shutil.rmtree(path)

    def mkdirs(self, path):
        """
        创建多级目录，创建成功返回 True，返回False说明目录已存在
        :param path:
        :return:
        """
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path)
            return True

    def save_photo(self, _dir, photo, data):
        """
        保存图片文件
        :param _dir: 目录
        :param photo: 图片名称
        :param data:  图片字节数据
        :return:
        """
        # 目录不存在时先创建目录
        # 创建目录时加锁，避免并发创建同一个目录
        if not os.path.exists(_dir):
            with self._lock:
                self.mkdirs(_dir)
        # 创建文件本身不需要加锁(即使并发程序也不会同时写入同一张图片)
        path = os.path.join(_dir, photo)
        if os.path.exists(path):
            return
        with open(path, 'bw+') as f:
            f.write(data)


if __name__ == '__main__':
    utils = MyFileUtils()

    utils.rmdirs(r'D:\Temporary\2018')
    # utils.clean_dirs(r'C:\Windows.old')

    print(utils.mkdirs(r'D:\Temporary\2018\07\15'))
