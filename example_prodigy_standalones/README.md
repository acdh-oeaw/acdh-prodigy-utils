## Stand alone launchables

Prodigy recipes wrapped up in python modules so that they can be launched directly and configured with python (instead of having to pass configurations as shell parameters).

Note that these scripts should be executed within this folder, otherwise it's possible that the prodigy.json file from the root folder overrides the local settings. A prodigy.json file is only loaded when being present in the current working directory - to my understanding.

To run the standalones, a virtual environment should be built. For this follow the README in the root directory (or install the needed packages yourself).
