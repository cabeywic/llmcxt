from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='llmcxt',
    version='0.1.2',
    author='Charaka Abeywickrama',
    author_email='charaka.abeywickrama@gmail.com',
    description='A tool to manage and generate context for Large Language Models from project files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cabeywic/llmcxt.git',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'llmcxt=llmcxt.cli:cli',
        ],
    },
)