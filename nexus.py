from csvw.metadata import TableGroup
from lingpy import util, LexStat
from lingpy.convert.html import template_path
from lingpy.convert.strings import write_nexus
from pathlib import Path

# receive the template path from lingpy for splitstree
tpath = util.Path(template_path('splitstree.nex'))
if tpath.exists:
    _template = util.read_text_file(tpath.as_posix())
else:  # pragma: no cover
    raise IOError("Unknown template %s" % template)

tbg = TableGroup.from_file(Path('cldf',
    'StructureDataset-metadata.json').as_posix())
existing_taxa = set([row['Language_ID'] for row in
    tbg.tabledict['values.csv']])
idx = 0
taxa = {}
for t in tbg.tabledict['languages.csv']:
    if t['ID'] in existing_taxa:
        taxa[t['ID']] = (idx, t['Name'])
        idx += 1
params = {t['ID']: (i, t['Name']) for i, t in
        enumerate(tbg.tabledict['features.csv'])}
matrix = [[0 for p in params] for t in taxa]
for row in tbg.tabledict['values.csv']:
    tidx, tname = taxa[row['Language_ID']]
    pidx, pname = params[row['Parameter_ID']]
    if row['Value'] == '+':
        matrix[tidx][pidx] = 1
        
alpha = 'abcdefghijklmnopqrstuvwxyz'
alpha += alpha.upper()
alpha += '0123456789'

matrix_string = ''
tax_list = sorted([t[1] for t in taxa.items()], key=lambda x: x[0])
for i, line in enumerate(matrix):
    matrix_string += '{0:12}'.format(''.join([x for x in tax_list[i][1] if 
        x in alpha])[:11])
    matrix_string += ''.join([str(x) for x in line])+'\n'

with open('chinese-structure.nex', 'w') as f:
    f.write(_template.format(
        matrix=matrix_string, 
        ntax=len(tax_list),
        dtype='STANDARD',
        nchar=len(params),
        gap='-',
        missing='?'
        ))

lex = LexStat.from_cldf(Path('cldf', 'cldf-metadata.json').as_posix())
lex.cluster(method='sca', threshold=0.45, ref='cogid')
write_nexus(lex, mode='splitstree', filename='chinese-lexemes.nex')

