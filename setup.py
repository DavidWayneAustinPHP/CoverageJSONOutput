
from setuptools import setup, find_packages

setup(
    name='coveragejson_converter',
    version='1.0.0',
    description='A tool to convert CSV data into CoverageJSON format',
    author='David Austin',
    packages=find_packages(),
    py_modules=['coveragejson_converter'],
    entry_points={
        'console_scripts': [
            'coveragejson-convert=coveragejson_converter:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
