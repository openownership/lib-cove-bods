from setuptools import setup, find_packages

setup(
    name='libcovebods',
    version='0.5.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    url='https://github.com/open-contracting/lib-cove-ocds',
    description='A data review library',
    packages=find_packages(),
    long_description='A data review library',
    install_requires=[
        'jsonref',
        'jsonschema<2.7',
        # Required for jsonschema to validate URIs
        'rfc3987',
        # Required for jsonschema to validate date-time
        'strict-rfc3339',
        'CommonMark',
        'Django',
        'bleach',
        'requests',
        'json-merge-patch',
        'cached-property',
        'python-dateutil',
        'flattentool>=0.5.0',
        'libcove>=0.6.0'
    ],
    classifiers=[
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    entry_points='''[console_scripts]
libcovebods = libcovebods.cli.__main__:main''',
    include_package_data=True,
)
