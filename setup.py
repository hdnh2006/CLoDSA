# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

def get_requirements():
    with open(path.join(here,'requirements.txt')) as f:
        return f.read().splitlines()

setup(
    name='clodsa',  # Required
    version='1.2.48',  # Required
    description='Image augmentation for classification, localization, detection and semantic segmentation',
    url='https://github.com/hdnh2006/CLoDSA',
    author='Henry Navarro, forked from Jonathan Heras (https://github.com/hdnh2006/CLoDSA)',
    author_email='contact@henrynavarro.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='image augmentation, classification, localization, detection, semantic segmentation',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=get_requirements(),
    entry_points={ 
        'console_scripts': [
            'clodsa=clodsa.command_line:main',
            'clodsa-sample=clodsa.command_line:main_sample',
        ],
    },
)
