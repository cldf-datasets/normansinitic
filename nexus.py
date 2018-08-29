from csvw.metadata import TableGroup
from lingpy import util
from lingpy.convert.html import template_path

# receive the template path from lingpy for splitstree
tpath = util.Path(template_path('splitstree.nex'))
if tpath.exists:
    _template = util.read_text_file(tpath.as_posix())
else:  # pragma: no cover
    raise IOError("Unknown template %s" % template)

tbg = TableGroup.from_file('cldf/StructureDataset-metadata.json')
taxa = {t['ID']: (i, t['Name']) for i, t in
        enumerate(tbg.tabledict['languages.csv'])}
params = {t['ID']: (i, t['Name']) for i, t in
        enumerate(tbg.tabledict['parameters.csv'])}
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

with open('chinese.nex', 'w') as f:
    f.write(_template.format(
        matrix=matrix_string, 
        ntax=len(tax_list),
        dtype='STANDARD',
        nchar=len(params),
        gap='-',
        missing='?'
        ))
    
