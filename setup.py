
#!/usr/bin/env python

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='TreeTime',
    version='2021.5',
    description='TreeTime is a to-do list manager, test report tool, project manager, family ancestry editor,'
                'mind-mapping tool, etc. Using TreeTime you can categorise and organise any data in tree structures.'
                'You can define several trees, each with a different structure, on the same data. You can use functions'
                '(sums, ratios and means) recursively up the branches of a tree.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jacob Kanev',
    author_email='jkanev@zoho.com',
    url='https://github.com/jkanev/treetime',
    packages=['treetime'],
    package_dir={'treetime': 'treetime'},
    include_package_data=True,
    entry_points={'gui_scripts': ['treetime = treetime.__main__:main']},
    package_data={'treetime': ['../data/Simple-Task-List.trt', '../data/treetime-logo.png', '../docs/*.png']},
    exclude_package_data={'treetime': ['treetime/compile-ui.py',]},
    # according to some people on the web install_requiring PyQt5 should work, but as my system gives me an error for
    # this, I'll comment it out. Please install it separately (pip3 PyQt5 apparently works)
    # install_requires=['PyQt5'],
)
