from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='uniprot-taxonomy',
    version='0.1.0',
    author='Victor Lin',
    author_email='vlin@ufl.edu',
    url='https://github.com/zhoulab/uniprot-taxonomy',
    description='get organism taxonomy information from http://uniprot.org',
    long_description=readme(),
    py_modules=['uniprot_taxonomy']
)
