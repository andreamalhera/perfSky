from setuptools import setup

# TODO: Pytest is currently not callable twice with docker-compose 
# since cache cannot be emptied from outside of the container and 
# it blocks any build after py.test.
setup(
        name='processmining',
        version='1.0',
        description='LMU Master Thesis: Process Mining 2019-2020',
        author = 'Andrea Maldonado',
        author_email='andrea.maldonado@trustyou.net',
        packages=[],
        install_requires=['pytest', 'py4pm', 'flake8']
        )