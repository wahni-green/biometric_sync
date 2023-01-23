from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in biometric_sync/__init__.py
from biometric_sync import __version__ as version

setup(
	name="biometric_sync",
	version=version,
	description="Biometric machine wise attendance marking",
	author="Wahni IT Solution",
	author_email="danyrt@wahni.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
