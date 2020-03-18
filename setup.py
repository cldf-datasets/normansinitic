from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_normansinitic',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_normansinitic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'normansinitic=lexibank_normansinitic:Dataset',
        ],
        'cldfbench.commands': [
            'normansinitic=normansiniticcommands',
        ],
    },
    install_requires=[
        'pylexibank>=2.0',
    ]
)
