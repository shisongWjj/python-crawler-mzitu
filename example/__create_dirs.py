import os

ROOT_DIR = r'D:\Temporary'

path = os.path.join(ROOT_DIR, r'2018\07\15')

if os.path.exists(path):
    try:
        os.makedirs(path)
    except FileExistsError as e:
        # [WinError 183] 当文件已存在时，无法创建该文件。: 'D:\\Temporary\\2018\\07\\15'
        print(e)
