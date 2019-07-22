from setuptools import setup

setup(
    name='prodigy_utils',
    version='0.0.1',
    description="""A bunch of custom loaders for prodigy""",
    author="Peter Andorfer",
    author_email="peter.andorfer@oeaw.ac.at",
    license="MIT",
    entry_points={
        'prodigy_loaders': [
            'from_dsebaseapp = dsebaseapp:from_dsebaseapp',
            'from_transkribus = transkribus:yield_samples',
            'from_transkribus_regions = transkribus:yield_texts',
            'from_ske_docs = ske:yield_docs'
        ],
    },
    requirements=[
        'prodigy>=1.8.3'
    ]
)
