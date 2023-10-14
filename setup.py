from setuptools import setup, find_packages

setup(
    name="pylotus-rpc",              # Replace with your package name
    version="0.1.0",                # Replace with your package version
    description="Python client for interacting with the Lotus JSON-RPC API.",
    long_description="",  # Optional
    url="https://github.com/your_username/your_package",    # Replace with your package's URL
    author="Jason Hudgins",
    author_email="jason@reallybadapps.com",
    license="MIT",                  # Replace with your package's license
    packages=find_packages(),       # Automatically discover and include all packages in the project
    install_requires=[],            # List of package dependencies (if any)
    classifiers=[                   # Optional classifiers to categorize your package on PyPI
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
