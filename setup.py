from setuptools import setup, find_packages


def _requirements(fname: str):
    with open(fname, 'r') as f:
        list(f)


setup(
    name='sqlbtye',
    version='0.0.1dev',
    packages=find_packages('src'),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=_requirements('./requirements.txt'),
)