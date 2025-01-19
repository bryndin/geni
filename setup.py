from setuptools import setup, find_packages

setup(
    name='geni',
    version='0.1.0',
    description='Python client library for the Geni.com public REST API',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Dmitry Bryndin',
    url='https://github.com/bryndin/geni',
    packages=find_packages(where=".", exclude=("tests*", "examples*")),
    install_requires=[
        # Add runtime dependencies here, e.g.,
        'requests>=2.28.0'
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "pytest>=8.3.4",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
