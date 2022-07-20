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
    python_requires=">=3.6",
    install_requires=[
        "python-dateutil",
        "Django>3.2,<3.3",
        "flattentool>=0.5.0",
        "libcove>=0.22.0",
        "libcoveweb>=0.21.0",
        "packaging",
    ],
    extras_require={"dev": ["pytest", "flake8", "black==22.3.0", "isort"]},
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    entry_points="""[console_scripts]
libcovebods = libcovebods.cli.__main__:main""",
    include_package_data=True,
)
