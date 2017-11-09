
#!/usr/bin/env python

from setuptools import setup

setup (
    name='TreeTime',
    version='0.1',
    description='TreeTime is a to-do list manager, test report tool, project manager, family ancestry editor,'
                'mind-mapping tool, etc. Using TreeTime you can categorise and organise any data in tree'
                'structures. You can define several trees at the same time, each with a different structure, on the'
                'same data. You can use functions (sums, ratios and means) recursively up the branches of a'
                'tree. ',
    author='Jacob Kanev',
    author_email='jkanev@zoho.com',
    url='https://github.com/jkanev/treetime',
    packages=['treetime'],
    entry_points={'gui_scripts': ['treetime = treetime.__main__:main']},
    package_data={'treetime': ['data/items.trt', 'doc/*.png']},
    # according to some people on the web install_requiring PyQt5 should work, but as my system gives me an error for
    # this, I'll comment it out. Please install it separately (pip3 PyQt5 apparently works)
    # install_requires=['PyQt5'],
)