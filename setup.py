from setuptools import setup

with open('docs/overview.md', 'r') as f:
    desc = f.read()
    skip_start = "[//]: # (INSTALL_BEGIN)"
    skip_end = "[//]: # (INSTALL_END)"
    begin = desc.find(skip_start)
    end = desc.find(skip_end) + len(skip_end)
    desc = desc[:begin] + desc[end:]

setup(
    name='adt-decorators',
    version='0.2.10',
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
