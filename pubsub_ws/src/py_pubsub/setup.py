from setuptools import find_packages, setup

package_name = 'py_pubsub'

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
            'talker_py = py_pubsub.pub_py:main',
            'listener_py = py_pubsub.sub_py:main',
            'talker_listener_py = py_pubsub.pubsub_py:main',
                'encoder_publisher = py_pubsub.encoder_publiser:main',
        ],
    },
)
