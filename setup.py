from setuptools import setup, find_packages

setup(
    name='libcovebods',
    version='0.6.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    url='https://github.com/open-contracting/lib-cove-ocds',
    description='A data review library',
    packages=find_packages(),
    long_description='A data review library',
    install_requires=[
        'rfc3987',
        'strict-rfc3339',
        'Django>1.11.23,<1.12',
        'python-dateutil',
        'libcove>=0.13.0'
    ],
    classifiers=[
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    entry_points='''[console_scripts]
libcovebods = libcovebods.cli.__main__:main''',
    include_package_data=True,
)
