import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pifetcher",
    version="0.0.2.5",
    author="Gavin Zhang",
    author_email="gavinz0228@gmail.com",
    description="A scalable headless data fetching library written with python and message queue service to enable quickly and easily prasing web data in a distributive way.",
    long_description=long_description,
    long_description_content_type ="text/markdown",
    url="https://github.com/gavinz0228/pifetcher",
    #packages=setuptools.find_packages("src"),
  
    packages=['pifetcher', 'pifetcher.core', 'pifetcher.data_fetchers', 'pifetcher.utilities', 'pifetcher.work_queue'],
    package_dir = {
        'pifetcher': 'src/pifetcher',
        'pifetcher.core': 'src/pifetcher/core', 
        'pifetcher.data_fetchers': 'src/pifetcher/data_fetchers',
        'pifetcher.utilities': 'src/pifetcher/utilities',
        'pifetcher.work_queue':'src/pifetcher/work_queue'
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX'
    ],
    include_package_data=True,
    install_requires=[
          'bs4',
          'selenium',
      ]

)