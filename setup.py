import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PandasBasketball",
    version="0.0.1",
    author="Alfredo Medina",
    author_email="alfremedpal@gmail.com",
    description="A Python module to scrape data from basketbal-reference.com and convert it to pandas data structures for analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alfremedpal/PandasBasketball",
    packages=setuptools.find_packages(),
    install_requires=[            
          "requests",
          "beautifulsoup4",
          "pandas"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)