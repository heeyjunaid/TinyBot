from setuptools import setup, find_packages


setup(name='tinybot',
      version='0.0.1',
      description='Minimal virtual agent creation library',
      author='Junaid Shaikh',
      author_email='junaidlatur@gmail.com',
      url='https://github.com/heeyjunaid/TinyBot',
      packages=find_packages(),
      # package_dir={"tinybot":"tinybot"},
      install_requires=[
            "PyYAML",
            "scikit-learn>=1.0.0",
            "torch>=1.12.0",
            "transformers>=4.20.1",
            "numpy>1.20.0"
      ]
     )