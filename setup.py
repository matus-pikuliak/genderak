from setuptools import find_packages, setup


def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="genderak",
    version="0.1",
    # package_dir={"": "."},
    install_requires=read_requirements("requirements.txt"),
    packages=find_packages(
        exclude=["runs"],  # empty by default
    ),
)