################################################################################
# CS/CNS/EE 155 2019
# Miniproject 3, Section 4: Unsupervised Learning
#
# Author:           Team Labour of Moles
# Original author:  Ashivek Dutta
#
# Description:      Utility functions for HMM implementation for Shakespearean
#                   poem generation for section 4 of CS 155 Miniproject 3.
#                   Based upon CS 155 Set 6 solutions.
################################################################################

import pickle


class Utility:
    '''
    Utility for the HMM files.
    '''

    def __init__(self):
        pass

    @staticmethod
    def load_pkl():
        '''
        Loads all data pickled into 'preprocessed_data.pkl'.

        Returns:
            data:       Matrix of sonnets with the following hierarchy:
                            1st dimension: Sonnets
                            2nd dimension: Lines in sonnet
                            3rd dimensoin: Word ids in line
            word_to_id: Dictionary from word to its word id
            id_to_word: Dictionary from word id to the corresponding word
            word_to_end_syllables:
                        Dictionary from word to the set of the number of
                        syllables the word consumes when placed at the end
                        of a line
            end_syllables_to_word:
                        Dictionary from number of syllables a word consumes when
                        placed at the end of a line to the set of such words
            word_to_syllables:
                        Dictionary from word to the set of the number of
                        syllables the word normally consumes
            syllable_to_words:
                        Dictionary from number of syllables a word normally
                        consumes to the set of such words
        '''

        # Unpack data from pickle file
        with open("../data/preprocessed_data.pkl") as f:
            preprocessed_data = pickle.load(f)
            data = preprocessed_data["data"]
            word_to_id = preprocessed_data["word_to_id"]
            id_to_word = preprocessed_data["id_to_word"]
            word_to_end_syllables = preprocessed_data["word_to_end_syllables"]
            end_syllables_to_word = preprocessed_data["end_syllables_to_word"]
            word_to_syllables = preprocessed_data["word_to_syllables"]
            syllable_to_words = preprocessed_data["syllable_to_words"]

        return data, word_to_id, id_to_word, word_to_end_syllables, \
            end_syllables_to_word, word_to_syllables, syllable_to_words

    @staticmethod
    def load_data():
        '''
        Loads the data matrix pickled into 'preprocessed_data.pkl'.

        Returns:
            data:       Matrix of sonnets with the following hierarchy:
                            1st dimension: Sonnets
                            2nd dimension: Lines in sonnet
                            3rd dimensoin: Word ids in line
        '''

        # Unpack data from pickle file
        with open("../data/preprocessed_data.pkl", "rb") as f:
            preprocessed_data = pickle.load(f)
            data = preprocessed_data["data"]

        return data

    @staticmethod
    def sample_line(hmm, id_to_word, word_to_syllables, word_to_end_syllables,
                    n_syllables=10):
        punctuation = ".,!?;:()"

        # Sample and convert sentence, with buffer for punctuation
        # and ending words with too many syllables.
        emission, _ = hmm.generate_emission(3 * n_syllables)

        emission_idx = 0
        remaining = n_syllables
        sentence = ""
        while remaining > 0:
            # Make sure there are still words left in the emission.
            assert(emission_idx < 3 * n_syllables)

            emission_idx += 1
            word = id_to_word[emission[emission_idx]]

            if word not in punctuation:
                if remaining != n_syllables:
                    sentence += " "

                word_syllables = word_to_syllables[word]
                if remaining in word_syllables:
                    remaining = 0
                    sentence += word
                else:
                    end_syllables = word_to_end_syllables[word]
                    if remaining in end_syllables:
                        remaining = 0
                        sentence += word
                    else:
                        for count in word_syllables:
                            if count < remaining:
                                remaining -= count
                                sentence += word
                                break

            else:
                if remaining != n_syllables:
                    sentence += word

        return sentence.capitalize()

    @staticmethod
    def generate_sonnet(hmm, id_to_word, word_to_syllables, word_to_end_syllables,
                        n_syllables=10, n_lines=14):
        sonnet = []
        for _ in n_lines:
            sonnet.append(Utility.sample_line(
                hmm, id_to_word, word_to_syllables,
                word_to_end_syllables, n_syllables))
        return sonnet
