# example/__rm_dirs_by_os.walk.py 测试了使用os.walk()函数遍历文件，并删除文件
# Python还提供了一个shutil模块，shutil 是高级的文件，文件夹，压缩包处理模块
# 同样实现删除目录下所有子目录及文件
import os
import shutil

if __name__ == '__main__':
    root_path = r'D:\Temporary\2018'

    # 准备目录及文件
    if not os.path.exists(os.path.join(root_path, '07')):
        os.makedirs(os.path.join(root_path, r'07\15\code'))
        os.makedirs(os.path.join(root_path, r'07\16\code'))
        with open(os.path.join(root_path, r'07\15\code\a.py'), 'w+'):
            pass
        with open(os.path.join(root_path, r'07\15\b.py'), 'w+'):
            pass
        with open(os.path.join(root_path, r'07\c.py'), 'w+'):
            pass

    # 生成的目录结构
    # ./2018/
    # └── 07
    #     ├── 15
    #     │   ├── b.py
    #     │   └── code
    #     │       └── a.py
    #     ├── 16
    #     │   └── code
    #     └── c.py

    # D:\Temporary\2018 True
    print(root_path, os.path.exists(root_path))

    # 执行删除目录
    shutil.rmtree(root_path)

    # D:\Temporary\2018 False
    print(root_path, os.path.exists(root_path))
