from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Concept, Language
from pylexibank import progressbar

from collections import OrderedDict, defaultdict

from lingpy import *
import json
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

    def cmd_makecldf(self, args):

        wl = Wordlist(self.raw_dir.joinpath('words.tsv').as_posix())
        args.writer.add_sources()
        args.writer.add_languages() 
        concept_lookup = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split('-')[-1]+'_'+slug(concept.english)
            args.writer.add_concept(
                    ID=idx,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss = concept.attributes['chinese']
                    )
            concept_lookup[concept.english] = idx
        
        for idx in progressbar(wl, desc='cldfify', total=len(wl)):
             args.writer.add_form(
                Language_ID=wl[idx, 'doculect'],
                Parameter_ID=concept_lookup[wl[idx, 'concept']],
                Value=wl[idx, 'value'],
                Form= wl[idx, 'value'],
                Source=['Norman2003']
                )



