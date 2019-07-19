import requests
import json
import spacy
import lxml.etree as ET

from secret import TRANSKRIBUS

rest_url = "https://transkribus.eu/TrpServer/rest"
nsmap = {
    "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
}
spacy_model = "de_core_news_sm"

user = TRANSKRIBUS['user']
pw = TRANSKRIBUS['pw']


def transkribus_login(user, pw, rest_url=rest_url):
    url = "{}/auth/login".format(rest_url)
    payload = "user={}&pw={}".format(user, pw)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.ok:
        session_id = response.text.split('<sessionId>')[1].split('</sessionId>')[0]
        return session_id
    else:
        response.ok


def get_page_keys(col_id, doc_id):
    doc_url = "{}/collections/{}/{}/fulldoc.xml".format(rest_url, col_id, doc_id)
    session_id = transkribus_login(TRANSKRIBUS['user'], TRANSKRIBUS['pw'], rest_url=rest_url)
    headers = {
        'cookie': "JSESSIONID={}".format(session_id),
    }
    response = requests.request("GET", doc_url, headers=headers)
    if response.ok:
        doc_xml = ET.fromstring(response.text.encode('utf8'))
        return doc_xml.xpath('//transcripts/url/text()')
    else:
        return response.ok


def yield_samples(source):
    col_id, doc_id = source.split('::')
    page_keys = get_page_keys(col_id, doc_id)
    for page_url in page_keys:
        page_xml = requests.get(page_url)
        page = ET.fromstring(page_xml.text.encode('utf8'))
        text = " ".join(
            page.xpath('.//page:TextRegion/page:TextEquiv/page:Unicode/text()', namespaces=nsmap)
        )
        text = text.replace('¬\n', '').replace('\n', ' ')
        nlp = spacy.load(spacy_model)
        doc = nlp(text)
        print("found {} sents in doc: {}".format(len(list(doc.sents)), page_url))
        for sent in list(doc.sents):
            yield {"text": sent.text}
