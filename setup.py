import setuptools

# Modify src if the source directory name changes
import src as module

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    # Project Details
    #   Configure in <module>/__init__.py
    name=module.APP_NAME,
    version=module.APP_VERSION,
    author=module.APP_AUTHOR_NAME,
    author_email=module.APP_AUTHOR_EMAIL,
    license=module.APP_LICENSE,
    description=module.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=module.APP_URL,
    project_urls={
        'Documentation': module.APP_URLS['bug-tracking'],
        'Bug Tracking': module.APP_URLS['documentation']
    },
    maintainer=module.MAINTAINER_NAME,
    maintainer_email=module.MAINTAINER_EMAIL,
    packages=setuptools.find_packages(),
    include_package_data=True,
    
    # Project Classifiers
    #   Useful if publishing to PyPi
    #   Valid Classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    ],
    
    # Project building requirements
    setup_requires=[
        "setuptools>=66.1.1",
        "wheel>=0.38.4",
        "pip>=22.3.1",
    ],
    
    # Project runtime requirements
    install_requires=[],
    
    # Project development/maintenance requirements
    extras_require={
        "dev": [
            "setuptools>=66.1.1",
            "wheel>=0.38.4",
            "flake9>=3.8.3.post2 ",
            "black>=22.12.0",
            "twine>=4.0.2",
            "sphinx>=6.1.3",
        ]
    },
    python_requires='>=3.10',

    # Project script entry point
    entry_points={
        "console_scripts": [
            f'{module.APP_NAME} = src.__main__:main'
        ]
    }
)
