import os
import time


class LogCat:
    @staticmethod
    def log(pos, exceptname, body):
        exceptname = str(exceptname)
        now = time.localtime()
        filename = "/%04d년%02d월%02d일 %02d시%02d분%02d초.txt" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        print('Err Log(', exceptname.split("'")[1],')',filename)
        f = open(os.getcwd() + '//errlog//' + str(filename) + '.txt', 'a')
        filebody = '{:20}\t|\t{:25}\t|\t{:}'.format(pos,exceptname.split("'")[1],body)
        f.write(filebody + "\n")
        f.close()