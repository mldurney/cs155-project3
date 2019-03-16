import sys
import pickle
from utility import Utility

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python generate_sonnet.py <hmm_filename> <sonnet_filename> optional: <is_rhyming>')

    hmm_filename = sys.argv[1]
    if len(sys.argv) > 2:
        sonnet_filename = sys.argv[2]
    is_rhyming = False
    if len(sys.argv) > 3:
        is_rhyming = bool(sys.argv[3])

    with open(hmm_filename, "rb") as f:
        hmm = pickle.load(f)

    _, _, id_to_word, word_to_end_syllables, _, word_to_syllables, _ = \
        Utility.load_pkl()
    rhyme_id_to_word_ids, word_id_to_rhyme_id = Utility.load_rhymes_pkl()

    if is_rhyming:
        sonnet = Utility.generate_rhyming_poem(hmm, id_to_word, word_to_syllables,
            word_to_end_syllables, 10, 14, rhyme_id_to_word_ids, 
            word_id_to_rhyme_id, 'petrarchan')
        
    else:
        sonnet = Utility.generate_sonnet(
            hmm, id_to_word, word_to_syllables, word_to_end_syllables)

    if len(sys.argv) > 2:
        filepath = '../poems/' + sonnet_filename
        with open(filepath, 'w') as f:
            f.write('\n'.join(sonnet))

    print('')
    print('Petrarchan Sonnet:')
    print('#' * 70)
    print('')
    print(*sonnet, sep='\n')
    print('')
    print('#' * 70)
    print('')
