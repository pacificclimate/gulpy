from setuptools import setup, find_packages

__version__ = (0, 0, 1)

setup(
    name="gulpy",
    description="Utility to import bulk data into PCIC's CRMP",
    keywords="sql database data science climate oceanography meteorology",
    version='.'.join(str(d) for d in __version__),
    url="http://www.pacificclimate.org/",
    author="Basil Veerman",
    author_email="bveerman@uvic.ca",
    packages=find_packages(),
    scripts = ["scripts/import_bch_flat.py"],
    install_requires = ['pycds'],
    )
