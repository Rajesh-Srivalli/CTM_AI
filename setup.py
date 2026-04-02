from setuptools import setup, find_packages

setup(
    name="python-project",
    version="0.1.0",
    description="A simple Python project",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/python-project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
