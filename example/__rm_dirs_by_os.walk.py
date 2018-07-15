# 实现一个函数，可以递归删除目录下所有子目录及文件
import os


def rec_seen_files(path):
    """
    返回指定PATH下所有文件，该函数为一个生成器
    :param path:
    :return:
    """
    if not path or not os.path.exists(path):
        return

    for parent, dirs, files in os.walk(path):
        if not files:
            continue
        # 返回全部的文件路径
        yield from [os.path.join(parent, f) for f in files]


def rec_seen_dirs(path):
    """
    返回指定PATH下所有子目录，该函数为一个生成器
    :param path:
    :return:
    """
    if not path or not os.path.exists(path):
        return

    for parent, dirs, files in os.walk(path):
        if not files:
            continue
        # 返回全部的文件路径
        yield from [os.path.join(parent, d) for d in dirs]


def rec_rm_dirs(path):
    """
    递归删除文件及子目录
    :param path:
    :return:
    """
    if not path or not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


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

    # 查看所有子文件
    # +打印所有子文件+
    # D:\Temporary\2018\07\c.py
    # D:\Temporary\2018\07\15\b.py
    # D:\Temporary\2018\07\15\code\a.py
    print('+打印所有子文件+')
    for _file in rec_seen_files(root_path):
        print(_file)

    # +打印所有子目录+
    # D:\Temporary\2018\07\15
    # D:\Temporary\2018\07\16
    # D:\Temporary\2018\07\15\code
    print('+打印所有子目录+')
    for _dir in rec_seen_dirs(root_path):
        print(_dir)

    # 执行删除函数
    print('+执行删除函数+')
    rec_rm_dirs(root_path)
