from setuptools import setup, find_packages

setup(
        name='perSky',
        version='0.1.0',
        description='Performance Skyline python package to visualize event logs (from process mining) performance',
        author = 'Andrea Maldonado',
        author_email='andreamalher.works@gmail.com',
        packages=find_packages(),
        install_requires=['pytest', 'py4pm']
        )