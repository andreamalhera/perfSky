from setuptools import setup, find_packages

setup(
        name = 'perfSky',
        version = '0.1.0',
        description = 'Performance Skyline python package to visualize event logs (from process mining) performance',
        author = 'Andrea Maldonado',
        author_email = 'andreamalher.works@gmail.com',
        license = 'MIT',
        url='https://github.com/andreamalhera/performanceskyline.git',
        install_requires=[
            'pytest',
            'py4pm',
            'flake8'    #Tool for coding style guide enforcement
            ],
        classifiers=[
            'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Science/Research',      # Define that your audience are developers
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
    ],
)