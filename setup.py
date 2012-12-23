from setuptools import find_packages, setup


version = '0.1'
requires = (
    'Django==1.4.3',
)


setup(
    install_requires=requires,
    name='takestock',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version=version,
    zip_safe=False,
)
