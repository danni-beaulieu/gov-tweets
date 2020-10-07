  
from setuptools import setup, find_packages

setup(
    name='govtweets',
    version='1.0.0',
    url='https://github.com/nhusar/GovTweets.git',
    author='Nataliya Husar',
    author_email='nhusar@seattleu.edu',
    description='Data Science project: Analysis of Twitter data of the U.S. congressmen',
    packages=find_packages(),    
    install_requires=['wordcloud >= 1.8.0'],
)