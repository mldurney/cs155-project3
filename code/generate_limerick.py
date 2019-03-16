import sys
import pickle
from utility import Utility

limerick_data_name = "../data/limerick_preprocessed_data.pkl"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python generate_limerick.py <hmm_filename> <sonnet_filename> optional: <is_rhyming>')

    hmm_filename = sys.argv[1]
    if len(sys.argv) > 2:
        limerick_filename = sys.argv[2]
    is_rhyming = False
    if len(sys.argv) > 3:
        is_rhyming = bool(sys.argv[3])

    with open(hmm_filename, "rb") as f:
        hmm = pickle.load(f)

    _, _, id_to_word, word_to_end_syllables, _, word_to_syllables, _ = \
        Utility.load_pkl(limerick_data_name)
    rhyme_id_to_word_ids, word_id_to_rhyme_id = Utility.load_rhymes_pkl(
        limerick_data_name)

    if is_rhyming:
        limerick = Utility.generate_rhyming_poem(hmm, id_to_word, word_to_syllables,
            word_to_end_syllables, [9, 9, 6, 6, 9], 0, rhyme_id_to_word_ids, 
            word_id_to_rhyme_id, 'limerick')
        
    else:
        limerick = Utility.generate_poem(hmm, id_to_word, word_to_syllables,
            word_to_end_syllables, [9, 9, 6, 6, 9], 0)

    if len(sys.argv) > 2:
        filepath = '../poems/' + limerick_filename
        with open(filepath, 'w') as f:
            f.write('\n'.join(limerick))

    print('')
    print('Limerick:')
    print('#' * 70)
    print('')
    print(*limerick, sep='\n')
    print('')
    print('#' * 70)
    print('')
