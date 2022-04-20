from setuptools import setup
 
setup(
    name='gripperEnv',
    version = '0.0.1',
    install_requires=[
        'stable-baselines',
        'tensorflow<1.15.0'
        'autopep8',
        'gym==0.15.7',
        'keras==2.2.4',
        'matplotlib',
        'numpy==1.18',
        'opencv-contrib-python',
        'pandas',
        'pytest',
        'pydot',
        'PyYAML==5.4.1',
        'seaborn',
        'scikit-learn',
        'tqdm',
        'paramiko',
        'pybullet',
        'numba'
    ],
)