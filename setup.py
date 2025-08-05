"""Setup script for LeetCode CLI Tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="leetcode-cli-tool",
    version="1.0.0",
    author="david1234012",
    author_email="david1234012@gmail.com",
    description="A command-line interface tool for interacting with the LeetCode platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david1234012/leetcode_cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    scripts=["leetcode_cli.py"],
    entry_points={
        "console_scripts": [
            "leetcode-cli=src.cli:main",
        ],
    },
)
