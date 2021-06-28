#!/usr/bin/env python

import setuptools

application_dependencies = ["api-client>=1.3.1"]
prod_dependencies = []
test_dependencies = ["pytest", "pytest-env", "pytest-cov", "vcrpy", "requests-mock"]
lint_dependencies = ["flake8", "flake8-docstrings", "black", "isort"]
docs_dependencies = []
dev_dependencies = test_dependencies + lint_dependencies + docs_dependencies + ["ipdb"]
deploy_dependencies = ["requests", "twine"]


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("VERSION", "r") as buf:
    version = buf.read()


setuptools.setup(
    name="nordigen-python",
    version=version,
    description="Clinet lib for integration with Nordigen banking API's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carl Sutton (dogmatic69)",
    author_email="dogmatic69@gmail.com",
    license='MIT',
    keywords = ['nordigen', 'banking', 'PSD2'],
    url="https://github.com/dogmatic69/nordigen-python",
    python_requires=">=3.6",
    packages=["nordigen"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    install_requires=application_dependencies,
    extras_require={
        "production": prod_dependencies,
        "test": test_dependencies,
        "lint": lint_dependencies,
        "docs": dev_dependencies,
        "dev": dev_dependencies,
        "deploy": deploy_dependencies,
    },
    include_package_data=True,
    zip_safe=False,
)