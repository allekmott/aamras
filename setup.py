import os.path
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

path_readme = os.path.join(here, "README.rst")
path_version = os.path.join(here, "aamras", "__version__.py")

with open(path_readme) as file_:
    long_description = file_.read()

about = {}
with open(path_version) as file_:
    exec(file_.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    license=about["__license__"],
    data_files=[("", ["LICENSE"])],
    python_requires=">=3.6",
    install_requires=["selenium"],
    extras_require={
        "dev": ["flake8", "mypy", "pytest", "pytest-cov", "pipenv-setup", "sphinx",]
    },
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
        "Topic :: Software Development :: Libraries",
    ],
)
