from setuptools import setup

setup(
    name='pyspeller',
    version='1.0.0',
    author='Алексей Устинов',
    author_email='lesin2798@mail.ru',
    description='Библиотека для проверки орфографии с использованием API Яндекс Спеллер. Обертка Python для Яндекс.Спеллер.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    license_files=['LICENSE'],
    keywords=['speller', 'yandex', 'api'],
    python_requires='>=3.12',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/austnv/pyspeller/',
    project_urls={
        'Repository': 'https://github.com/austnv/pyspeller/',
        'Issues': 'https://github.com/austnv/pyspeller/issues',
    },
)
