try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup

with open('README.md') as f:    
	readme = f.read()

with open('LICENSE.txt') as f:    
	license = f.read()	
	
setup(
	name = 'waterapputils',
	version = '1.0.0',
	description = 'Read, process, write, and plot hydrologic data from the USGS Kentucky Water Science Center WATER application developed by Williamson, T., Ulery, R. and Newson, J.',
	long_description = readme,
	author = 'Jeremiah Lant',
	author_email = 'jlant@usgs.gov',
	url = 'https://github.com/jlant-usgs/waterapputils',
	license = license,
	packages = find_packages()
	)
