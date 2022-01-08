import genanki
import boto3
from jamdict import Jamdict

# TODO: Make use of this to display other writing systems.
import pykakasi

# TODO: Remove if default is desired.
boto3.setup_default_session(profile_name="personal")

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

    sample_fname = f"{word}.mp3"

    with open(sample_fname, "wb") as f:
        f.write(response["AudioStream"].read())

    note = genanki.Note(
        model=model, fields=[japanese, english, f"[sound:{sample_fname}]"]
    )
    deck.add_note(note)

    return sample_fname


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
            "qfmt": "<center><h1>{{Question}}</h1></center>",
            "afmt": """
            {{FrontSide}}
            <hr id="answer">
            <center><h1>{{Answer}}</h1></center>
            <br />
            <center>{{MyMedia}}</center>
            """,
        },
    ],
)

deck = genanki.Deck(2059400110, "Automatic Japanese Deck Test")

media_files = [add_card(deck, model, "assistant")]

pkg = genanki.Package(deck)
pkg.media_files = media_files
pkg.write_to_file("output.apkg")
