import os
import re
import sys
import subprocess
import shlex
from pathlib import Path
from . import NS_LIST


class ProgressBar():
    '''進度條'''

    def __init__(self, title='Progress', symbol='=', bar_size=50) -> None:
        '''進度表屬性'''
        self.title = title
        self.symbol = symbol
        self.bar_size = bar_size
        self.done = 0  # 迴圈內 使用

    def __call__(self, total: int, done=1, decimal=1, in_loop=False):
        '''
        in_loop: 建立的實體是否在迴圈內使用
        '''
        if in_loop:
            self.done += done
            if self.done >= total:
                self.done = total
            self.__print_progress_bar(self.done, total, decimal)
            if self.done == total:
                self.__done()
        else:
            count = 0
            while True:
                count += done
                if count >= total:
                    count = total
                self.__print_progress_bar(count, total, decimal)
                if count == total:
                    break
            self.__done()

    def __print_progress_bar(self, done, total, decimal):
        '''
        繪製 進度表
        done:完成數
        total:總任務數
        decimal: 百分比顯示到後面幾位
        '''
        # 計算百分比
        precent = float(round(100 * done / total, decimal))
        done_symbol = int(precent / 100 * self.bar_size)
        left = self.symbol * done_symbol
        right = ' ' * (self.bar_size - done_symbol)
        # 顯示進度條
        bar = f"\r{self.title}:[{left}{right}] {format(precent, f'.{decimal}f')}% {done}/{total}"
        sys.stdout.write(bar)
        sys.stdout.flush()

    def __done(self):
        print()


def get_all_files(dir_path, extensions: list, get_relative_path=False):
    """取得所有檔案

    Args:
        dir_path (_type_): 檔案資料夾
        extensions (_type_, optional): 指定副檔名,若無指定則全部列出. 可多個 tar, conf

    Returns:
        _type_: _description_
    """
    target_file_path = []
    path = Path(dir_path).absolute()
    print(path)

    for file in os.listdir(path):

        _, file_extension = os.path.splitext(file)
        if extensions:
            allow_extension = [f'.{e}' for e in extensions]
            if file_extension in allow_extension:
                target_file_path.append(file)
        else:
            target_file_path.append(file)

        # 遞迴
        if os.path.isdir(f'{dir_path}/{file}'):
            sub_dir = f'{dir_path}/{file}'
            files = get_all_files(sub_dir, extensions)
            for file in files:
                if get_relative_path:
                    target_file_path.append(f'{sub_dir}/{file}')
                else:
                    target_file_path.append(file)
    target_file_path.sort()
    return target_file_path


def get_domain_from_nginx_config(conf_name):
    return os.path.splitext(conf_name)[0]


def is_domain(name):
    return re.match(r'.*\..*', name)


def check_ns(domain):
    command = f'dig -t NS {domain} +short'
    # command='dig @ns1.netnames.net www.rac.co.uk +short'
    # command='dig @ns1.netnames.net www.rac.co.uk CNAME'
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    out, err = proc.communicate()  # out, err
    if err:
        return (False, err.decode('utf-8'))
    else:
        r = []
        for i in out.decode('utf-8').split('\n'):
            if i != '':
                r.append(i[:-1])
        return (True, r)


def is_own_ns(ns_list: list):
    for ns in ns_list:
        if ns not in NS_LIST:
            return False
    return True
