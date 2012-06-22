#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, atexit, datetime
from signal import SIGTERM, SIG_DFL
import logging as log

class Daemon:
    """
    Родительский класс для реализации демона
    Использование: Наследоваться от класса и реализовать метод run()
    """
    def __init__(self, pidfile, chroot=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', log_level='ERROR'):
        LOG_LEVEL = {'DEBUG': log.DEBUG,
                     'INFO': log.INFO,
                     'WARNING': log.WARNING,
                     'ERROR': log.ERROR,
                     'CRITICAL': log.CRITICAL}
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.chroot = chroot
        log.basicConfig(filename='daemon.log', level=LOG_LEVEL[log_level],
            format='%(asctime)s [%(levelname)s] %(message)s')

    def get_pid(self):
        """
        Метод проверяет наличие PID-файла и пингует процесс,
        посылая ему SIG_DFL
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            try:
                os.kill(pid, SIG_DFL)
                return pid
            except OSError, err:
                err = str(err)
                if err.find("No such process") > 0:
                    sys.stderr.write("Daemon is not responding. PID-file exist. Starting post_stop().\n")
                    self.post_stop()
                    return 0

    def demonize(self):
        """
        Метод, выполняющий демонизацию процесса через double-fork
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("First fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        if self.chroot:
            try:
                os.chroot(self.chroot)
            except Exception, e:
                log.critical('Chroot in %s error: %s' % (self.chroot, e.strerror))

        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Second fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.post_stop)
        pid = str(os.getpid())
        log.info('Process PID: %s' % pid)
        file(self.pidfile, 'w+').write("%s\n" % pid)
        log.debug('PID-file %s created' % self.pidfile)

    def post_stop(self):
        """
        Метод выполняется при нормальном завершении работы демона
        """
        os.remove(self.pidfile)
        log.debug('Delete PID-file')

    def start(self):
        """
        Метода стартует работу демона
        """
        pid = self.get_pid()
        if pid > 0:
            sys.stderr.write("Daemon already running on PID: %d\n" % pid)
        else:
            log.info('Starting...')
            self.demonize()
            log.debug('Start success')
            self.run()

    def stop(self):
        """
        Метод выполняет остановку демона посылая ему SIGTERM
        """
        pid = self.get_pid()
        if pid > 0:
            os.kill(pid, SIGTERM)
            log.info('Stop programm')
            self.post_stop()
        else:
            sys.stderr.write("Daemon not running\n")

    def restart(self):
        """
        Метод перезапускает демон
        """
        log.info('Restarting...')
        self.stop()
        self.start()

    def handle(self, argv=sys.argv):
        """
        Метод принимет аргументы командной строки и запускает соответствующие методы класса
        """
        if len(argv) == 2:
            if 'start' == argv[1]:
                self.start()
            elif 'stop' == argv[1]:
                self.stop()
            elif 'restart' == argv[1]:
                self.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "Use: %s start|stop|restart" % argv[0]
            sys.exit(2)

    def run(self):
        """
        Этот метод нужно реализовать. Он вызывается в методе start() после demonize()
        """

