from setuptools import setup, find_packages

setup(
    name='website-doc-extractor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'extract-docs=src.extractor:main',
        ],
    },
)
