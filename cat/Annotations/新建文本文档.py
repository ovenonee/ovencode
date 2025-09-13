import os

def remove_spaces_in_filenames(directory: str) -> None:
    """
    递归地去掉 directory 及其子目录中所有文件/文件夹名称里的空格。
    如果目标文件名已存在则跳过，防止覆盖。
    """
    for root, dirs, files in os.walk(directory, topdown=False):
        # 先处理文件
        for name in files:
            if ' ' not in name:
                continue
            new_name = name.replace(' ', '')
            src = os.path.join(root, name)
            dst = os.path.join(root, new_name)
            if os.path.exists(dst):
                print(f'⚠️  目标文件已存在，跳过：{dst}')
                continue
            os.rename(src, dst)
            print(f'✅ 已重命名：{src} -> {dst}')

        # 再处理目录（保证父目录重命名在子目录之后）
        for name in dirs:
            if ' ' not in name:
                continue
            new_name = name.replace(' ', '')
            src = os.path.join(root, name)
            dst = os.path.join(root, new_name)
            if os.path.exists(dst):
                print(f'⚠️  目标目录已存在，跳过：{dst}')
                continue
            os.rename(src, dst)
            print(f'✅ 已重命名：{src} -> {dst}')


if __name__ == '__main__':
    directory = r'D:\oven\ovenrm\cat\Annotations'
    remove_spaces_in_filenames(directory)