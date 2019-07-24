import requests
import json
import spacy

from prodigy import get_config

rest_url = "http://ske.herkules.arz.oeaw.ac.at/run.cgi"
spacy_model = "de_core_news_sm"

config = get_config()
user = config['api_keys']['ske_user']
pw = config['api_keys']['ske_pw']


def get_start_toks(user, pw, rest_url, corpus_id):
    """ yields the number of the first token of each document in a corpus
        :param user: username for the sketch engine instance
        :param pw: password for the sketch engine instance
        :param rest_url: The base URL of the sketch engine instance
        :corpus_id: The name/id of the sketch engine corpus
        :return: yields the IDs of a document's first token.
    """
    auth = (user, pw)
    next = True
    counter = 1
    while next:
        url = "{}/first".format(rest_url)
        querystring = {
            "corpname": corpus_id,
            "queryselector": "cqlrow",
            "cql": "<doc> []",
            "default_attr": "word",
            "format": "json",
            "fromp": '{}'.format(counter)
        }
        response = requests.request("GET", url, auth=auth, params=querystring)
        result = response.json()
        if result.get('nextlink', False):
            next = True
            counter += 1
        else:
            next = False
        for line in result.get('Lines'):
            yield line.get('toknum')


def yield_samples(source):
    """ fetches all documents form a sketch-engine corpus and yields their texts.
        :param source: the name of the corpus
        :return: yields samples {"text": ""}
    """
    print(source)
    corpus_id = source
    auth = (user, pw)
    docs = get_start_toks(user, pw, rest_url, corpus_id)
    for x in docs:
        url = "{}/structctx?corpname={};pos={}".format(rest_url, corpus_id, x)
        response = requests.request("GET", url, auth=auth)
        if response.ok:
            yield {"text": response.text}
        else:
            continue
