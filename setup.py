#!/usr/bin/env python
from setuptools import setup

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setup(
    name='xontrib-argcomplete',
    version='0.0.2',
    license='BSD',
    author='anki-code',
    author_email='author@example.com',
    description="Adding support of kislyuk/argcomplete to xonsh.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['argcomplete'],
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    platforms='any',
    url='https://github.com/anki-code/xontrib-argcomplete',
    project_urls={
        "Documentation": "https://github.com/anki-code/xontrib-argcomplete/blob/master/README.md",
        "Code": "https://github.com/anki-code/xontrib-argcomplete",
        "Issue tracker": "https://github.com/anki-code/xontrib-argcomplete/issues",
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Unix Shell",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: BSD License"
    ]
)
