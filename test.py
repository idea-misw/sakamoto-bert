import os

import mojimoji
from pyknp import Juman

jumanpp = Juman()

sentences = []
with open('calendar.txt') as f:
    for line in f:
        result = jumanpp.analysis(mojimoji.han_to_zen(line.rstrip()))
        sentence = ' '.join(mrph.midasi for mrph in result.mrph_list())
        sentences.append(sentence)

with open(os.path.join('SST-2', 'test.tsv'), 'w') as f:
    f.write('index\tsentence\n')
    for index, sentence in enumerate(sentences):
        f.write(str(index) + '\t' + sentence + '\n')
