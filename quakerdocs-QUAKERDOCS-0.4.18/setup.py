# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(
    name="quakerdocs-QUAKERDOCS",
    version = "0.4.18",
    description = "Static Documentation Generator",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    entry_points={
        'console_scripts': [
            'quaker=quaker:main',
        ],
    },
    url = "https://www.quakerdocs.nl/",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.8",
    packages = find_packages("src"),  # include all packages under src
    package_dir = {"quaker": "src/quaker", "quaker_lib": "src/quaker_lib"},
    include_package_data = True,
    package_data = { "quaker_lib": ["static/*", "wasm/*"] }
)