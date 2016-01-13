# coding=utf-8
import time
import threading

from Tkinter import *


class MyThread(threading.Thread):
    def __init__(self, my_win):
        threading.Thread.__init__(self)
        self.my_win = my_win

    def run(self):
        time.sleep(5)
        self.my_win.destroy()


def index():
    print 'hello world'


def show(url):
    win = Tk()
    win.title('图片url')
    win.geometry('600x40')

    btn = Button(win, text='复制', command=index)
    btn.pack(sid=RIGHT)
    text = Text(win)
    text.insert(INSERT, url)
    text.pack(sid=LEFT)

    temp = MyThread(win)
    temp.start()
    win.mainloop()

if __name__ == '__main__':
    show('http://www.runoob.com/python/python-gui-tkinter.html')
