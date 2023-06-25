# -*- encoding: utf-8 -*-
# Date: 27/Apr/2020
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Module for path, file oeprations
"""

import os


def traverse_folders(path, recursive=False):
    """ Traverse the folders under the path """
    for dirpath, dirnames, _ in os.walk(path):
        dirnames.sort()
        for dirname in dirnames:
            yield os.path.join(dirpath, dirname)
        if not recursive:
            break


def traverse_files(path, extensions='', recursive=False):
    """ Traverse the files under the path

    Args:
        path (str): path
        extensions (str, optional): File extensions filters, e.g. 'cpp h txt jpg'. Defaults to ''.
        recursive (bool, optional): Whether to traverse recursively. Defaults to False.
    """

    if extensions:
        extensions = set(extensions.split())

    for dirpath, _, filenames in os.walk(path):
        filenames.sort()
        for filename in filenames:
            ext = os.path.splitext(filename)[1][1:]
            if not extensions or ext in extensions:
                yield os.path.join(dirpath, filename)
        if not recursive:
            break


def exists_file(file):
    """ if file exists """
    return os.path.exists(file)


def delete_file(file_path):
    """
    Deletes a file if it exists.

    Args:
        file_path (str): The path of the file to be deleted.
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def create_path(dirs):
    """
    Creates a directory if it does not exist.

    Args:
        dirs (str): The path of the directory to be created.
    """
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def join_path(dirs, sub):
    """
    Joins two paths to create a new path.

    Args:
        dirs (str): The first part of the path.
        sub (str): The second part of the path.

    Returns:
        str: The joined path.
    """
    return os.path.join(dirs, sub)


def abs_path(dirs):
    """ get absolute path """
    return os.path.abspath(dirs)


def real_path(dirs):
    """ get real path """
    return os.path.realpath(dirs)


def dir_path(path):
    """ get file folder """
    return os.path.dirname(path)


def delete_folder(file_path):
    """ delete folder """
    if os.path.exists(file_path):
        for file in os.scandir(file_path):
            if file.is_file():
                os.remove(file.path)


def get_file_name(file):
    """get basename, 'name.exe' 'x.zip' """
    return os.path.basename(file)


def get_file_names(file):
    """get split names, 'name.exe'--> tuple('name', '.exe') """
    name = get_file_name(file)
    return os.path.splitext(name)


def get_file_extension(file):
    """ get extension """
    return get_file_names(file)[1]


def file_size(file):
    """ get file size """
    return os.path.getsize(file)  # file size in bytes


def readable_file_size(size, decimal_places=2):
    """ convert bytes number to readable str """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def main():
    """ main function """
    path = os. getcwd()
    print(f'\nFolders list under path: {path}:')
    for i in traverse_folders(path):
        print(i)

    print(f'\nfolders and subfolders list under path: {path}:')
    for i in traverse_folders(path, True):
        print(i)

    print(f'\nFiles list under path: {path}:')
    for i in traverse_files(path, extensions='txt py csv'):
        print(i)

    print(f'\nFiles list recursive under path: {path}:')
    for i in traverse_files(path, extensions='txt py csv', recursive=True):
        print(i)

    print('\n')
    file = join_path(path, 'abc.txt')
    print('file=', file)
    print('file_name=', get_file_name(file))
    print('names=', get_file_names(file))
    print('extension=', get_file_extension(file))

    realpath = real_path(__file__)
    directory = dir_path(realpath)
    print('__file__=', __file__)
    print('realpath=', realpath)
    print('directory=', directory)
    print('x realpath=', real_path('common_path.py'))
    print('x abs realpath=', abs_path('common_path.py'))
    print('file size: ', file_size(realpath), 'bytes')
    print('file size readable: ', readable_file_size(file_size(realpath)))


if __name__ == "__main__":
    main()
