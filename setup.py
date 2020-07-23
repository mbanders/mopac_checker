

from setuptools import find_packages, setup

setup(
    name="mopac",
    version="0.9",
    python_requires='>3.5.0',
    description="Check Mopac Fast Lane Prices",
    author="Michael Anderson",
    url="https://github.com/mbanders/mopac_checker",
    packages=find_packages(),
    package_data={"": ["*.txt", "*.json", "*.cfg", "*.md"]},
    include_package_data=True,
    install_requires=['requests', 'pytz'],
    entry_points={"console_scripts": ["mopac=mopac.mopac:main"],},
)
