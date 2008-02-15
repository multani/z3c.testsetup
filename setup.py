from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n\n'
    + 'Detailed Documentation\n'
    + '----------------------\n'
    + read('src', 'z3c', 'testsetup', 'README.txt')
    + '\n\n'
    + read('CHANGES.txt')
    + '\n\n'
    )

setup(
    name='z3c.testsetup',
    version='0.1.0',
    author='Uli Fouquet and the Zope Community',
    author_email='uli@gnufix.de',
    url = 'http://pypi.python.org/pypi/z3c.testsetup',
    description='Easier test setup for Zope 3 projects and '
                'other Python packages.',
    long_description=long_description,
    license='ZPL 2.1',
    keywords="zope3 zope tests unittest doctest testsetup",
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Operating System :: OS Independent',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['z3c'],
    include_package_data = True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zope.component',
                      'zope.testing',
                      'zope.app.testing',
                      'martian',
                      ],
)
