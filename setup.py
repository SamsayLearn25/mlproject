from setuptools import setup, find_packages


from typing import List
HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str)->List:
    requirements = []
    with open(file_path) as f:
        requirements = [line.replace("\n", "").strip() for line in f.readlines() if HYPEN_E_DOT not in line]
    return requirements


setup(
    name="mlproject-pipeline",
    version='0.0.1',
    author_email="samsay.learn25@gmail.com",
    author="Samsay",
    packages=find_packages(),
    install_requires = get_requirements("requirements.txt")
)