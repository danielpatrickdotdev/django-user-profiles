#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-user-profiles',
    version="0.1",
    author='Danny Patrick',
    author_email='danieljudepatrick@gmail.com',
    description='Just a custom user profile application',
    #url='http://github.com/...',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Me",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
