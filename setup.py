import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name='AltAzRange',
  packages=['AltAzRange'],
  version='0.57',
  license='MIT',
  author='SQ3TLE',
  author_email='sq3tle@gmail.com',
  description='Simple tool to get altitude (elevation), azimuth and range between observer and object / pair of '
              'cordinates',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/sq3tle/altazrange',
  keywords=['altitude', 'elevation', 'azimuth', 'distance', 'gps', 'satellite'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ])
