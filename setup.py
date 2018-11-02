from setuptools import setup

setup(
    name='midiband',
    version='0.0.1',
    packages=['midiband'],
    url='https://github.com/droberin/midiband',
    license='GPL v3.0',
    author='DRoBeR',
    author_email='drober@gmail.com',
    description='MIDIBand - Music hub over the net',
    requires='zeroconf, netifaces, mido'
)
