import numpy as np
import pandas as pd
import sys
from tqdm import tqdm
import pickle

'''
    Takes as input a list of sentences to parse and generate new sentences
    based on occurrence probabilities using a Markov Chain.
'''
class GenerateSentences:

    def __init__(self):
        self.word_counts = {}
        self.training = []
        self.state_matrix = None
        self.row_totals = {}

    def main(self, all_text=[], new_matrix=False, num_sentences=1):
        print("Starting generator")
        if new_matrix: # should a new state matrix be generated (this takes longer than using the cached version
            self.training = all_text
            unique_size = self.count_unique()
            print("Unique words: " + str(unique_size))
            # initialize pandas to 0s and add row/column labels with word_counts keys
            zeros = np.zeros((unique_size, unique_size))
            self.state_matrix = pd.DataFrame(zeros, index=self.word_counts.keys(),
                                             columns=self.word_counts.keys())
            self.initialize_states()
            self.count_row_totals()
            self.build_state_matrix()
            print("State Matrix built")
            self.save_state_matrix('/home/patt/Documents/MarkovFun/data/state_matrix.pkl')
            self.save_word_counts('/home/patt/Documents/MarkovFun/data/word_counts.pkl')
        else:
            self.state_matrix = self.load_state_matrix('/home/patt/Documents/MarkovFun/data/state_matrix.pkl')
            self.word_counts = self.load_word_counts('/home/patt/Documents/MarkovFun/data/word_counts.pkl')

        top_words = sorted(self.word_counts.items(), key=lambda kv: kv[1], reverse=True)
        len_words = len(top_words)
        print("Generating the sentences.")
        generated_sentences = []
        for i in range(int(num_sentences)):
            generated_sentences.append(self.generate_sentence(state=top_words[i%len_words][0]))
        return generated_sentences

    '''
        Creates a set of all words and their associated occurrence count, 
        this is saved in self.word_counts
    '''
    def count_unique(self):
        for sentence in tqdm(self.training):
            words = sentence.lower().split(' ')
            for word in words:
                try:
                    self.word_counts[word] = self.word_counts[word] + 1
                except KeyError:
                    self.word_counts[word] = 1
        return len(self.word_counts.keys())

    '''
        Create a NxN state matrix where N is the set of all words. This initial matrix can be
        interpreted as rows=word from and columns = word to. For example the words 'from to'
        would be accessing state_matrix.loc['from']['to'] NOT state_matrix.loc['to']['from'],
        this is then set to a sentinel value of 999 for future use when calculating probabilities.
    '''
    def initialize_states(self):
        print("Initializing states matrix")
        for sentence in tqdm(self.training):
            words = sentence.lower().split(' ')
            for i, word in enumerate(words):
                try:
                    next_word = words[i+1]
                except IndexError:
                    break # really?
                self.state_matrix.loc[word][next_word] = 999

    '''
        Create the self.row_totals array which sums up the word counts for each row word. This is
        used to calculate probabilities in the build_state_matrix() method by using the formula 
        #single_word_occurrences / row_total so that each `to` word in the columns has a prob that
        sums up to 1.
    '''
    def count_row_totals(self):
        print("Staring to count row totals")
        # sum up the rows by creating a boolean list of the row that is 999
        # sum up the word counts using the boolean list to index
        for word in tqdm(self.word_counts.keys()):
            other_states = list(self.state_matrix.loc[word] == 999)
            self.row_totals[word] = pd.DataFrame(list(self.word_counts.values()))[other_states].sum()
        print("Done counting row totals")

    def build_state_matrix(self):
        print("Starting to build state matrix")
        for word in tqdm(self.word_counts.keys()):
            other_states = self.state_matrix.loc[word] > 0#== 999)
            row = self.state_matrix.loc[word][other_states]
            for index, val in row.iteritems():
                self.state_matrix.loc[word][index] = self.word_counts[index]/self.row_totals[word]

    '''
        Generate new sentences by using the probabilities to randomly jump around the state_matrix.
    '''
    def generate_sentence(self, state='the'):
        sentence = state + ' '
        while sum(self.state_matrix.loc[state]) != 0 and len(sentence.split(' ')) <= 15:
            p = np.array(self.state_matrix.loc[state])
            p /= sum(p) # normalized
            new_state = np.random.choice(np.array(list(self.word_counts.keys())), 1, p=p)
            sentence += (new_state[0] + ' ')
            state = new_state[0]
        sentence = sentence[0].upper() + sentence[1:-1] + '.'
        return sentence

    def save_state_matrix(self, filepath):
        self.state_matrix.to_pickle(filepath)

    def load_state_matrix(self, filepath):
        return pd.read_pickle(filepath)

    def save_word_counts(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.word_counts, f, pickle.HIGHEST_PROTOCOL)

    def load_word_counts(self, filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    '''
        Used for testing and for large input text files.
    '''
    def read_text_file(self, filepath):
        self.training = []
        with open(filepath, 'r') as file:
            tmp_lines = file.readlines()
        for line in tmp_lines:
            stripped = line.rstrip('\n').replace('!', '').replace('?', '').replace('...', ' ').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
            if len(stripped) >= 1:
                self.training.append(stripped)

# GenerateSentences().main(new_matrix=True)