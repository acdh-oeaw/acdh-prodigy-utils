from setuptools import setup

setup(
    name='prodigy_utils',
    entry_points={
        'prodigy_loaders': [
            'from_dsebaseapp = dsebaseapp:from_dsebaseapp',
            'from_transkribus = transkribus:yield_samples',
        ],
    },
    requirements=[
        'prodigy>=1.8.3'
    ]
)
