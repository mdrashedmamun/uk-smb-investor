from setuptools import setup, find_packages

setup(
    name="uk_smb_investor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit>=1.28.0",
        "pydantic>=2.5.0",
    ],
)
