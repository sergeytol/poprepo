from setuptools import find_packages, setup


def get_version() -> str:
    with open("src/poprepo/version.py", "r") as version_file:
        return version_file.readline().split("VERSION = ")[1].strip()[1:-1]


setup(
    name="poprepo",
    version=get_version(),
    url="https://github.com/sergeytol/poprepo",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "pydantic>=1.8.0,<2.0.0",
        "uvicorn>=0.15.0,<0.16.0",
        "python-dotenv>=0.20.0,<0.21.0",
        "PyGithub==1.55",
        "django-environ>=0.8.1,<0.9",
        "redis==4.2.2",
        "pytest==7.1.1",
    ],
)
