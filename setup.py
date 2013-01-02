from setuptools import find_packages, setup


version = '0.1'
requires = (
    'django==1.4.3',
    'django-extensions==1.0.2',
    'html5lib==0.95',
    'pil==1.1.7',
    'pisa==3.0.33',
    'reportlab==2.6',
)


setup(
    install_requires=requires,
    name='takestock',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version=version,
    zip_safe=False,
)
