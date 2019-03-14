import sys
import pickle
from utility import Utility

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python generate_sonnet.py <hmm_filename> <sonnet_filename>')

    hmm_filename = sys.argv[1]
    if len(sys.argv) > 2:
        sonnet_filename = sys.argv[2]

    with open(hmm_filename, "rb") as f:
        hmm = pickle.load(f)

    _, _, id_to_word, word_to_end_syllables, _, word_to_syllables, _ = \
        Utility.load_pkl()

    sonnet = Utility.generate_sonnet(
        hmm, id_to_word, word_to_syllables, word_to_end_syllables)

    if len(sys.argv) > 2:
        filepath = '../poems/' + sonnet_filename
        with open(filepath, 'w') as f:
            f.write('\n'.join(sonnet))

    print('')
    print('Sonnet:')
    print('#' * 70)
    print('')
    print(*sonnet, sep='\n')
    print('')
    print('#' * 70)
    print('')
