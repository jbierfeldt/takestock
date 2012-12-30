from setuptools import find_packages, setup


version = '0.1'
requires = (
    'django==1.4.3',
    'django-extensions==1.0.2',
)


setup(
    install_requires=requires,
    name='takestock',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version=version,
    zip_safe=False,
)
