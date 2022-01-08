import genanki
import boto3
from jamdict import Jamdict


polly_client = boto3.Session(region_name="us-west-2").client("polly")

jam = Jamdict()


def add_card(deck, model, word):

    # Assume latest is most accurate.
    found = jam.lookup(word).entries[0]

    japanese, english = found.text().split(" : ")

    print(f"{japanese} => {english}")
    # Also Mizuki but doesn't support Neural voice I think.
    response = polly_client.synthesize_speech(
        VoiceId="Takumi", OutputFormat="mp3", Text=japanese, Engine="neural"
    )

    with open(f"{english}.mp3", "wb") as f:
        f.write(response["AudioStream"].read())

    note = genanki.Note(model=model, fields=[japanese, english])
    deck.add_note(note)


def deck_from_word_list():
    pass


model = genanki.Model(
    1607392319,
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "MyMedia"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}{{MyMedia}}',
        },
    ],
)

deck = genanki.Deck(2059400110, "Example words")

add_card(deck, model, "assistant")

pkg = genanki.Package(deck)
# pkg.media_files = ... TODO
pkg.write_to_file("output.apkg")
