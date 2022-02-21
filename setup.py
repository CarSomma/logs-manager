from setuptools import setup, find_packages
import os

def read_file(fname):
    """helper function to open a local file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='logsmanager',  # distribution name of your package
    version='0.0.1', 
    author='Carmine Somma',
    author_email='carsomma@gmail.com',
	  packages=find_packages(),
    url='', # URL for the homepage of the project it may be a link to the git repo that host your project
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ], # some additional metadata about your package.
    description='Manager of logging',
    #long_description=read_file('README.md'),
    # end-user dependencies for your library
    #install_requires=[
        #'<name-of-required-packake>',
    #],
		
		#package_data= {
    #'<package-name>': ['data/*.csv', 'trained_models/*.pickle']
#}
)