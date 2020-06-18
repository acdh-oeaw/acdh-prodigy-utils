import prodigy
from example_prodigy_standalones import data_provider


# local dict overriding any prodigy.json file
prodigy_config = {
    "choice_style": "multiple"
}


def stream_most_basic():

    for t in data_provider.get_basic_text_stream():

        yield {
            "text": t,
            "options": data_provider.choice_options
        }


@prodigy.recipe("prodigy_most_basic_id")
def custom_recipe():

    return {
        "view_id": "choice",
        "dataset": "prodigy_standalone_dataset",
        "stream": stream_most_basic(),
    }


prodigy.serve("prodigy_most_basic_id", **prodigy_config)
