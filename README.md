# MarkovFun
#### Messing around with Markov Chains

# Twitter bot
I have also created a simple twitter bot that will generate new tweets based off the tweets of its followers. For example if only my personal twiter account is following the bot then it will use my all of the words in my tweets to generate new tweets. The tweets are still jibberish because they don't follow a sentence structure. The essence of "sentence strucutre" in the tweets is that of a probabilistic reconstruction of the sentence strucutre in the tweets of its followers. The next iteration of this app will be to include some sort of sentence strucuture in my markov chain model.

https://twitter.com/NonsenseMarkov

# What are Markov Chains?
- https://en.wikipedia.org/wiki/Markov_chain
- http://setosa.io/ev/markov-chains/

## GenerateSentences.py
This program simply creates a markov chain from a list of sentences and then cycles through the transition matrix to generate new sentecnes.

#### Some example input:
- The cow jumped over the moon
- The chicken crossed the road
- The human skipped over the stream
- The river loves the mountain
- The horses ride on rainbows
- The mushrooms dance in the rain
- The mushrooms skipped over the river
- The fireflies crossed the night sky
- The human shivered in the grass as the wind blew

#### Some example output:
- The human skipped over the grass as the horses ride on rainbows.
- The human skipped over the chicken crossed the horses ride on rainbows.
- The river loves the chicken crossed the cow jumped over the night sky.
- The river loves the stream.
- The night sky.
- The human shivered in the moon.
- The river loves the moon.

---

I Then experimented by using the whole text of [Dr. Seuss's Oh the places you'll go](http://denuccio.net/ohplaces.html)!

#### Output:
- The guy who'll decide where to your day.
- The waiting and frequently do you will go you may not in for a slump.
- The road between hither and on and you the high heights.
- The weather be best of town.
- The great places you'll get so confused.
- The places you'll start in your shoes full of course.
- The places you'll play lonely games too smart to your elbow and the whole wide.
- The great tact.
- The lead.
- The great places you'll go on and the best of the rain to stay out.

