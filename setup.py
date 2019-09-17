from setuptools import setup

setup(name='Tinder',
      version='0.1',
      description='Tinder API for Python',
      long_description=open('README.md').read().strip(),
      author='Brian Cefali',
      url='https://github.com/brocef/Tinder',
      py_modules=['src.tinder_api', 'src.fb_auth_token'],
      install_requires=['requests',
                        'robobrowser',
                        'lxml'],
      license='MIT License',
      zip_safe=False,
      keywords=['tinder-api', 'tinder', 'python-3', 'robobrowser'],
      #classifiers=[]
     )
