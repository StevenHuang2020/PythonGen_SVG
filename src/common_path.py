# -*- encoding: utf-8 -*-
# Date: 27/Apr/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Module for path, file oeprations
"""

import os


def traverse_folders(path, sub_folder=False):
    """Traverse the folders under the path"""
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames.sort()
        # print(dirnames)
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)
        if not sub_folder:
            break


def traverse_files(path, filters='', sub_folder=False):
    """Traverse the files under the path

    Args:
        path (str): path
        filters (str, optional): Extension name list, 'cpp h txt jpg'. Defaults to ''.
        sub_folder (bool, optional): Whether to traverse subfolders. Defaults to False.
    """

    def getExtFile(file):
        return file[file.find('.')+1:]

    fmts = filters.split()
    if fmts:
        for dirpath, dirnames, filenames in os.walk(path):
            filenames.sort()
            print('filenames=', filenames)
            for filename in filenames:
                if getExtFile(get_file_names(filename)[1]) in fmts:
                    yield os.path.join(dirpath, filename)
            if not sub_folder:
                break
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            filenames.sort()
            for filename in filenames:
                yield os.path.join(dirpath, filename)
            if not sub_folder:
                break


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def create_path(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def delete_folder(file_path):
    if os.path.exists(file_path):
        for lists in os.listdir(file_path):
            f = os.path.join(file_path, lists)
            if os.path.isfile(f):
                os.remove(f)


def get_file_name(path):
    """get basename, 'name.exe' 'x.zip' """
    return os.path.basename(path)


def get_file_names(path):
    """get split names, 'name.exe'--> tuple('name', '.exe') """
    name = get_file_name(path)
    return os.path.splitext(name)


def main():
    path = os. getcwd()
    print(f'Folders list under path:{path}:')
    for i in traverse_folders(path):
        print(i)

    print(f'folders and subfolders list under path:{path}:')
    for i in traverse_folders(path, True):
        print(i)

    print(f'Files list under path:{path}:')
    for i in traverse_files(path, filters='txt py csv'):
        print(i)

    file = os.path.join(path, 'abc.txt')
    print('file=', file)
    print('file_name=', get_file_name(file))
    names = get_file_names(file)
    print('names=', names)


if __name__ == "__main__":
    main()
