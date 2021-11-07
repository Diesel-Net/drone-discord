from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    README = fh.read()

setup(
    name='api',
    version='1.0.0a0',
    description='Drone-Discord Build logger',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==1.1.2',
        'connexion==2.7.0',
        'flask-cors==3.0.8', 
        'pymongo==3.11.0', 
        'ruamel.yaml==0.16.10',
        'cryptography==3.2.1',
        'PyJWT==1.7.1',
        'flask-limiter',
        'pendulum==2.1.2',
    ],
)
