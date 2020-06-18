from prodigy.components.db import connect

db = connect()
all_dataset_names = db.datasets
examples = db.get_dataset("prodigy_standalone_dataset")
print()