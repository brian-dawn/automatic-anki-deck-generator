import os
import genanki
import boto3

# TODO: Make use of this to display other writing systems.
import pykakasi

aws_profile_override = os.environ.get("AWS_PROFILE")
if aws_profile_override is not None:
    print(f"Using AWS_PROFILE={aws_profile_override}")
    boto3.setup_default_session(profile_name=aws_profile_override)
else:
    print("Using default AWS_PROFILE")

polly_client = boto3.Session(region_name="us-west-2").client("polly")

sound_folder = "mp3s"


def add_card_japanese_to_english(deck, model, english, japanese):

    if not os.path.exists(sound_folder):
        os.mkdir(sound_folder)

    sample_fname = f"{english}.mp3"
    sample_path = f"{sound_folder}/{english}.mp3"

    if os.path.exists(sample_path):
        print(f"{japanese} => {english} using cached")
    else:
        # Run the text through Polly to get the audio.

        print(f"{japanese} => {english}")

        # Also Mizuki but doesn't support Neural voice I think.
        response = polly_client.synthesize_speech(
            VoiceId="Takumi", OutputFormat="mp3", Text=japanese, Engine="neural"
        )

        with open(sample_path, "wb") as f:
            f.write(response["AudioStream"].read())

    note = genanki.Note(
        model=model,
        fields=[japanese, english, f"[sound:{sample_fname}]"],
    )
    deck.add_note(note)

    return sample_path


japanese_to_english_model = genanki.Model(
    1607392319,
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "MyMedia"},
    ],
    css="""
    .card {
        font-family: arial;
        font-size: 3em;
    }
    """,
    templates=[
        {
            "name": "Card 1",
            "qfmt": "<center><h1>{{Question}}</h1></center>",
            "afmt": """
            {{FrontSide}}
            <hr id="answer">
            <center>{{Answer}}</center>
            <br />
            <center>{{MyMedia}}</center>
            """,
        },
    ],
)

deck = genanki.Deck(2059400110, "Automatic Japanese Deck Test")

english_to_japanese_katakana = """
assistant : アシスタント 
Argentina : アルゼンチン 
Brazil : ブラジル 
"""


def split_question_answer(line):
    a, b = line.split(":")
    return (a.strip(), b.strip())


media_files = []
for line in english_to_japanese_katakana.strip().splitlines():
    english, japanese = split_question_answer(line)

    media_file = add_card_japanese_to_english(
        deck, japanese_to_english_model, english, japanese
    )
    media_files.append(media_file)


pkg = genanki.Package(deck)
pkg.media_files = media_files
pkg.write_to_file("output.apkg")
