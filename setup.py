from os import path
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def readme():
    with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding="utf8") as f:
        return f.read()

setup(
    name='pinyin_markdown',
    version='0.8.2',
    description='Type Chinese pinyin with tone numbers in Markdown. Get accented pinyin.',
    long_description=readme(),
    url='https://github.com/bcaller/pinyin_markdown',
    py_modules=['pinyin_markdown'],
    packages=['pinyin_markdown'],
    license='AGPLv3',
    author='Ben Caller',
    author_email='bcallergmai@l.com',
    keywords='pinyin chinese markdown',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    install_requires=['markdown>=2.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: GNU Affero General Public License v3'
      ]
)
