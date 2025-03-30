from setuptools import setup

setup(
    name='pyspeller',
    version='0.1',
    description='Библиотека для проверки орфографии с использованием API Яндекс Спеллер',
    url='https://github.com/ustinov/pyspeller',
    author='Алексей Устинов',
    author_email='lesin2798@mail.ru',
    license='MIT',
    packages=['pyspeller'],
    install_requires=[
        'requests',
        'typing'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
