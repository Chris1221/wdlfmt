from setuptools import setup

setup(
    name="wdlformat",
    version="0.1",
    description="Formatter for WDL files",
    author="Chris Cole",
    author_email="chris.c.1221@gmail.com",
    entry_points={
        "console_scripts": [
            "wdlformat = wdlformat.cli:cli",
        ],
    },
    packages=["wdlformat"],  # same as name
)
