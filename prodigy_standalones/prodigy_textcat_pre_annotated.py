import prodigy
import spacy
from prodigy_standalones import data_provider


def stream_pre_annotated():

    nlp = spacy.blank("de")
    nlp.add_pipe(nlp.create_pipe("textcat"))
    nlp.from_disk("./dummy_model")

    options = data_provider.choice_options

    for text in data_provider.get_basic_text_stream():

        cat_scores = nlp(text).cats
        options_accepted = []

        for o in options:
            if cat_scores[o["text"]] >= 0.5:
                options_accepted.append(o["id"])

        yield {
            "text": text,
            "options": options,
            "accept": options_accepted
        }


@prodigy.recipe("prodigy_textcat_pre_annotated_id")
def custom_recipe():

    return {
        "view_id": "choice",
        "dataset": "prodigy_standalone_dataset",
        "stream": stream_pre_annotated(),
        "config": {
            "choice_style": "multiple"
        }
    }


prodigy.serve("prodigy_textcat_pre_annotated_id")
