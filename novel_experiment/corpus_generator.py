"""
In order to ensure the corpus used in the novel experiment is non-trivial we want to ensure
that the lexicon is shared between both types of sentences, negative and positive. To do
so we generate the corpus using the following CFG and a set of common lexicon.
All words take the singular form for simplicity. The generated sentences are then manually labelled as positive
or negative
"""
from functools import reduce
import random

from nltk.parse.generate import generate
from nltk import CFG

NOUNS = ["'alice'", "'bob'", "'man'", "'programmer'", "'linguist'", "'chef'"]
ADJECTIVES = ["'red'", "'blue'", "'curious'", "'warm'", "'cold'", "'informed'",
              "'mean'", "'angry'", "'rude'", "'ignorant'", "'annoying'",
              "'happy'", "'joyful'", "'skilled'", "'kind'", "'helpful'", "'pleasant'"]
VERBS = ["'sees'", "'asks'", "'approaches'",
         "'hates'", "'avoids'", "'loathes'", "'misleads'", "'attacks'",
         "'loves'", "'helps'", "'wants'", "'respects'", "'likes'"]

production_rules = ["S -> NP VP", "NP -> A N", "NP -> N", "VP -> V NP",
                    f"N -> {reduce(lambda x, y: f'{x} | {y}', NOUNS)}",
                    f"A -> {reduce(lambda x, y: f'{x} | {y}', ADJECTIVES)}",
                    f"V -> {reduce(lambda x, y: f'{x} | {y}', VERBS)}"]

cfg = CFG.fromstring(reduce(lambda x, y: f'{x}\n{y}', production_rules))
sentences = list(generate(cfg))
print(f'{len(sentences)} sentences generated')
print('Selecting 150 sentences')
selected_sentences = random.sample(sentences, 150)
formatted_sentences = list(map(lambda z: reduce(lambda x,y: f'{x} {y}', z), selected_sentences))
print("Generated sentences will be presented, press 1 to indicate it is positive, 2 for negative, press 0 to skip")
positive = []
negative = []
for sentence in formatted_sentences:
    sentiment = input(f'{sentence}: ')
    if sentiment == '1' and len(positive) < 65:
        positive.append(sentence + '\n')
    if sentiment == '2' and len(negative) < 65:
        negative.append(sentence + '\n')
with open("negative_corpus.txt", 'w') as negative_corpus:
    negative_corpus.writelines(negative)
with open("positive_corpus.txt", 'w') as positive_corpus:
    positive_corpus.writelines(positive)
