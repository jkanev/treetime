
#!/usr/bin/env python

from distutils.core import setup

setup (
    name='TreeTime',
    version='0.1',
    description='TreeTime is a to-do list manager, test report tool, project manager, family ancestry editor, mind-mapping tool, etc. Using TreeTime you can categorise and organise your data items in tree structures. You can define several trees at the same time, each with a different structure, but on the same data.You can use functions (calculate sums, ratios and means) recursively up the branches of a tree. ',
    author='Jacob Kanev',
    author_email='jkanev@zoho.com',
    url='https://github.com/jkanev/treetime',
    packages=['treetime'],
    package_data={'treetime': ['data/items.trt', 'doc/*.png']},
)