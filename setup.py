from setuptools import find_packages, setup

setup(
    name="libcovebods",
    version="0.14.0",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/openownership/lib-cove-bods",
    description="A data review library",
    packages=find_packages(),
    long_description="A data review library",
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil",
        "packaging",
        "ijson",
        # Jsonschema 4.10 breaks the message
        #     'missingPersonType' is a dependency of 'missingPersonReason'
        # in tests/fixtures/0.1/badfile_all_validation_errors.json
        "jsonschema<4.10",
        "pytz",
        # These should be in libcove2
        "requests",
    ],
    extras_require={"dev": ["pytest", "flake8", "black==22.3.0", "isort"]},
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    entry_points="""[console_scripts]
libcovebods = libcovebods.cli.__main__:main""",
    include_package_data=True,
)
