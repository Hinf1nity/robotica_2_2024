from setuptools import find_packages, setup

package_name = 'ejercicios'

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
    maintainer_email='hinfinity@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'request_client = ejercicios.request_client:main',
            'request_service = ejercicios.request_service:main',
            'pub_ejer1 = ejercicios.pub_ejer1:main',
            'service_ejer2 = ejercicios.angulo_service:main',
            'client_ejer2 = ejercicios.angulo_client_py:main',
        ],
    },
)
