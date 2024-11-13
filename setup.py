from setuptools import setup, find_packages

setup(
    name="Chimera",
    version="0.1.0",
    author="38c",
    author_email="chimera@38c.xyz",
    description="Scratch API library, can authenticate through session and access cloud variables.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/38c1/Chimera/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "websocket-client",
        "requests"
    ],
)
