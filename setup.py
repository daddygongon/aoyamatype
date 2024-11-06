from setuptools import setup, find_packages

setup(
    name='aoyamatype',
    version='1.1.0',  # バージョンアップで管理しやすくなります
    packages=find_packages(),
    install_requires=[
        'matplotlib',  # グラフ描画のために必要なライブラリ
    ],
    entry_points={
        'console_scripts': [
            'aoyamatype=aoyamatype:main',  # メイン実行ファイルと関数名を指定
        ],
    },
    package_data={
        '': ['*.txt', '*.list'],  # 例: 必要なファイルのパターンを指定
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
