from setuptools import setup

setup(
    name="wdlfmt",
    version="0.1",
    description="Formatter for WDL files",
    author="Chris Cole",
    author_email="chris.c.1221@gmail.com",
    entry_points={
        "console_scripts": [
            "wdlfmt = wdlfmt.cli:cli",
        ],
    },
    packages=["wdlfmt"],  # same as name
    install_requires=["shfmt-py", "antlr4-python3-runtime==4.12"],
)
