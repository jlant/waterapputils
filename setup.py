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
	description = 'Process simulations from a hydrologic model and apply water use and global circulation model deltas to model simulations.',
	long_description = readme,
	author = 'Jeremiah Lant',
	author_email = 'jlant@usgs.gov',
	url = 'https://github.com/jlant-usgs/waterapputils',
	license = license,
	packages = find_packages()
	)
