from setuptools import setup, find_packages

setup(
    name="pylotus-rpc",
    version="0.1.0",
    description="Python client for interacting with the Lotus JSON-RPC API.",
    url="https://github.com/jasonhudgins/pylotus-rpc",
    author="Jason Hudgins",
    author_email="jason@reallybadapps.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "requests==2.31.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
