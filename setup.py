import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="pycasinosim",
    version="0.0.1",
    author="Christopher McCarthy",
    author_email="chris.mccarthy20@protonmail.com",
    description="A Python package to simulate and analyse casino game play.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pycasinosim"],
    package_dir={"pycasinosim": "pycasinosim"},
    python_requires=">=3.6",
)
