from setuptools import setup, find_packages

setup(
    name='geni',
    version='0.1.0',
    description='Python client library for the Geni.com public REST API',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/geni',
    # package_dir={"": "."},  # Root directory is the source root
    packages=find_packages(where=".", exclude=("tests*", "examples*")),
    install_requires=[
        # Add runtime dependencies here, e.g.,
        # 'requests>=2.28.0'
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





# setup(
#     name="geni",
#     version="0.1.0",
#     packages=["geni"],
#     package_dir={"": "."},  # Root package is in `src`
#     include_package_data=True,  # Include data files listed in MANIFEST.in
#     python_requires=">=3.7",  # Specify the minimum Python version
#     install_requires=[],  # Add runtime dependencies here if needed
# )

# from setuptools import setup, find_packages

# setup(
#     name="geni",
#     version="0.1.0",
#     author="Your Name",
#     author_email="your.email@example.com",
#     description="A brief description of your library",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/yourusername/geni",  # Replace with your project's URL
#     packages=find_packages(where="src"),
#     # packages=["src"],
#     package_dir={"": "src"},
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",  # Change the license if needed
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.7",
#     install_requires=[
#         # List your library's dependencies here, e.g., 'requests>=2.0.0',
#     ],
#     extras_require={
#         "dev": [
#             "pytest>=6.0",
#             # "pytest-cov",
#             # "flake8",
#             # "black",
#         ],
#     },
#     test_suite="tests",
#     include_package_data=True,
#     # entry_points={
#     #     "console_scripts": [
#     #         # Uncomment and add any CLI scripts here if your library has them
#     #         # "geni-cli=geni.cli:main",
#     #     ],
#     # },
# )
