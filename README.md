Python Daemon
=============

Introduction
------------
This class allows you easily create UNIX-daemons.

Install
-------
`localhost:~$ pip install -e git+https://github.com/shamanis/python-daemon#egg=python-daemon`

Start-up and use
----------------
All you need to do - extend Daemon class and override method run().

For example:

    import sys
    from daemon import Daemon
    
    class MyDaemon(Daemon):
        def run(self):
            while 1:
                pass
    
    if __name__ == "__main__":
        daemon = MyDaemon('/tmp/test.pid')
        daemon.handle()

As an example of a file `run.py`

* To start: `localhost:~$ python run.py start`

* To stop: `localhost:~$ python run.py stop`

* To restart: `localhost:~$ python run.py restart`

\_\_init\_\_(self, pidfile, chroot=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
----------
Class constructor expects only one parameter - a `pidfile`.

`pidfile` - is absolute path to PID file of the daemon.

`chroot` - absolute path to the directory for chroot.If `chroot=None` chroot is not done.

`stdin` - Standart stream input. Default `/dev/null`

`stdout` - Standart stream output. Default `/dev/null`

`stderr` - Standart stream output for errors. Default `/dev/null`

run(self)
---------
This method must be implemented.

handle(self, argv=sys.argv)
---------------------------
This method handles the command line arguments - sys.argv

