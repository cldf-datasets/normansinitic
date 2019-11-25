from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Concept, Language
from pylexibank import progressbar
from cldfbench import CLDFSpec

from lingpy import *
from clldutils.misc import slug
import attr


@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    SubGroup = attr.ib(default="Sinitic")
    DialectGroup = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")
    ChineseName = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'normansinitic'
    dir = Path(__file__).parent
    concept_class = CustomConcept
    language_class = CustomLanguage

    def cldf_specs(self):
        return {
            None: BaseDataset.cldf_specs(self),
            'structure': CLDFSpec(
                module='StructureDataset',
                dir=self.cldf_dir,
                data_fnames={'ParameterTable': 'features.csv'}
            )
        }

    def cmd_makecldf(self, args):
        with self.cldf_writer(args) as writer:
            wl = Wordlist(self.raw_dir.joinpath('words.tsv').as_posix())
            writer.add_sources()
            writer.add_languages()
            concept_lookup = {}
            for concept in self.conceptlists[0].concepts.values():
                idx = concept.id.split('-')[-1]+'_'+slug(concept.english)
                writer.add_concept(
                    ID=idx,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss = concept.attributes['chinese']
                )
                concept_lookup[concept.english] = idx

            for idx in progressbar(wl, desc='cldfify', total=len(wl)):
                writer.add_form(
                    Language_ID=wl[idx, 'doculect'],
                    Parameter_ID=concept_lookup[wl[idx, 'concept']],
                    Value=wl[idx, 'value'],
                    Form= wl[idx, 'value'],
                    Source=[wl[idx, 'source']]
                )
            language_table = writer.cldf['LanguageTable']

        with self.cldf_writer(args, cldf_spec='structure', clean=False) as writer:
            writer.cldf.add_component(language_table)
            writer.objects['LanguageTable'] = self.languages

            pids = set()
            for vals in self.raw_dir.read_csv('structures.tsv', delimiter='\t', dicts=True):
                vidx, lidx, pidx = vals['ID'], vals['DOCULECT'], vals['STRUCTURE_ID']
                idx = '{0}-{1}-{2}'.format(lidx, pidx, vidx)
                if not pidx in pids:
                    writer.objects['ParameterTable'].append({
                        'ID': pidx,
                        'Name': vals['NAME'],
                        'Description': vals['STRUCTURE']
                    })
                    pids.add(pidx)
                writer.objects['ValueTable'].append({
                    'ID': idx,
                    'Language_ID': lidx,
                    'Parameter_ID': pidx,
                    'Value': vals['VALUE'],
                    'Source': [vals['SOURCE']],
                })
