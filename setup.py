from setuptools import setup

setup(
    name='prodigy_utils',
    version='0.0.2',
    description="""A bunch of custom loaders for prodigy""",
    author="Peter Andorfer",
    author_email="peter.andorfer@oeaw.ac.at",
    license="MIT",
    entry_points={
        'prodigy_loaders': [
            'from_dsebaseapp = dsebaseapp:yield_samples',
            'from_transkribus = pr_transkribus:yield_samples',
            'from_transkribus_regions = pr_transkribus:yield_texts',
            'from_ske_docs = ske:yield_samples',
            'from_drf = drf:yield_samples'
        ],
    }
)
