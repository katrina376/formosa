from distutils.core import setup


setup(
    name='formosa',
    version='0.1.0',
    author='Hao-Yung Chan',
    author_email='katrina.hyc@gmail.com',
    packages=['formosa'],
    license='LICENSE',
    description='Coloring SVG Taiwan map.',
    long_description=open('README.md').read(),
    install_requires=[
        'svgwrite'
    ],
)
