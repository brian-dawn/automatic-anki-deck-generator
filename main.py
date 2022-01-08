import genanki
import boto3
from jamdict import Jamdict


jam = Jamdict()


def add_card(deck, model, word):

    # Assume latest is most accurate.
    found = jam.lookup(word).entries[0]

    japanese, english = found.text().split(" : ")


    print(f"{japanese} => {english}")

    note = genanki.Note(
            model=model,
            fields=[japanese, english]
            )
    deck.add_note(note)


def deck_from_word_list():
    pass

model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

deck = genanki.Deck( 2059400110, "Example words")

add_card(deck, model, "assistant")

genanki.Package(deck).write_to_file('output.apkg')

