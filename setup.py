from setuptools import find_namespace_packages, setup


def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="genderak",
    version="0.1",
    install_requires=read_requirements("requirements.txt"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
)
