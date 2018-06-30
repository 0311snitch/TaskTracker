from setuptools import setup

packages = ['console', 'console.parser_api', 'console.presentations']

setup(
    name='task_tracker',
    version='0.1',
    author='sad_snitch',
    author_email='0311snitch@gmail.com',
    packages=packages,
    description='console part of Takinata',
    include_package_data=False,
    install_requires=['tasklib==0.1'],
    entry_points={
        'console_scripts':
            ['task_tracker = console.start:main']
    }
)
