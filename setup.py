from os.path import dirname, join
from setuptools import setup, find_packages

from streamitem import __version__ as version

setup(
    name='scrapy-streamitem',
    version=version,
    url='http://scrapy.org',
    description='Scrapy support for working with streamcorpus Stream Items',
    author='Scrapy developers',
    maintainer='scrapinghub',
    maintainer_email='javier@scrapinghub.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Scrapy>=0.22.0',
        'streamcorpus',
    ],
)
