import requests
import json


def yield_samples(source):
    """ yields samples from and DRF-Endpoint
        :param source: {URL::text_key::min_len}; something like:\
        source = "https://annotator.acdh-dev.oeaw.ac.at/api/nersampletodo/?format=json::text::50"
        :return: yields samples {"text": "Lorem ipsums", "meta": {"url": drf-url, "field": lookup}}
    """
    rest_url, lookup, min_len = source.split("::")
    next = True
    url = rest_url
    while next:
        print(url)
        response = requests.request("GET", url)
        result = response.json()
        if result.get('next', False):
            url = result.get('next')
        else:
            next = False
        results = result.get('results')
        for x in results:
            text = x.get(lookup)
            if len(text) >= int(min_len):
                result = {
                        "text": x.get(lookup),
                        "meta": {
                            "url": x.get('url'),
                            "field": lookup
                        }
                    }
                yield result
