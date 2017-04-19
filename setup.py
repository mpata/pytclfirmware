from setuptools import setup

setup(
    name='pytclfirmware',
    version='1.0.1',
    description='Scan and extract TCL SmartTV Televisions firmware',
    author='Manuel Pata',
    author_email='pata@alface.de',
    license='BSD',
    keywords='tcl android smarttv television',
    packages=['pytclfirmware'],
    entry_points={
        'console_scripts': [
            'tclfirmware=pytclfirmware:main']}
)
