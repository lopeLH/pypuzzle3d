import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("pip_requirements.txt", "r") as fh:
    pip_requirements = fh.read()

setuptools.setup(
    name="pypuzzle3d",  # Replace with your own username
    version="0.0.1",
    author="Daniel López Sánchez",
    author_email="lope@usal.es",
    description="A small example package to solve 3D puzzles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lopeLH/3x3x3-Cube-Puzzle-Solver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=pip_requirements
)