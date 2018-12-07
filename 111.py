# def str_to_int(string):
#     if not string:  # 空字符返回异常
#         raise Exception('string cannot be None', string)
#     flag = 0  # 用来表示第一个字符是否为+、-
#     ret = 0  # 结果
#     for k, s in enumerate(string):
#         if s.isdigit():  # 数字直接运算
#             val = ord(s) - ord('0')
#             ret = ret * 10 + val
#         else:
#             if not flag:
#                 if s == '+' and k == 0:  # 避免中间出现+、-
#                     flag = 1
#                 elif s == '-' and k == 0:
#                     flag = -1
#                 else:
#                     raise Exception('digit is need', string)
#             else:
#                 raise Exception('digit is need', string)
#     if flag and len(string) == 1:  # 判断是不是只有+、-
#         raise Exception('digit is need', string)
#     return ret if flag >= 0 else -ret
#
#
# if __name__ == '__main__':
#     print(type(ord('1') - ord('0')))
#     print(int('1'))


from threading import Thread
import time
from time import sleep, ctime


# def my_counter():
#     for i in range(2):
#         n = i + 1
#     sleep(1)
#     return n
#
#
# def main():
#     thread_array = {}
#     start_time = time.time()  # 开始计时
#     for tid in range(2):
#         t = Thread(target=my_counter)  # 线程中执行my_counter函数
#         t.start()
#         print("%s is running thread No.%d" % (ctime(), tid + 1))
#         t.join()  # 等待到该线程结束，才开始执行下一个线程
#         print("%s thread No.%d ended" % (ctime(), tid + 1))
#         sleep(1)
#     end_time = time.time()  # 结束计时
#
#     print("Total time:{}".format(end_time - start_time))
#
#
# from threading import Thread
# import time
# from time import ctime, sleep
#
#
def my_counter():
    for i in range(2):
        i += 1
    sleep(1)
    return True


def main():
    thread_array = []
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        thread_array.append(t)
        print("%s is running thread_array[%d]" % (ctime(), tid))
    for i in thread_array:
        i.start()
        i.join()
        print("%s %s ended" % (ctime(), i))
    end_time = time.time()
    print("Total time:{}".format(end_time - start_time))


if __name__ == '__main__':
    main()
