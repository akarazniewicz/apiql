import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='apiql',
    version='0.12.3',
    test_suite='tests',
    author="Artur Karazniewicz",
    author_email="karaznie+pip@protonmail.com",
    description="A simple API Query Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karaznie/apiql",
    packages=setuptools.find_packages(),
    install_requires=[
        'funcy',
        'whatever',
        'antlr4-python3-runtime'
    ],
    test_require=[
      'SQLAlchemy'
    ],
    python_requires='>=3.6'
    ,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",

    ],
)
