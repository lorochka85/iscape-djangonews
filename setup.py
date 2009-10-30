from setuptools import setup, find_packages


setup(
    name='djangonews',
    version='0.1.2',
    description='A News Release Application for Django',

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',

    install_requires=(
        'django-staticmedia',
        'feedparser',
    ),

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=('ez_setup', 'examples', 'tests')),
)
