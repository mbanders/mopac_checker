

from setuptools import find_packages, setup

setup(
    name="mopac",
    version="0.9",
    description="Check Mopac Fast Lane Prices",
    author="Michael Anderson",
    url="https://github.com/mbanders/mopac_checker",
    packages=find_packages(),
    package_data={"": ["*.txt", "*.json", "*.cfg", "*.md"]},
    include_package_data=True,
    entry_points={"console_scripts": ["mopac=mopac.mopac:main"],},
)
