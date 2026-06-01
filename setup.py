#!/usr/bin/env python
"""Setup script for helpdesk-lite."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("helpdesk/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="helpdesk-lite",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A minimal internal ticketing system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR-USERNAME/helpdesk_lite",
    project_urls={
        "Bug Tracker": "https://github.com/YOUR-USERNAME/helpdesk_lite/issues",
        "Documentation": "https://github.com/YOUR-USERNAME/helpdesk_lite",
        "Source Code": "https://github.com/YOUR-USERNAME/helpdesk_lite",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "helpdesk=helpdesk.server.main:app",
        ],
    },
)
