from setuptools import setup, find_packages

setup(
    name="my_twitter",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["my-twitter = my_twitter.cli:main"]},
    install_requires=[],
)
