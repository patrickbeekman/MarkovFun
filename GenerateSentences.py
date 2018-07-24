import numpy as np
import pandas as pd
import sys


class GenerateSentences:

    def __init__(self):
        self.word_counts = {}
        self.training = []
        self.state_matrix = None
        self.row_totals = {}

    def main(self, all_text=[]):
        print("Starting generator")
        #self.read_text_file('/home/patt/Documents/MarkovFun/OhThePlacesYoullGo-Seus.txt')
        self.training = all_text
        unique_size = self.count_unique()
        print("Unique words: " + unique_size)
        # initialize pandas to 0s and add row/column labels with word_counts keys
        zeros = np.zeros((unique_size, unique_size))
        self.state_matrix = pd.DataFrame(zeros, index=self.word_counts.keys(),
                                         columns=self.word_counts.keys())
        self.initialize_states()
        self.count_row_totals()
        self.build_state_matrix()
        print("State Matrix built")
        top_words = sorted(self.word_counts.items(), key=lambda kv: kv[1], reverse=True)
        len_words = len(top_words)
        print("Generating the sentences.")
        generated_sentences = []
        for i in range(int(sys.argv[1])):
            generated_sentences.append(self.generate_sentence(state=top_words[i%len_words][0]))
        return generated_sentences

    def count_unique(self):
        for sentence in self.training:
            words = sentence.lower().split(' ')
            for word in words:
                try:
                    self.word_counts[word] = self.word_counts[word] + 1
                except KeyError:
                    self.word_counts[word] = 1
        return len(self.word_counts.keys())

    def initialize_states(self):
        print("Initializing states matrix")
        for sentence in self.training:
            words = sentence.lower().split(' ')
            for i, word in enumerate(words):
                try:
                    next_word = words[i+1]
                except IndexError:
                    break # really?
                self.state_matrix.loc[word][next_word] = 999

    def build_state_matrix(self):
        for word_x in self.word_counts.keys():
            for word_y in self.word_counts.keys():
                if int(self.state_matrix.loc[word_x][word_y]) == 999:
                    self.state_matrix.loc[word_x][word_y] = self.word_counts[word_y]/self.row_totals[word_x]

    def count_row_totals(self):
        for word_x in self.word_counts.keys():
            for word_y in self.word_counts.keys():
                if int(self.state_matrix.loc[word_x][word_y]) == 999:
                    try:
                        self.row_totals[word_x] += self.word_counts[word_y]
                    except KeyError:
                        self.row_totals[word_x] = self.word_counts[word_y]

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

    def read_text_file(self, filepath):
        self.training = []
        with open(filepath, 'r') as file:
            tmp_lines = file.readlines()
        for line in tmp_lines:
            stripped = line.rstrip('\n').replace('!', '').replace('?', '').replace('...', ' ').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
            if len(stripped) >= 1:
                self.training.append(stripped)
