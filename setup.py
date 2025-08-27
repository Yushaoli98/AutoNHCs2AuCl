from setuptools import setup, find_packages

setup(
    name="nhc_aucl_generate",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "rdkit-pypi",
        "pandas",
        "numpy",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "nhc-aucl=scripts.run_pipeline:main",
        ],
    },
)
