# _*_ coding: UTF-8 _*_

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='hunor',
    description='The son of Nimrod',
    long_description=readme(),
    keywords='test mutant analysis',
    version='0.0.0',
    url='https://github.com/marcioaug/hunor',
    author='Marcio Augusto Guimarães',
    author_email='masg@ic.ufal.br',
    license='MIT',
    packages=['hunor'],
    install_requires=[
        'argparse==1.4.0'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['hunor=hunor.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Test :: Mutation'
    ]
)