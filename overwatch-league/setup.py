import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="overwatch-league-skill",
    version="0.0.1",
    author="Joel Heenan",
    author_email="joelh@planetjoel.com",
    description="Alexa Skill to ask questions of the Overwatch League API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mechcow/overwatch-league-skill",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)