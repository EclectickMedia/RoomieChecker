from setuptools import setup, find_packages
from UserChecker import __version__

with open("Readme.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as f:
#     required = f.read().splitlines()

setup(
    name='UserChecker',
    version=__version__,
    description='Executes callback upon user connection to network',
    long_description=long_description,
    author='Ariana Giroux',
    author_email='ariana.giroux@gmail.com',
    license='MIT',
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    zip_safe=True,
    entry_points={
        'console_scripts': ['UserChecker=UserChecker.main:run']
    },
    classifiers=(
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Development Status :: 4 - Beta",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "Intended Audience :: End Users/Desktop",
                "Intended Audience :: Information Technology",
                "License :: OSI Approved :: MIT License",
                "Operating System :: Unix",
                "Topic :: System :: Networking :: Monitoring",
                "Topic :: Utilities",
    ),
)
