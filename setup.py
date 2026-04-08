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
    author='Essadeq',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/datagrep-cli',
    project_urls={
        'Bug Tracker': 'https://github.com/yourusername/datagrep-cli/issues',
        'Documentation': 'https://github.com/yourusername/datagrep-cli#readme',
        'Source Code': 'https://github.com/yourusername/datagrep-cli',
    },
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=[],
    extras_require={
        'color': ['colorama>=0.4.3,<1.0.0'],
        'progress': ['tqdm>=4.50.0,<5.0.0'],
        'excel': ['openpyxl>=3.0.0,<4.0.0'],
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.12.0',
            'black>=21.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
            'pylint>=2.8.0',
            'isort>=5.9.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'datagrep=datagrep:main',
        ],
    },
    include_package_data=True,
    package_data={'': ['py.typed']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    keywords='search filter csv json excel grep data-processing',
    zip_safe=False,
)
