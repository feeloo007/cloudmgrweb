VERSION = '0.0.1'

from setuptools import setup, find_packages

setup(
      name = 'cloudmgrweb',
      version = 0.1,
      author = 'Philippe GONCALVES',
      author_email = 'philippe.goncalves@paris.fr',
      description = '',
      license = '',
      keywords = '',
      url = '',
      packages = find_packages(),
      include_package_data = True,
      package_data = {'' : ['*.cfg']},
      zip_safe = False,
      install_requires = ('nagare',),
      entry_points = """
      [nagare.applications]
      cloudmgrweb = cloudmgrweb.app:app
      """
     )
