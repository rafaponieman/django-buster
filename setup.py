from setuptools import setup, find_packages

setup(
    name='django-buster',
    version = '0.0.1',
    description='A simple utility to use busters.json from gulp-buster with Django',
    author='Eric Bartels',
    author_email='ebartels@gmail.com',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data = True,
)
