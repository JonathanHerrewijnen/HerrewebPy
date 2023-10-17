from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# Parse the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = [str(req) for req in parse_requirements(f.read())]

setup(
    name='herrewebpy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={},
)
