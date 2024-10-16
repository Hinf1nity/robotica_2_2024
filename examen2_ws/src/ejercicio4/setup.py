from setuptools import find_packages, setup

package_name = 'ejercicio4'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hinfinity',
    maintainer_email='dacalvimontes@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'explorador = ejercicio4.explorador:main',
            'nodo_odom = ejercicio4.nodo_odom:main',
            'nodo_map = ejercicio4.nodo_map:main',
            'giro_90 = ejercicio4.giro_90:main',
        ],
    },
)
