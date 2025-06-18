from setuptools import setup

setup(
    name='RdpGui',
    version='1.0',
    packages=[
        "rdpgui", 
        "rdpgui.widgets"
    ],
    package_data={
        'rdpgui': [
            'fonts/*.ttf',
            'style/*.scss'
        ],
    },
    include_package_data=True,
    install_requires=[
        'pyside6>=6.8.0.2',
        'pysqlcipher3>=1.2.0',
        'pillow>=11.0.0'
    ],
    entry_points={
        'gui_scripts': [
            'rdpgui = rdpgui.app:main',
        ],
    },
)
