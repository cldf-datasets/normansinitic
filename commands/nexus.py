"""
Write NEXUS files suitable as input for SplitsTree for the structural and the lexical data.
"""
import string
import pathlib

from lingpy import LexStat
from lingpy.convert.html import template_path
from lingpy.convert.strings import write_nexus

from lexibank_normansinitic import Dataset


def run(args):
    # use lingpy's nexus template for splitstree:
    _template = pathlib.Path(template_path('splitstree.nex')).read_text(encoding='utf-8')

    ds = Dataset(args)
    structure_dataset = ds.cldf_reader('structure')
    existing_taxa = set(row['Language_ID'] for row in structure_dataset['ValueTable'])
    idx = 0
    taxa = {}
    for t in structure_dataset['LanguageTable']:
        if t['ID'] in existing_taxa:
            taxa[t['ID']] = (idx, t['Name'])
            idx += 1
    params = {t['ID']: (i, t['Name']) for i, t in enumerate(structure_dataset['ParameterTable'])}

    matrix = [[0 for p in params] for t in taxa]
    for row in structure_dataset['ValueTable']:
        tidx, tname = taxa[row['Language_ID']]
        pidx, pname = params[row['Parameter_ID']]
        if row['Value'] == '+':
            matrix[tidx][pidx] = 1

    alpha = string.ascii_letters + string.digits
    matrix_string = ''
    tax_list = sorted([t[1] for t in taxa.items()], key=lambda x: x[0])
    for i, line in enumerate(matrix):
        matrix_string += '{0:12}'.format(''.join([x for x in tax_list[i][1] if x in alpha])[:11])
        matrix_string += ''.join([str(x) for x in line]) + '\n'

    pathlib.Path('chinese-structure.nex').write_text(
        _template.format(
            matrix=matrix_string,
            ntax=len(tax_list),
            dtype='STANDARD',
            nchar=len(params),
            gap='-',
            missing='?'
        ),
        encoding='utf8')

    lex = LexStat.from_cldf(str(ds.cldf_specs()[None].metadata_path))
    lex.cluster(method='sca', threshold=0.45, ref='cogid')
    write_nexus(lex, mode='splitstree', filename='chinese-lexemes.nex')
