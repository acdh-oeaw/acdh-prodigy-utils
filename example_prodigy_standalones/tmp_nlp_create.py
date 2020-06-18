import spacy
from example_prodigy_standalones import data_provider


def train(nlp):

    train_iteration_limit = 1

    from datetime import datetime

    cats = {}
    for cat in data_provider.choice_options:
        cats[cat["text"]] = 1

    train_data = [
        ("text 1", {"cats": cats}),
        ("text 2", {"cats": cats}),
        ("text 3", {"cats": cats})
    ]

    optimizer = nlp.begin_training()

    start = datetime.now()
    print("\nSTART TRAINING")

    for iteration in range(train_iteration_limit):

        start_iteration = datetime.now()
        print("start iteration:", iteration, "at", start_iteration.strftime("%H:%M:%S"))

        i = 0
        for doc, gold in train_data:
            i += 1
            nlp.update([doc], [gold], sgd=optimizer)

            # TODO : remove unused pipes
            # TODO : feedback of current iteration

        end_iteration = datetime.now()
        print("end iteration:", iteration, end_iteration.strftime("%H:%M:%S"))
        print("duration iteration:", end_iteration - start_iteration, "\n")

    end = datetime.now()
    print("END TRAINING")
    print("DURATION TRAINING:", end - start)

    return nlp




lang = "de_core_news_sm"
nlp = spacy.load(lang)
textcat = nlp.create_pipe("textcat")
for cat in data_provider.choice_options:
    textcat.add_label(cat["text"])

nlp.add_pipe(textcat, last=True)

print("Loaded new spacy model:", lang)

train(nlp)

file_path = "./dummy_model"
nlp.to_disk(file_path)
print("persisted to path:", file_path)