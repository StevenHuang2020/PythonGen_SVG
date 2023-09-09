# -*- encoding: utf-8 -*-
# Date: 09/Jan/2022
# Author: Steven Huang, Auckland, NZ
# License: MIT License
"""
Description: Progressbar GUI
"""
import time
import datetime


class SimpleProgressBar():
    """ Progress bar GUI class """

    def __init__(self, width=50, total=100, title='progress', str_c='=', str_a='>', str_r='.'):
        self._width = width  # bar width
        self._total = total  # total amount
        self._title = title  # title
        self._str_c = str_c  # completed char
        self._str_a = str_a  # arrow char
        self._str_r = str_r  # remainder char
        self._start_time = time.time()  # start time
        self._indent = len(str(self._total))

    def _get_output(self, x, percent):
        pointer = int(self._width * (x / self._total))

        time_elapsed = int(time.time() - self._start_time)
        time_str = str(datetime.timedelta(seconds=time_elapsed))

        remain = self._width - pointer
        if remain == 0:
            str_tmp = f'{self._str_c * (self._width + len(self._str_a))}'
        else:
            str_tmp = f'{self._str_c * pointer}{self._str_a}{self._str_r * remain}'

        return f'{self._title}: {x:{self._indent}}/{self._total} [{str_tmp}] {percent:6.2f}%, time-elapsed: {time_str}'

    def update(self, x):
        if self._total <= 0:
            return

        x = self._total if x > self._total else x
        x = x if x > 0 else 0

        percent = x * 100 / self._total
        print(self._get_output(x, percent), end='\r')
        if percent >= 100:
            print('')


def main():
    """ exapmles """
    N = 50
    pb = SimpleProgressBar(total=N, title='Bar example1')
    for i in range(N):
        pb.update(i + 1)
        time.sleep(0.05)

    pb = SimpleProgressBar(width=30, total=N, title='Bar example2', str_c='#', str_a='->')
    for i in range(N):
        pb.update(i + 1)
        time.sleep(0.05)

    pb = SimpleProgressBar(width=60, title='Bar example3', str_c='-', str_a='', str_r='*')
    for i in range(100):
        pb.update(i + 1)
        time.sleep(0.05)


if __name__ == '__main__':
    main()
