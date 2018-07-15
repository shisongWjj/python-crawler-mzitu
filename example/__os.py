import os

DIR_ROOT = r'd:\temporary\mzitu'

# 创建子目录
path = os.path.join(DIR_ROOT, '2018')
# d:\temporary\mzitu\2018
print(path)
# 判断目录(文件)是否存在
# d:\temporary\mzitu\2018 True
print(path, os.path.exists(path))
# d:\temporary\mzitu True
print(DIR_ROOT, os.path.exists(DIR_ROOT))

# 创建单层目录
if not os.path.exists(path):
    os.mkdir(path, 755)
# d:\temporary\mzitu\2018 True
print(path, os.path.exists(path))

# 创建多层目录
path = os.path.join(DIR_ROOT, r'2018\07\15')
if not os.path.exists(path):
    os.makedirs(path, 755)
# d:\temporary\mzitu\2018\07\15 True
print(path, os.path.exists(path))

# 创建文件
with open(os.path.join(path, 'a.py'), 'w+'):
    pass

# 尝试删除单层目录，但目录下有文件
if os.path.exists(path):
    try:
        os.rmdir(path)
    except OSError as e:
        # [WinError 145] 目录不是空的。: 'd:\\temporary\\mzitu\\2018\\07\\15'
        print(e)
        # 先删除文件
        # 父目录、子目录列表、文件列表
        for parent, dirs, files in os.walk(path):
            # 这里没有子目录
            print('没有子目录：', dirs)
            # 但可能有文件
            for f in files:
                os.remove(os.path.join(path, f))

        # 再删除目录
        os.rmdir(path)

# d:\temporary\mzitu\2018\07\15 False
print(path, os.path.exists(path))

# 再创建一些子目录和文件，测试删除多级目录
os.makedirs(path)
with open(os.path.join(path, 'b.py'), 'w+'):
    pass
with open(os.path.join(DIR_ROOT, r'2018\c.py'), 'w+'):
    pass
with open(os.path.join(DIR_ROOT, r'2018\07\d.py'), 'w+'):
    pass

# 删除多级目录，如果目录下没有文件，可以直接删除
# 将要删除多级目录：d:\temporary\mzitu\2018\07\15
print('将要删除多级目录：{}'.format(path))
if os.path.exists(path):
    try:
        # 该方法与常规理解不同，方法会递归删除指定目录
        # 但并非删除给定目录及其所有子目录，
        # 而是以给定目录为最内层目录，层层向上找其不为空的上级(没有文件)
        # 如果有文件就不再向上找，找到的目录将被删除，下面给一个示例：
        # 假设目录：/a/b/c/d，其中/a目录下除了有b目录，还有F文件
        # 调用该方法传入：/a/b/c/d，删除除的顺序：
        # /a/b/c/d
        # /a/b/c/
        # /a/b/
        # /a，到a的时候，因为里面有文件，所以不再向上找，也不删除，方法结束
        # 本例传入的目录下有文件，所以一层目录也没有删除，会抛出异常
        os.removedirs(path)
    except OSError as e:
        print(e)


        # 删除目录及子目录下所有文件
        def recursion_remove_files(path):
            if not path or not os.path.exists(path):
                return
            for parent, dirs, files in os.walk(path):
                # 如果有文件就删除文件
                if files:
                    for f in files:
                        os.remove(os.path.join(path, f))
                # 如果有目录，就向下遍历
                if dirs:
                    for dir in dirs:
                        recursion_remove_files(os.path.join(path, dir))


        # 递归删除文件，这里的递归是程序员自己实现的，从外层目录向内层目录递归，所以要指定为外层目录
        recursion_remove_files(os.path.join(DIR_ROOT, '2018'))
        # 再执行删除多级目录
        os.removedirs(path)

# d:\temporary\mzitu\2018\07\15 False
print(path, os.path.exists(path))
