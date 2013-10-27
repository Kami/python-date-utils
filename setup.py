import os
import sys

from os.path import join as pjoin

from setuptools import setup


def read_version_string():
    version = None
    sys.path.insert(0, pjoin(os.getcwd()))
    from date_utils import __version__
    version = __version__
    sys.path.pop(0)
    return version


def forbid_publish():
    argv = sys.argv
    blacklist = ['register', 'upload']

    for command in blacklist:
        if command in argv:
            values = {'command': command}
            raise RuntimeError('Command "%(command)s" has been blacklisted' %
                               values)

forbid_publish()


with open('requirements.txt', 'r') as fp:
    content = fp.read().strip()
    requirements = content.split('\n')


setup(
    name='date-utils',
    version=read_version_string(),
    #long_description=open('README.rst').read() + '\n\n' +
    #open('CHANGES.rst').read(),
    packages=[
        'date_utils'
    ],
    install_requires=requirements,
    url='https://github.com/Kami/python-date-utils/',
    license='Apache License (2.0)',
    author='Tomaz Muraus',
    author_email='tomaz+pypi@tomaz.me',
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
