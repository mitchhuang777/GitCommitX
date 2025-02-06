from setuptools import setup, find_packages

setup(
    name="gitcommitx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "gitcommitx=gitcommitx.cli:app"
        ]
    },
)
