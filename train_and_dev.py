import glob
import os

import mojimoji
from pyknp import Juman

jumanpp = Juman()

id2text = {}
pos_ids = []

for tsv_path in glob.glob('tsv/*'):
    with open(tsv_path) as f:
        for line in f:
            id_str, text = line.rstrip().split('\t', maxsplit=1)
            id_ = int(id_str)
            id2text[id_] = text

            screen_name = os.path.splitext(os.path.basename(tsv_path))[0]
            if screen_name == 'sksk_sskn':
                pos_ids.append(id_)

split2pairs = {}

for id_ in sorted(id2text):
    result = jumanpp.analysis(mojimoji.han_to_zen(id2text[id_]))
    sentence = ' '.join(mrph.midasi for mrph in result.mrph_list())
    label = int(id_ in pos_ids)

    split = 'train' if id_ % 50 else 'dev'
    if split not in split2pairs:
        split2pairs[split] = []
    split2pairs[split].append((sentence, label))

for split, pairs in split2pairs.items():
    with open(os.path.join('SST-2', split + '.tsv'), 'w') as f:
        f.write('sentence\tlabel\n')
        for sentence, label in pairs:
            f.write(sentence + '\t' + str(label) + '\n')
