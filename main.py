import discord
from env_vars import TOKEN
from GetRank import LastMatch
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow as tf
import random
import json
import pickle


nltk.download('punkt')

SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')
# Deep learning
with open("intents.json") as file:
    data = json.load(file)
#Put an X in try when intent data has changed, or delete old model.
try:
    with open("data.pickle", "rb") as f:
        words,labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
    # Take lists and turn them into arrays
    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
#2 Hidden layers
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
#output layer which is not hidden and has softmax applied
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")

except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    


# SmiteAPI + Discord Bot
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('rank'):
        get_user_name = msg.split('rank ', 1)[1]
        rank = LastMatch(get_user_name).conquest_rank()
        await message.channel.send(get_user_name + ' is ' + rank)

    if msg.startswith('is ben een noob?'):
        await message.channel.send('Jazeker')

    if msg.startswith('is leendert een noob?'):
        rankleendert = LastMatch(get_user_name).conquest_rank()
        await message.channel.send('Nee die is toch ' + rankleendert)

    if msg.startswith('last match'):
        get_user_name = msg.split('last match ', 1)[1]
        rankslastmatch = LastMatch(get_user_name).last_match_ranks()

        await message.channel.send(rankslastmatch)


# TODO: Add error message when bot is offline
# TODO: Add error message when name is misspelled
# if msg.startswith('build'):
#
#     get_user_name = msg.split('build ', 1)[1]
#     # rankslastmatch = LastMatch(get_user_name).last_match_ranks()
#
#     # await message.channel.send(rankslastmatch)
client.run(TOKEN)
