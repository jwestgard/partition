from setuptools import find_packages, setup

setup(
    name='partition',
    version='0.1',
    description='Command-line file partitioning tool.',
    author='Joshua A. Westgard',
    author_email="westgard@umd.edu",
    platforms=["any"],
    license="BSD",
    url="http://github.com/jwestgard/partition",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['preserve=preserve.__main__:main']
        },
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
