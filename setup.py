from setuptools import find_packages, setup

setup(
    name="libcovebods",
    version="0.15.0",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/openownership/lib-cove-bods",
    description="A data review library",
    packages=find_packages(),
    long_description="A data review library",
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil",
        "libcove2",
        "packaging",
        # Jsonschema 4.10 breaks the message
        #     'missingPersonType' is a dependency of 'missingPersonReason'
        # in tests/fixtures/0.1/badfile_all_validation_errors.json
        "jsonschema<4.10",
        "pytz",
        "ijson",
        # Required for jsonschema to validate URIs
        "rfc3987",
        # Required for jsonschema to validate date-time
        "rfc3339-validator",
    ],
    extras_require={"dev": ["pytest", "flake8", "black==22.3.0", "isort", "mypy"]},
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    entry_points="""[console_scripts]
libcovebods = libcovebods.cli:main""",
    include_package_data=True,
)
