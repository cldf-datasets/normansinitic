from pycldf import StructureDataset, Source
from csvw.metadata import TableGroup
import json
from lingpy import *
from lingpy.strings import write_nexus

# load languages
with open('raw/languages.json') as f:
    langs = json.load(f)

formtable, languagetable, parametertable = [], [], []

with open('raw/structures.tsv') as f:
    tmp = f.readlines()
    data = [t.strip('\n').split('\t') for t in tmp]

visited = []
for line in data[1:]:
    vals = dict(zip(data[0], line))
    vidx, lidx, pidx = vals['ID'], vals['DOCULECT_IN_SOURCE'], vals['STRUCTURE_ID']
    idx = '{0}-{1}-{2}'.format(lidx, pidx, vidx)
    if not pidx in visited:
        parametertable += [{
            'ID': pidx,
            'Name': vals['NAME'],
            'Description': vals['STRUCTURE']}]
        visited += [pidx]
    if not lidx in visited:
        languagetable += [{
            'ID': lidx,
            'Name': vals['DOCULECT'],
            'Glottocode': langs.get(vals['DOCULECT'], {'glottolog': ''})['glottolog']
            }]
        visited += [lidx]
    formtable += [{
        'ID': idx,
        'Language_ID': lidx,
        'Parameter_ID': pidx,
        'Value': vals['VALUE'],
        'Source': ['Norman2003'],
        }]

ds = StructureDataset.in_dir('cldf')
ds.add_sources(
        Source('article', 'Norman2003', 
            author='Jerry Norman',
            booktitle='The Sino-Tibetan languages',
            editor = "Thurgood, Graham and LaPolla, Randy J.",
            publisher="Routledge",
            address="London and New York",
            pages='72-83',
            year="2003",
            title='The Chinese dialects. Phonology',
        ))

ds.add_component('ParameterTable')
ds.add_component('LanguageTable')
ds.write(ValueTable=formtable, ParameterTable=parametertable,
        LanguageTable=languagetable)

ds.write_metadata()
ds.write_sources()



