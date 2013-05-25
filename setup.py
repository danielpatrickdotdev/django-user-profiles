#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-user-profiles',
    version="0.1",
    author='Danny Patrick',
    author_email='danieljudepatrick@gmail.com',
    description='Custom user profile',
    url='http://github.com/remarkablerocket/django-user-profiles',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
)
