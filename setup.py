import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='python-daemon',
    version='0.1',
    author='Petr Bondarenko',
    author_email='public@shamanis.com',
    description=('Class for create UNIX-daemons'),
    license='BSD',
    keywords='unix, daemon'
    url='https://github.com/shamanis/python-daemon',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: BSD License',
        'Operation System :: POSIX',
        'Operation System :: Unix',
        'Programmin Language :: Python',
        'Topic :: Utilites',
    ]
)
