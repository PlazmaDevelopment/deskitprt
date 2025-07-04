from setuptools import setup, find_packages

setup(
    name="deskitprt",
    version="1.0.0",
    packages=find_packages(),
    install_requires=['cryptography>=3.4.7'],
    entry_points={'console_scripts': ['deskit=deskitprt.cli:main']},
    author="PlazmaDevelopment",
    author_email="plazmadevacc@gmail.com",
    description="File encryption/decryption tool",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/deskitprt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
