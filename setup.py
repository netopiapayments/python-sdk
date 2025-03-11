from setuptools import setup, find_packages

setup(
    name="netopia-sdk",
    version="2.0.8",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "pyjwt>=2.6.0",
        "cryptography>=39.0.0",
    ],
    include_package_data=True,
    description="NETOPIA Payments Python SDK for integration with the NETOPIA Payments API v2.",
    long_description=open("README.MD", "r").read(),
    long_description_content_type="text/markdown",
    author="NETOPIA Payments",
    author_email="support@netopia.ro",
    url="https://github.com/netopiapayments/python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
