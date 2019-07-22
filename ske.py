import requests
import json
import spacy

from secret import SKE

rest_url = "http://ske.herkules.arz.oeaw.ac.at/run.cgi"
spacy_model = "de_core_news_sm"

user = SKE['user']
pw = SKE['pw']


def get_start_toks(user, pw, rest_url, corpus_id):
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


def yield_docs(source):
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
