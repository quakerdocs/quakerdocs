from setuptools import setup, find_packages

# From https://github.com/pypa/pip/issues/7953#issuecomment-645133255
import site
import sys
site.ENABLE_USER_SITE = '--user' in sys.argv[1:]


setup(
    name = "quaker",
    version = "1.0.1",
    description = "Static Documentation Generator",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    entry_points = {
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
    packages = find_packages("src"),
    package_dir = {"": "src"},
    include_package_data = True,
    package_data = {"quaker_lib": ["static/*", "wasm/*", "quickstart/*"]},
    install_requires = [
        "Pygments==2.9.0",
        "docutils==0.17.1",
        "Jinja2==2.10.3"
    ]
)
