from setuptools import setup, find_packages

setup(
    name='kyberswap_py_sdk',
    version='0.2.8',  # Update version as needed
    author='Harsh',
    author_email='hssingh@connect.ust.hk',
    description='A Python SDK for the KyberSwap Aggregator API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Harsh-Gill/kyberswap_py_sdk',  # Update with your repository URL
    packages=find_packages(),
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    package_data={
        "kyberswap_py_sdk": ["abis/*.json"],  # Include JSON files inside the abi folder
    },
    install_requires=[
        'web3==6.20.1',
        'eth-account',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)