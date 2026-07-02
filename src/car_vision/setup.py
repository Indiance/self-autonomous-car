from setuptools import find_packages, setup

package_name = 'car_vision'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/camera.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='tharun.tvishy@gmail.com',
    description='CSI camera capture and viewing for the autonomous RC car',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'csi_camera_publisher = car_vision.csi_camera_publisher:main',
            'image_viewer = car_vision.image_viewer:main',
        ],
    },
)
