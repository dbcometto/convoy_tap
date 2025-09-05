from setuptools import find_packages, setup

package_name = 'ts_convoy_comm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    extras_require={
        'test': ['pytest', 'mock']  # Testing dependencies
    },
    zip_safe=True,
    maintainer='dma',
    maintainer_email='dma@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'ts_pub = ts_convoy_comm.ts_pub:main',
            'ts_sub = ts_convoy_comm.ts_sub:main'
        ],
    },
)

