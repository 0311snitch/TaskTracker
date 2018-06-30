from setuptools import setup, find_packages

packages = ['lib','lib.controllers','lib.models','lib.storage_controller']

setup(
    name='tasklib',
    version='0.1',
    author='sad_snitch',
    author_email='0311snitch@gmail.com',
    packages=packages,
    description='library part of Takinata',
    include_package_data=False)
