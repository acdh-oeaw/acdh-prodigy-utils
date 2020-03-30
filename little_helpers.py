import requests

ABBR_BASE = "https://abbr.acdh.oeaw.ac.at/api/abbreviations/?format=json"


def yield_abbr(ABBR_BASE):
    """ iterator to yield all abbreviations from ABBR_BASE """
    next = True
    url = ABBR_BASE
    counter = 0
    while next:
        response = requests.request("GET", url)
        result = response.json()
        if result.get('next', False):
            url = result.get('next')
        else:
            next = False
        results = result.get('results')
        for x in results:
            text = x.get('orth')
            counter += 1
            yield(text)
