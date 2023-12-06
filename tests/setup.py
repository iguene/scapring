from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['colorama', 'instabot'],

    'py2app': {
        'packages': ['colorama', 'instabot'],
        'includes': ['check_proxies', 'config', 'decoration', 'gsheet', ],  # Ajoute ici le nom du fichier utils.py sans l'extension '.py'
    },
    'include_package_data': True,
    'plist': {
        'CFBundleName': 'Simubot',
        # Ajoute d'autres clés plist si nécessaire
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)