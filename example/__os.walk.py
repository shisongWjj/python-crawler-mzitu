# 测试os.walk()函数
import os


def rec_rm_dirs(path):
    if not path or not os.path.exists(path):
        return

    # topdown=False，参数决定文件顺序，False时子目录(文件)从内层到外层，True则反之
    for parent, dirs, files in os.walk(path, topdown=False):
        # if files:
        #     for file in files:
        #         print(os.path.join(path, file))
        # if dirs:
        #     for dir in dirs:
        #         rec_rm_dirs(os.path.join(path, dir))

        # os.walk(path) 函数将目录、子目录、文件一次全部遍历出来，topdown=True
        # parent = D:\Temporary\2018, dirs = ['07'], files = []
        # parent = D:\Temporary\2018\07, dirs = ['15', '16'], files = ['c.py']
        # parent = D:\Temporary\2018\07\15, dirs = ['code'], files = ['b.py']
        # parent = D:\Temporary\2018\07\15\code, dirs = [], files = ['a.py']
        # parent = D:\Temporary\2018\07\16, dirs = ['code'], files = []
        # parent = D:\Temporary\2018\07\16\code, dirs = [], files = []
        # topdown=False，子目录(文件)从内层到外层，这对于删除目录时非常有用
        # parent = D:\Temporary\2018\07\15\code, dirs = [], files = ['a.py']
        # parent = D:\Temporary\2018\07\15, dirs = ['code'], files = ['b.py']
        # parent = D:\Temporary\2018\07\16\code, dirs = [], files = []
        # parent = D:\Temporary\2018\07\16, dirs = ['code'], files = []
        # parent = D:\Temporary\2018\07, dirs = ['15', '16'], files = ['c.py']
        # parent = D:\Temporary\2018, dirs = ['07'], files = []
        print('parent = {}, dirs = {}, files = {}'.format(parent, dirs, files))

        # 打印全部文件PATH
        # +打印全部文件路径+
        # +打印全部文件路径+
        # D:\Temporary\2018\07\c.py
        # +打印全部文件路径+
        # D:\Temporary\2018\07\15\b.py
        # +打印全部文件路径+
        # D:\Temporary\2018\07\15\code\a.py
        # +打印全部文件路径+
        # +打印全部文件路径+
        # print('+打印全部文件路径+')
        # for _file in files:
        #     print(os.path.join(parent, _file))

        # 打印全部目录PATH
        # +打印全部目录路径+
        # D:\Temporary\2018\07
        # +打印全部目录路径+
        # D:\Temporary\2018\07\15
        # D:\Temporary\2018\07\16
        # +打印全部目录路径+
        # D:\Temporary\2018\07\15\code
        # +打印全部目录路径+
        # +打印全部目录路径+
        # D:\Temporary\2018\07\16\code
        # +打印全部目录路径+
        # print('+打印全部目录路径+')
        # for _dir in dirs:
        #     print(os.path.join(parent, _dir))


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

    # 执行删除函数
    rec_rm_dirs(root_path)
