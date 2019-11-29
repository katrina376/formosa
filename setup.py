from distutils.core import setup


setup(
    name='formosa',
    version='0.2.0',
    author='Hao-Yung Chan',
    author_email='katrina.hyc@gmail.com',
    packages=['formosa'],
    license='LICENSE',
    description='Generate and color SVG Taiwan maps.',
    long_description=open('README.md').read(),
    install_requires=[
        'svgwrite',
        'pyshp',
    ],
)
