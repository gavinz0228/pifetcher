import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pifetcher",
    version="0.0.2",
    author="Gavin Zhang",
    author_email="gavinz0228@gmail.com",
    description="A generic web scrapping library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gavinz0228/pifetcher",
    #packages=setuptools.find_packages("src"),
  
    packages=['pifetcher'],
    package_dir = {'pifetcher': 'src/pifetcher/'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ]
)