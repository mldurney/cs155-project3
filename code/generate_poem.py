import sys
import pickle
from utility import Utility

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('usage: python generate_poem.py <hmm_filename> <opt: poem_filename>')
        sys.exit(1)

    hmm_filename = sys.argv[1]
    if len(sys.argv) > 2:
        poem_filename = sys.argv[2]

    print('Number of syllables per line: ')
    n_syllables = [int(x) for x in input().split()]

    if len(n_syllables) == 1:
        n_syllables = n_syllables[0]
        print('Number of lines: ')
        n_lines = int(input())
    else:
        n_lines = 0

    with open(hmm_filename, "rb") as f:
        hmm = pickle.load(f)

    _, _, id_to_word, word_to_end_syllables, _, word_to_syllables, _ = \
        Utility.load_pkl()

    poem = Utility.generate_poem(
        hmm, id_to_word, word_to_syllables, word_to_end_syllables,
        n_syllables, n_lines)

    if len(sys.argv) > 2:
        filepath = '../poems/' + poem_filename
        with open(filepath, 'w') as f:
            f.write('\n'.join(poem))

    print('')
    print('Poem:')
    print('#' * 70)
    print('')
    print(*poem, sep='\n')
    print('')
    print('#' * 70)
    print('')
