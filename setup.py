import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='apiql',
    version='0.12.4',
    test_suite='tests',
    author="Artur Karazniewicz",
    author_email="karaznie+pip@protonmail.com",
    description="A simple API Query Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karaznie/apiql",
    packages=setuptools.find_packages(),
    package_data={'': ['*.txt', '*.md', '*.tokens', '*.interp']},
    install_requires=[
        'funcy',
        'whatever',
        'antlr4-python3-runtime',
        'python-dateutil'
    ],
    python_requires='>=3.5',
    keywords='api dynamic query flask bottle django sqlalchemy',
    project_urls={
        "Homepage": "https://github.com/akarazniewicz/apiql/issues",
        "Bug Tracker": "https://github.com/akarazniewicz/apiql/issues",
        "Documentation": "https://github.com/akarazniewicz/apiql",
        "Source Code": "https://github.com/akarazniewicz/apiql",
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Environment :: Web Environment"
    ],
)
