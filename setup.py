from setuptools import setup, find_packages

setup(
    name="uds_connect",                    # Name of the package
    version="0.1.0",                       # Package version
    description="A package to interface with UDS via different CAN interfaces",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/uds_connect",  # URL of the project's GitHub repo
    license="MIT",                         # License type
    packages=find_packages(),              # Automatically find package directories
    install_requires=[
        "uds",                             # Specify any dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",               # Python version requirement
)