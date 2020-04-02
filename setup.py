from setuptools import setup, find_packages

setup(
        name='processmining',
        version='1.0',
        description='LMU Master Thesis: Process Mining 2019-2020',
        author = 'Andrea Maldonado',
        author_email='andrea.maldonado@trustyou.net',
        packages=find_packages(),
        install_requires=['pytest', 'py4pm', 'flake8', 'pyspark']
        )