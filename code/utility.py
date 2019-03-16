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
import random
import re

class Utility:
    '''
    Utility for the HMM files.
    '''

    def __init__(self):
        pass

    @staticmethod
    def load_rhymes_pkl(pkl_name="../data/preprocessed_data.pkl"):
        with open(pkl_name, "rb") as f:
            preprocessed_data = pickle.load(f)
            rhyme_id_to_word_ids = preprocessed_data["rhyme_id_to_word_ids"]
            word_id_to_rhyme_id = preprocessed_data["word_id_to_rhyme_id"]

        return rhyme_id_to_word_ids, word_id_to_rhyme_id
        
    
    @staticmethod
    def load_pkl(pkl_name="../data/preprocessed_data.pkl"):
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
        with open(pkl_name, "rb") as f:
            preprocessed_data = pickle.load(f)
            data = preprocessed_data["data"]
            word_to_id = preprocessed_data["word_to_id"]
            id_to_word = preprocessed_data["id_to_word"]
            word_to_end_syllables = preprocessed_data["word_to_end_syllables"]
            end_syllable_to_words = preprocessed_data["end_syllable_to_words"]
            word_to_syllables = preprocessed_data["word_to_syllables"]
            syllable_to_words = preprocessed_data["syllable_to_words"]

        return data, word_to_id, id_to_word, word_to_end_syllables, \
            end_syllable_to_words, word_to_syllables, syllable_to_words

    @staticmethod
    def load_data(pkl_name="../data/preprocessed_data.pkl"):
        '''
        Loads the data matrix pickled into 'preprocessed_data.pkl'.

        Returns:
            data:       Matrix of sonnets with the following hierarchy:
                            1st dimension: Sonnets
                            2nd dimension: Lines in sonnet
                            3rd dimensoin: Word ids in line
        '''

        # Unpack data from pickle file
        with open(pkl_name, "rb") as f:
            preprocessed_data = pickle.load(f)
            data = preprocessed_data["data"]

        return data

    @staticmethod
    def sample_line(emission, id_to_word, word_to_syllables,
                    word_to_end_syllables, n_syllables, emission_idx):
        # Helper function to add leading space to word when needed.
        def add_word(word, remaining):
            addition = ""
            if remaining != n_syllables:
                addition += " "
            addition += word
            return addition

        punctuation = ".,!?;:()"
        end_punctuation = ".!?"
        parantheses = "()"
        capitalize = True

        remaining = n_syllables
        line = ""
        while remaining > 0:
            # Make sure there are still words left in the emission.
            assert(emission_idx < len(emission))

            emission_idx += 1
            word = id_to_word[emission[emission_idx]]

            if word not in punctuation:
                word_syllables = word_to_syllables[word]
                end_syllables = word_to_end_syllables[word]
                was_prev_word = True

                if capitalize:
                    word = word.capitalize()
                    capitalize = False

                if word == 'i':
                    word = word.capitalize()

                if remaining in word_syllables:
                    line += add_word(word, remaining)
                    remaining = 0
                else:
                    if remaining in end_syllables:
                        line += add_word(word, remaining)
                        remaining = 0
                    else:
                        for count in word_syllables:
                            if count < remaining:
                                line += add_word(word, remaining)
                                remaining -= count
                                break

            else:
                if remaining != n_syllables \
                        and word not in parantheses \
                        and was_prev_word:
                    line += word
                    was_prev_word = False

                    if word in end_punctuation:
                        capitalize = True

        return emission_idx, line

    @staticmethod
    def generate_rhyming_poem(hmm, id_to_word, word_to_syllables,
                              word_to_end_syllables, n_syllables=10,
                              n_lines=14,
                              rhyme_id_to_word_ids=None, 
                              word_id_to_rhyme_id=None,
                              rhyme_scheme='sonnet'):
        assert(rhyme_scheme in ['sonnet', 'limerick', 'petrarchan'])
        
        if not isinstance(n_syllables, (list,)):
            n_syllables = [n_syllables] * n_lines
        else:
            n_lines = len(n_syllables)
            
        poem = []
        n_rhyme_ids = len(rhyme_id_to_word_ids.keys())
        n_word_ids = len(word_to_syllables)
        if rhyme_scheme == 'sonnet':
            rhyme_ids = [random.randint(0, n_rhyme_ids - 1) for i in range(n_lines // 2)]
        if rhyme_scheme == 'petrarchan':
            rhyme_ids = []
            while len(rhyme_ids) != 5:
                rhyme_id = random.randint(0, n_rhyme_ids - 1)
                if len(rhyme_id_to_word_ids[rhyme_id]) > 3 or len(rhyme_ids) > 2:
                    # print(rhyme_id_to_word_ids[rhyme_id])
                    rhyme_ids.append(rhyme_id)
        if rhyme_scheme == 'limerick':
            rhyme_ids = []
            while len(rhyme_ids) != 2:
                rhyme_id = random.randint(0, n_rhyme_ids - 1)
                if len(rhyme_id_to_word_ids[rhyme_id]) > 2 or len(rhyme_ids) == 1:
                    rhyme_ids.append(rhyme_id)
        # make an empty array
        emissions = [None] * n_lines
        for i, rhyme_id in enumerate(rhyme_ids):
            rhyme_set = rhyme_id_to_word_ids[rhyme_id]
            
            if rhyme_scheme == 'sonnet':
                seed_word_id_1 = random.choice(list(rhyme_set))
                if len(rhyme_set) == 1:
                    seed_word_id_2 = seed_word_id_1
                else:
                    seed_word_id_2 = random.choice(
                        list(rhyme_set.difference({seed_word_id_1})))

                # print([id_to_word[word_id]
                #        for word_id in [seed_word_id_1, seed_word_id_2]])

                emission_1, _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_1)

                # print([id_to_word[word_id] for word_id in emission_1])
                emission_2, _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_2)
                if i == 6:
                    emissions[12] = emission_1
                    emissions[13] = emission_2
                elif i % 2 == 0:
                    emissions[i * 2] = emission_1
                    emissions[i * 2 + 2] = emission_2
                else:
                    emissions[i * 2 - 1] = emission_1
                    emissions[i * 2 + 1] = emission_2
                                
            if rhyme_scheme == 'petrarchan':
                seed_word_ids = []
                for _ in range(4):
                    seed_word_id = random.choice(list(rhyme_set))
                    seed_word_ids.append(seed_word_id)
                    if len(rhyme_set) > 1:
                        rhyme_set.remove(seed_word_id)
                        # print("removed", seed_word_id)
                        # print(rhyme_set)

                group_emissions = [None] * 4
                for j in range(4):
                    group_emissions[j], _ = hmm.generate_reverse_emission(
                        2 * max(n_syllables), seed_word_ids[j])

                if i == 0:
                    emissions[0] = group_emissions[0]
                    emissions[3] = group_emissions[1]
                    emissions[4] = group_emissions[2]
                    emissions[7] = group_emissions[3]
                elif i == 1:
                    emissions[1] = group_emissions[0]
                    emissions[2] = group_emissions[1]
                    emissions[5] = group_emissions[2]
                    emissions[6] = group_emissions[3]
                elif i == 2:
                    emissions[8] = group_emissions[0]
                    emissions[12] = group_emissions[1]
                elif i == 3:
                    emissions[9] = group_emissions[0]
                    emissions[10] = group_emissions[1]
                elif i == 4:
                    emissions[11] = group_emissions[0]
                    emissions[13] = group_emissions[1]
            
            if rhyme_scheme == 'limerick':
                seed_word_id_1 = random.choice(list(rhyme_set))
                if len(rhyme_set) == 1:
                    seed_word_id_2 = seed_word_id_1
                    seed_word_id_3 = seed_word_id_1
                elif len(rhyme_set) == 2:
                    seed_word_id_2 = random.choice(
                        list(rhyme_set.difference({seed_word_id_1})))
                    seed_word_id_3 = random.choice(list(rhyme_set))
                else:
                    seed_word_id_2 = random.choice(
                        list(rhyme_set.difference({seed_word_id_1})))
                    seed_word_id_3 = random.choice(
                        list(rhyme_set.difference({seed_word_id_1, seed_word_id_2})))

                # print([id_to_word[word_id]
                #        for word_id in [seed_word_id_1, seed_word_id_2]])

                emission_1, _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_1)

                # print([id_to_word[word_id] for word_id in emission_1])
                emission_2, _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_2)

                emission_3, _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_3)
                
                if i == 0:
                    emissions[0] = emission_1
                    emissions[1] = emission_2
                    emissions[4] = emission_3
                else:
                    emissions[2] = emission_1
                    emissions[3] = emission_2

        # fill empty emissions
        for i, emission in enumerate(emissions):
            if emission is None:
                rhyme_id = random.randint(0, n_rhyme_ids - 1)
                rhyme_set = rhyme_id_to_word_ids[rhyme_id]
                seed_word_id_1 = random.choice(list(rhyme_set))
                emissions[i], _ = hmm.generate_reverse_emission(
                    2 * max(n_syllables), seed_word_id_1)
                
        # Sample and convert sentence, with buffer for punctuation
        # and ending words with too many syllables.

        for (emission, n) in zip(emissions, n_syllables):
            emission_idx = 0
            # print(emission)
            emission_idx, line = Utility.sample_line(
                [69] + emission, id_to_word, word_to_syllables,
                word_to_end_syllables, n, emission_idx)
            if line[0] in ",.:;?!() ":
                line = line[1:]
            reversed_line = ''
            for word in reversed(line.split()):
                if word[-1] == ',':
                    word = word[:-1]
                    reversed_line += ','
                reversed_line += ' ' + word
            reversed_line = reversed_line[1:]
            
            poem.append(reversed_line.capitalize())

        return poem
    
    @staticmethod
    def generate_poem(hmm, id_to_word, word_to_syllables,
                      word_to_end_syllables, n_syllables=10,
                      n_lines=14,
                      rhyme_id_to_word_id=None, 
                      word_id_to_rhyme_id=None):
        if not isinstance(n_syllables, (list,)):
            n_syllables = [n_syllables] * n_lines

        poem = []

        # Sample and convert sentence, with buffer for punctuation
        # and ending words with too many syllables.
        emission, _ = hmm.generate_emission(3 * sum(n_syllables))

        emission_idx = 0
        for n in n_syllables:
            emission_idx, line = Utility.sample_line(
                emission, id_to_word, word_to_syllables,
                word_to_end_syllables, n, emission_idx)
            poem.append(line)

        return poem

    @staticmethod
    def generate_sonnet(hmm, id_to_word, word_to_syllables,
                        word_to_end_syllables):
        return Utility.generate_poem(hmm, id_to_word, word_to_syllables,
                                     word_to_end_syllables, 10, 14)

