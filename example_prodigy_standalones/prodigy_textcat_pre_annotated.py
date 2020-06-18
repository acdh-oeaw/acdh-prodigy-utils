import prodigy
import spacy


# local dict overriding any prodigy.json file
prodigy_config = {
    "choice_style": "multiple"
}


def get_basic_text_stream():

    yield "The story so far:"
    yield "In the beginning the Universe was created."
    yield "This has made a lot of people very angry "
    yield "and been widely regarded as a bad move."


choice_options = [
    {"id": 0, "text": "category A"},
    {"id": 1, "text": "category B"},
    {"id": 2, "text": "category C"},
]


def stream_pre_annotated():

    nlp = spacy.blank("en")
    nlp.add_pipe(nlp.create_pipe("textcat"))
    nlp.from_disk("./dummy_model")

    options = choice_options

    for text in get_basic_text_stream():

        cat_scores = nlp(text).cats
        options_accepted = []

        for o in options:
            if cat_scores[o["text"]] >= 0.5:
                options_accepted.append(o["id"])

        yield {
            "text": text,
            "options": options,
            "accept": options_accepted,
            "meta": {
                "score": str(cat_scores)
            }
        }


@prodigy.recipe("prodigy_textcat_pre_annotated_id")
def custom_recipe():

    return {
        "view_id": "choice",
        "dataset": "prodigy_standalone_dataset",
        "stream": stream_pre_annotated(),
    }


prodigy.serve("prodigy_textcat_pre_annotated_id", **prodigy_config)
