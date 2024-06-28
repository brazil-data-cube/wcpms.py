import os
from setuptools import find_packages, setup

DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR, "VERSION"), "r") as file:
    VERSION = file.read()

with open(os.path.join(DIR, "README.rst"), "r") as file:
    LONG_DESCRIPTION = file.read()

long_description = LONG_DESCRIPTION,

setup(
    name='wcpms',
    packages=find_packages(),
    include_package_data=True,
    version = VERSION,
    description='Python Client of the Web Crop Phenological Metrics Service for Earth Observation Data Cubes',
    author='Gabriel Sansigolo',
    author_email = "gabrielsansigolo@gmail.com",
    url = "https://github.com/GSansigolo/wcpms.py",
    install_requires= [
        "urllib3==2.2.2",
        "requests==2.32.3",
        "pandas==2.2.2",
        "matplotlib==3.9.0",
        "scipy==1.13.1",
        "datetime==5.5"
    ],
    long_description = LONG_DESCRIPTION,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
