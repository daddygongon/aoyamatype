from setuptools import setup, find_packages

setup(
    name="aoyamatype",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'aoyamatype = aoyamatype.typing_game:main',
        ],
    },
    package_data={
        '': ['data/*.txt'],
    },
    install_requires=[
        # 必要な依存関係があればここに記述
        "matplotlib"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)