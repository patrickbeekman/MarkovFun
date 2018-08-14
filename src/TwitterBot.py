import tweepy
import tweepy_grabber
import GenerateSentences
import pandas as pd
import os
import re

class TwitterBot:

    def __init__(self):
        self.Grabber = tweepy_grabber.TweepyGrabber()
        self.Generator = GenerateSentences.GenerateSentences()

    def main(self):
        my_followers = self.Grabber.get_users_followers(screen_name='NonsenseMarkov')
        users_tweets_path = '/home/patt/Documents/MarkovFun/data/users_tweets/'
        all_file_paths = [users_tweets_path + name for name in os.listdir(users_tweets_path)]
        old_len = len(all_file_paths)

        for index, follower in my_followers.iterrows():
            output_path = users_tweets_path + follower.loc['screen_name'] + "_tweets.json"
            if not os.path.isfile(output_path):
                self.Grabber.get_users_timeline(screen_name=follower.loc['screen_name'],
                                                output_file_path=output_path)
                all_file_paths.append(output_path)
        new_len = len(all_file_paths)

        all_text = self.extract_text(all_file_paths)
        if old_len != new_len:
            generated = self.Generator.main(all_text=all_text, new_matrix=True, num_sentences=15)
        else:
            generated = self.Generator.main(all_text=all_text, new_matrix=False, num_sentences=15)
        #print(generated)
        top_sentences = self.choose_most_unique(generated)
        print(top_sentences[0][0])
        self.Grabber.new_tweet(top_sentences[0][0])

    def extract_text(self, filepaths):
        if type(filepaths) is not list:
            list(filepaths)
        all_text = []
        for filepath in filepaths:
            file = pd.read_json(filepath)
            for text in file.iterrows():
                tweet_text = re.sub(r'http\S+', '', str(text[1].loc['text']).lower(), flags=re.MULTILINE)
                tweet_text = tweet_text.strip().replace('\n', '').replace('\r', '').replace('.', '').replace('!', '').replace('?', '').replace('rt', '')
                all_text.append(tweet_text)
        return all_text

    def choose_most_unique(self, sentences):
        unique_count = {}
        for sentence in sentences:
            unique_count[sentence] = len(set(sentence[:-1].split(" ")))
        return sorted(unique_count.items(), key=lambda kv: kv[1], reverse=True)[:3]

TwitterBot().main()