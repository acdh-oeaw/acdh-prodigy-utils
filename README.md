# prodigy_utils

A bunch of custom loaders for prodigy

* dsebaseapp
* transkribus
* sketch-engine
* django-rest-framework based APIs

# install

* clone the repo
* build the package (in your virtual environment) `python setup.py develop`
* add needed api-credentials to your `prodigy.json` config file like
```python
"api_keys": {
    "ske_user": "someusername",
    "ske_pw": "somepassword",
    "trankskribus_user": "someusername",
    "trankskribus_pw": "somepassword"
}
```

also install lxml and requests

## example dsebaseapp

annotate TEI documents stored in a dsebaseapp instance

### create dataset

`python -m prodigy dataset asbw "ASBW-Retro for gold annotations"`

### Make NER-Gold-Data

`python -m prodigy ner.make-gold asbw de_core_news_sm https://asbw-retro.acdh-dev.oeaw.ac.at::asbw-retro::editions --loader from_dsebaseapp --label PER,ORG,LOC -U`

## example django-rest-framework

`python -m prodigy ner.make-gold drf de_core_news_sm https://annotator.acdh-dev.oeaw.ac.at/api/nersampletodo/?format=json::text::50 --loader from_drf --label PER,ORG,LOC,MISC -U`

## example transkribus

### Make NER-Gold-Data

`python -m prodigy ner.make-gold asbw de_core_news_sm 44688::181839  --loader from_transkribus --label PER,ORG,LOC,MISC -U`

### text classifier

#### make a dataset

`python -m prodigy dataset mpr_retro_ungarn_textcat "MPR-Ungarn for text classification"`

#### start prodigy

`python -m prodigy textcat.manual mpr_retro_ungarn_textcat de_core_news_sm 45410::187485 --loader from_transkribus_regions --label PB,P,REGEST,NOTE,MINUTEH,OTHER`

## example sketch-engine


### text classifier

#### make a dataset

`python -m prodigy dataset ske-amc "AMC for text classification"`

#### start prodigy

`python -m prodigy textcat.manual ske-amc de_core_news_sm amc_3.1 --loader from_ske_docs --label SPORT,CHRONIK,SONST`


### NER

`python -m prodigy ner.make-gold ske-amc de_core_news_sm amc3_demo --loader from_ske_docs`
