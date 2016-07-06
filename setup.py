# coding: utf-8
#
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup


#
setup(
    name='AoikRegistryEditor',

    version='0.1.0',

    description="""A customizable registry editor.""",

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikRegistryEditor>`_""",

    url='https://github.com/AoiKuiyuyou/AoikRegistryEditor',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='registry editor',

    package_dir={
        '': 'src'
    },

    package_data={
        'aoikregistryeditor.static': [
            '*.png',
        ],
    },

    packages=find_packages('src'),

    entry_points={
        'console_scripts': [
            'aoikregistryeditor=aoikregistryeditor.aoikregistryeditor:main',
        ],
    },
)
