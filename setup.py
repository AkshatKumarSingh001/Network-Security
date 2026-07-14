'''
The setup.py file is an essential part of packaging and distributing Python projects.
It is used by setup tools (or distutils in older Python versions) to define the configurtion of your project,
such as its metadata, dependencies, and more.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function will return list of requirements
    
    """

    requirement_list: List[str] = []
    try:
        with open('requirements.txt') as f:
            # Read lines from the file
            lines = f.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")
    return requirement_list

    return requirement_list

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author = "Akshat Kumar Singh",
    author_email = "akshatsingh360@gmail.com",
    packages = find_packages(), # find_packages() is responsible for automatically discovering all packages and sub-packages in your project directory.
    install_requires = get_requirements('requirements.txt') # install_requires specifies the dependencies that need to be installed for your project to work correctly. It uses the get_requirements function to read the dependencies from the requirements.txt file.
    
)
