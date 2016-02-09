from setuptools import setup

setup(
    name = 'Lukas Heinrich',
    version = '0.0.1',
    install_requires = [
        'Flask',
        'click',
        'zmq',
        'pyyaml',
        'requests'
    ],
  entry_points = {
      'console_scripts': [
          'mprtect_server=mprtect.event_server:eventserver',
          'mprtect_collector=mprtect.event_collector:eventcollector',
          'mprtect_sherpa=mprtect.steersherpa:steersherpa'
      ],
  },)