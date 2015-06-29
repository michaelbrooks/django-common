from setuptools import setup

setup(
    name='django-mb-core',
    version='0.1.0',
    packages=['mbcore',],
    url='https://github.com/michaelbrooks/django-mb-core',
    license='MIT',
    author='Michael Brooks',
    author_email='mjbrooks@uw.edu',
    description='Base package for django apps',
    install_reqs=[
        "Fabric >= 1.10, <1.11",
        "path.py >= 7.3, < 7.4",
    ],
)
