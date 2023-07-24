from setuptools import setup

with open('docs/overview.md', 'r') as f:
    desc = f.read()

setup(
    name='adt-decorators',
    version='0.1.0',    
    description='Algebraic Data Types via Class Decorators',
    long_description=desc,
    long_description_content_type='text/markdown',
    url='https://github.com/m0rphism/adt-decorators',
    author='Hannes Saffrich',
    author_email='saffrich@informatik.uni-freiburg.de',
    license='BSD 2-clause',
    packages=['adt'],
    install_requires=[],

    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
