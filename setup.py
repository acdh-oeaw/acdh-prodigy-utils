from setuptools import setup

setup(
    name='prodigy_utils',
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
