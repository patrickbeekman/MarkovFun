import tweepy
import tweepy_grabber
import GenerateSentences
import pandas as pd
import os

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
            generated = self.Generator.main(all_text, False)
        else:
            generated = self.Generator.main(all_text, True)
        print(generated)

    def extract_text(self, filepaths):
        if type(filepaths) is not list:
            list(filepaths)
        all_text = []
        for filepath in filepaths:
            file = pd.read_json(filepath)
            for text in file.iterrows():
                all_text.append(text[1].loc['text'])
        return all_text


TwitterBot().main()