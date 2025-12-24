from setuptools import setup

package_name = 'turtlebot4_backend'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sasr01-kit',
    maintainer_email='uswup@student.kit.edu',
    description='Backend package for TurtleBot4',
    license='MIT',
    entry_points={
        'console_scripts': [
            # Example: 'node = turtlebot4_backend.turtlebot4_controller:main'
        ],
    },
)
