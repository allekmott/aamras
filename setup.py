from setuptools import setup

version = "0.0.1"

with open("README.md", "r") as file_:
    long_description = file_.read()

setup(
    name="aamras",
    version=version,
    description="Library for headless browser manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries"
    ],
    author="Allek Mott",
    author_email="allekmott@gmail.com",
    url="https://github.com/allekmott/aamras",
    packages=["aamras"],
    license="GPLv3",
    data_files=[("", ["LICENSE"])],
    python_requires=">=3.6",
    install_requires=["selenium"],
    extras_require={
        "dev": [
            "flake8",
            "mypy",
            "pytest",
            "pytest-cov",
            "pipenv-setup"
        ]
    }
)
