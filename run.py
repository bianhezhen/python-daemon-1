#!/usr/bin/env python
#encoding:utf8
import sys
from daemon import Daemon
 
class MyDaemon(Daemon):
    def run(self):
        while 1:
            pass

if __name__ == "__main__":
   daemon = MyDaemon('/tmp/test.pid')
   daemon.handle()
