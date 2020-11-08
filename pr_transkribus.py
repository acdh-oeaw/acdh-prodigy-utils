import os

import requests
import json
import spacy
import lxml.etree as ET

from prodigy import get_config

rest_url = "https://transkribus.eu/TrpServer/rest"
nsmap = {
    "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
}
spacy_model = "de_core_news_sm"

config = get_config()
try:
    user = config['api_keys']['trankskribus_user']
except KeyError:
    print("no config set")
    user = os.environ.get('TRANSKRIBUS_USER', 'user')
try:
    pw = config['api_keys']['trankskribus_pw']
except KeyError:
    print("no config set")
    pw = os.environ.get('TRANSKRIBUS_PW', 'pw')


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


def get_page_keys(col_id, doc_id, user=user, pw=pw):
    doc_url = "{}/collections/{}/{}/fulldoc.xml".format(rest_url, col_id, doc_id)
    session_id = transkribus_login(user, pw, rest_url=rest_url)
    headers = {
        'cookie': "JSESSIONID={}".format(session_id),
    }
    response = requests.request("GET", doc_url, headers=headers)
    if response.ok:
        doc_xml = ET.fromstring(response.text.encode('utf8'))
        result = {}
        result["doc_url"] = doc_url
        result["doc_xml"] = doc_xml
        result["page_keys"] = doc_xml.xpath('//tsList/transcripts[1]/url/text()')
        result["page_thumbs"] = doc_xml.xpath('//pages/url/text()')
        result["page_ids"] = doc_xml.xpath('//pages/pageId/text()')

        return result
    else:
        return response.ok


def yield_samples(source):
    col_id, doc_id = source.split('::')
    page_keys = get_page_keys(col_id, doc_id)
    counter = 0
    for page_url in page_keys["page_keys"]:
        page_xml = requests.get(page_url)
        page = ET.fromstring(page_xml.text.encode('utf8'))
        text = " ".join(
            page.xpath('.//page:TextRegion/page:TextEquiv/page:Unicode/text()', namespaces=nsmap)
        )
        text = text.replace('¬\n', '').replace('\n', ' ')
        nlp = spacy.load(spacy_model)
        doc = nlp(text)
        print("found {} sents in doc: {}".format(len(list(doc.sents)), page_url))
        meta_dict = {
            "doc_id": page_url,
            "doc_url": page_keys['doc_url'],
            "page_id": page_keys["page_ids"][counter],
            "page_thumb": page_keys["page_thumbs"][counter],
            "image": page_keys["page_thumbs"][counter]
        }
        for sent in list(doc.sents):
            yield {
                "text": sent.text,
                "meta": meta_dict
            }


def yield_texts(source):
    col_id, doc_id = source.split('::')
    print(col_id, doc_id)
    page_keys = get_page_keys(col_id, doc_id)
    counter = 0
    for page_url in page_keys["page_keys"]:
        print(page_url)
        page_xml = requests.get(page_url)
        page = ET.fromstring(page_xml.text.encode('utf8'))
        for y in page.xpath(
            './/page:TextRegion/page:TextEquiv/page:Unicode/text()', namespaces=nsmap
        ):
            text = y.replace('¬\n', '').replace('\n', ' ')
            img_url = page_keys["page_thumbs"][counter]
            meta_dict = {
                "doc_id": page_url,
                "doc_url": page_keys['doc_url'],
                "page_id": page_keys["page_ids"][counter],
                "page_thumb": page_keys["page_thumbs"][counter],
                "image": page_keys["page_thumbs"][counter]
            }
            html = f"<div><p>{text}</p><img src='{img_url}' style='max-width: 100%'/></div>"
            yield {
                "text": text,
                "html": html,
                "meta": meta_dict
            }
        counter += 1
