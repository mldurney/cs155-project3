################################################################################
# CS/CNS/EE 155 2019
# Miniproject 3, Section 4: Unsupervised Learning
#
# Author:           Team Labour of Moles
# Original author:  Andrew Kang
#
# Description:      Script to run hmm using unsupervised learning on the
#                   pickle file of preprocessed limerick data.
#                   Number of hidden states must be specified when started.
################################################################################


import sys
import pickle
from hmm import unsupervised_HMM
from utility import Utility

limerick_data_name = "../data/limerick_preprocessed_data.pkl"

def unsupervised_learning(n_states, n_iters, filename='', verbose=False):
    '''
    Trains an hmm using unsupervised learning on the collection of
    limericks and prints the results.

    Arguments:
        n_states:   Number of hidden states that the hmm should have.
        n_iters:    Number of iterations to run unsupervised learning.
        filename:   Output filename in ../models/ directory to save hmm.
        verbose:    Flag to print transition and observation matrices.
    '''

    if filename == '':
        filename = 'hmm_limerick_' + str(n_states) + 's_' + str(n_iters) + 'i.pkl'
    filepath = '../models/' + filename

    data = Utility.load_data(limerick_data_name)

    # Generate list of lines from all limericks.
    lines = [line for limerick in data for line in limerick]

    # Train the hmm.
    hmm = unsupervised_HMM(lines, n_states, n_iters)

    if verbose:
        print('Saving HMM into pickle at ' + filepath + '...')
        print('')

    # Save the hmm for later analysis.
    with open(filepath, 'wb') as f:
        pickle.dump(hmm, f)

    if verbose:
        # Print the transition matrix.
        print('Transition Matrix:')
        print('#' * 70)
        for i in range(len(hmm.A)):
            print(''.join('{:<12.3e}'.format(hmm.A[i][j])
                          for j in range(len(hmm.A[i]))))
        print('')

        # Print the observation matrix.
        print('Observation Matrix:  ')
        print('#' * 70)
        for i in range(len(hmm.O)):
            print(''.join('{:<12.3e}'.format(hmm.O[i][j])
                          for j in range(len(hmm.O[i]))))
        print('')

    return hmm


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print('usage: python run_unsupervised.py <n_states> <n_iters> ' +
              '<opt: filename> <opt: verbose (0/1)>')
        sys.exit(1)

    n_states = int(sys.argv[1])
    n_iters = int(sys.argv[2])
    filename = ''
    verbose = False

    if len(sys.argv) >= 4:
        filename = sys.argv[3]
    if len(sys.argv) == 5 and int(sys.argv[4]) == 1:
        verbose = True

    print('')
    print('#' * 70)
    print('Running unsupervised hmm on limericks with ')
    print('\t' + str(n_states) + '\thidden states')
    print('\t' + str(n_iters) + '\titerations')
    print('')

    hmm = unsupervised_learning(n_states, n_iters, filename, verbose)

    print('#' * 70)
    print('')
    print('')

    _, _, id_to_word, word_to_end_syllables, _, word_to_syllables, _ = \
        Utility.load_pkl(limerick_data_name)

    limerick = Utility.generate_poem(
        hmm, id_to_word, word_to_syllables, word_to_end_syllables)

    filename = 'hmm_limerick_' + str(n_states) + 's_' + str(n_iters) + 'i.txt'
    filepath = '../poems/' + filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(limerick))

    print('Resulting limerick:')
    print('#' * 70)
    print('')
    print(*limerick, sep='\n')
    print('')
    print('#' * 70)
    print('')
