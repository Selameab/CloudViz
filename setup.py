import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='CloudViz',
    version='0.0.1',
    description='',
    url='https://github.com/Selameab/CloudViz',
    author='Selameab S. Demilew',
    author_email='selameab@demilew.com',

    packages=['cloudviz'],

    install_requires=requirements,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
