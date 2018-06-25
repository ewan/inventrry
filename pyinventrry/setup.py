import os
from setuptools import setup, Command

class CleanCommand(Command):
	"""Custom clean command to tidy up the project root."""
	user_options = []
	def initialize_options(self):
		pass
	def finalize_options(self):
		pass
	def run(self):
		os.system('rm -vrf ./build ./dist ./*.pyc  ./*.egg-info')

# Further down when you call setup()
setup(
	cmdclass={ 'clean': CleanCommand},
	name='pyinventrry',
	version='1',
	description='In progress',
	url='http://github.com/ewan/inventry',
	author='Ewan DUNBAR & Sebastien GADIOUX',
	author_email='',
	license='',
	packages=['pyinventrry','pyinventrry.score'],
	entry_points={'console_scripts' : 
		['calculate_score=pyinventrry.scoreCalcule:main',
		'calculate_specs=pyinventrry.spec:main',
		'calculate_time_specs=pyinventrry.spec_timer:main',
		'clean_inventory=pyinventrry.clean:main']},
	zip_safe=False
)
