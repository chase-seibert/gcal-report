import os
from setuptools import setup, find_packages

install_requires = []

cwd = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(cwd, 'requirements.txt'), 'r') as f:
    install_requires.extend(l.strip() for l in f.readlines())

setup(
    name='gcal-report',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=install_requires,
    include_package_data=True,
    author='Chase Seibert',
    author_email='chase.seibert+gcal@gmail.com',
    license='Other/Proprietary License',
    description='Generate a report on team and individual Google Calendar metting hours',
    long_description='',
    url='https://github.com/chase-seibert/gcal-report',
    entry_points={
        'console_scripts': ['gcal-report=gcal_report.console:main'],
    },
)
