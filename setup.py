from setuptools import setup

setup(
    name='dominoes',
    version='6.1.1',
    description='A Python library for the game of dominoes, with an accompanying CLI and AI players.',
    url='https://github.com/Brunozml/dominoes-rl',
    author='Bruno Zorrilla',
    author_email='bzorrilla02@gmail.com',
    license='MIT',
    packages=['dominoes'],
    scripts=['scripts/dominoes'],
    test_suite='tests'
)
