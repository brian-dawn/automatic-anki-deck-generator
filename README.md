# Anki deck generator


Automatically generate anki decks using Amazon Polly to supply pronunciations.


## Requirements

* Python + Poetry
* An AWS account configured on your machine

Once Poetry is installed:

    poetry install
    poetry shell
    python main.py

This will create an apkg file that you can then load into Anki. If you have multiple AWS profiles you can choose one by setting the 
`AWS_PROFILE` environment variable.

    AWS_PROFILE=personal python main.py

## Side goals

I want to try studying by going from English => Target Language


