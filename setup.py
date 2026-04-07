"""Setup configuration for datagrep-cli."""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='datagrep-cli',
    version='1.0.0',
    description='Search and filter CSV, JSON, and Excel records with flexible matching modes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/datagrep-cli',
    license='MIT',
    py_modules=['datagrep'],
    python_requires='>=3.7',
    install_requires=[],
    extras_require={
        'color': ['colorama>=0.4.3'],
        'progress': ['tqdm>=4.50.0'],
        'excel': ['openpyxl>=3.0.0'],
        'dev': ['pytest>=6.0', 'black', 'flake8'],
    },
    entry_points={
        'console_scripts': [
            'datagrep=datagrep:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
    ],
    keywords='search filter csv json excel grep',
)
