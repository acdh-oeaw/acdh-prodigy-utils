import requests
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, HYPHENS
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex


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


def customize_infixes():
    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
            r"(?<=[{a}0-9])[:<>/](?=[{a}])".format(a=ALPHA),
        ]
    )
    infix_re = compile_infix_regex(infixes)
    return infix_re
