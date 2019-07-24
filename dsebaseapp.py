import json
import re
import requests
import spacy
from spacy.symbols import ORTH


def get_doc_list(domain, app_name, collection='editions', verbose=True):
    """ retrieves a list of doc-uris stored in a dsebaseapp
        :param domain: Domain hosting the dsebaseapp instance, e.g. "http://127.0.0.1:8080"
        :param app_name: The name of the dsebaseapp instance.
        :param collection: The name of the collection to process
        :verbose: Defaults to True and logs some basic information
        :return: A list of absolut URLs
    """

    endpoint = "{}/exist/restxq/{}/api/collections/{}".format(domain, app_name, collection)
    r = requests.get(endpoint)
    if r.status_code == 200:
        if verbose:
            print('connection to: {} status: all good'.format(endpoint))
    else:
        print(
            "There is a problem with connection to {}, status code: {}".format(
                endpoint, r.status_code
            )
        )
        return None
    hits = r.json()['result']['meta']['hits']
    all_files = requests.get("{}?page[size]={}".format(endpoint, hits)).json()['data']
    files = ["{}{}".format(domain, x['links']['self']) for x in all_files]
    if verbose:
        print("{} documents found".format(len(files)))
    return files


def yield_samples(source):
    """ fetches TEI-Docs from an dsebaseapp instance and yields JSONL samples
        :param source: a string follwoing this scheme {domain}::{app_name}::{collection}
        return: yields samples {"text": "Lorem ipsums"}
    """
    my_terms = [
        "Ew.",
        "Ah.",
        "FML.",
        "Ag.",
        "Se. "
    ]
    domain, app_name, collection = source.split('::')
    collection = 'editions'
    spacy_model = 'de_core_news_sm'
    min_len = 15
    verbose = True
    files = get_doc_list(domain, app_name, collection, verbose=verbose)
    nlp = spacy.load(spacy_model)
    exceptions = {}
    for x in my_terms:
        exceptions[x] = [
            {ORTH: x}
        ]
    for key, value in exceptions.items():
        nlp.tokenizer.add_special_case(key, value)
    for x in files:
        url = "{}?format=text".format(x)
        r = requests.get(url)
        text = r.text
        text = re.sub('\s+', ' ', text).strip()
        text = re.sub('- ', '', text).strip()
        doc = nlp(text)
        if verbose:
            print("found {} sents in doc".format(len(list(doc.sents))))
        for sent in list(doc.sents):
                yield {"text": sent.text}
