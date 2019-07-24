# prodigy_utils

A bunch of custom loaders for prodigy

* dsebaseapp
* transkribus
* sketch-engine

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

## example dsebaseapp

annotate TEI documents stored in a dsebaseapp instance

### create dataset

`python -m prodigy dataset asbw "ASBW-Retro for gold annotations"`

### Make NER-Gold-Data

`python -m prodigy ner.make-gold asbw de_core_news_sm https://asbw-retro.acdh-dev.oeaw.ac.at::asbw-retro::editions --loader from_dsebaseapp --label PER,ORG,LOC -U`


## example transkribus

* clone the repo


### Make NER-Gold-Data

`python -m prodigy ner.make-gold asbw de_core_news_sm 44688::181839  --loader from_transkribus --label PER,ORG,LOC,MISC -U`

## example sketch-engine


### text classifier

#### make a dataset

`python -m prodigy dataset ske-amc "AMC for text classification"`

#### start prodigy

`python -m prodigy textcat.manual ske-amc de_core_news_sm amc_3.1 --loader from_ske_docs --label SPORT,CHRONIK,SONST`


### NER

`python -m prodigy ner.make-gold ske-amc de_core_news_sm amc3_demo --loader from_ske_docs --label PER,ORG,LOC,MISC`