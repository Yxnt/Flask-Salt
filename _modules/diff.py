#!/usr/bin/env python
# -*- coding:utf-8 -*-

from os import listdir, path, remove, mkdir, walk, rmdir
from hashlib import md5
import shutil
import redis
import json

__outputter__ = { __name__: 'json'}


def _loop(dire, ret=None):
    """遍历目录
    :param dire: 指定目录名称
    :param ret: 结果保存值
    :return: None
    """

    if path.exists(dire) is not True:
        mkdir(dire)

    for i in listdir(dire):
        file_name = path.join(dire, i)
        if path.isdir(file_name):
            _loop(file_name, ret)
        else:
            if ret is not None:
                res = file_name.replace('\\', '/').split('/')
                if res[3] == res[-1]:
                    ret.add(res[3])
                else:
                    res = '/'.join(res[3:])
                    ret.add(res)


def _md5ret(obj):
    """md5值获取
    :param obj: 文件路径
    :return: 文件对应的md5码
    """

    md5obj = md5()
    with open(obj, 'rb') as f:
        md5obj.update(f.read())

    return md5obj.hexdigest()


def diff(src, dst):
    """对比两个目录下的文件
    如果源目录下有目标目录下没有则复制，反之则删除。
    如果源目录和目标目录都有则判断md5是否相同，不同则覆盖
    :param src: 源目录
    :param dst: 目标目录
    :return: 具体操作的文件列表
    """
    pool = redis.ConnectionPool(
        host='',
        port='',
        db=None,
        password=''
    )
    r = redis.Redis(connection_pool=pool)
    filelist = set([i.encode('utf8') for i in json.loads(r.get('salt:publish:salt:save_res'))])

    ret = []
    src_list = set()
    dst_list = set()


    _loop(src, src_list)
    _loop(dst, dst_list)

    oper = src_list - filelist
    for i in oper:
        remove(path.join(src,i))
        src_list.remove(i)

    exp = src_list - dst_list

    if exp:
        for i in exp:
            src_file = path.join(src, i).replace('\\', '/')
            dst_file = path.join(dst, i).replace('\\', '/')
            src_dirname = path.dirname(src_file)
            dst_dirname = path.dirname(dst_file)

            if path.exists(dst_dirname):
                shutil.copy2(src_file, dst_file)
                ret.append(src_file)
            else:
                shutil.copytree(src_dirname, dst_dirname)
    else:
        exp = dst_list - src_list
        if exp:
            for i in exp:
                dst_file = path.join(dst, i).replace('\\', '/')
                remove(dst_file)
                ret.append(dst_file)
                if sum(len(files) for root, dirs, files in walk(path.dirname(dst_file))) == 0:
                    rmdir(path.dirname(dst_file))

    ret_list = src_list & dst_list
    for i in ret_list:
        src_hash = _md5ret(path.join(src, i))
        dst_hash = _md5ret(path.join(dst, i))
        if src_hash != dst_hash:
            shutil.copy2(path.join(src, i), path.join(dst, i))
            ret.append(path.join(dst, i))

    return ret


if __name__ == '__main__':
    print(diff(r'D:\test\HGSQ.Business.Detail', r'D:\test\HGSQ.Business.Detail1'))
