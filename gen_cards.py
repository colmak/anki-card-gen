import genanki
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI
from pydantic import BaseModel
from itertools import islice
import re
import re
import base64
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

image_dir = Path(r"C:\anki_images")
audio_dir = Path(r"C:\anki_audio")
image_dir.mkdir(exist_ok=True)
audio_dir.mkdir(exist_ok=True)

notes_file = Path(r"processed_notes.json")
if not notes_file.exists():
    notes_file.write_text("[]")  

def load_translations():
    with open('1000-most-common-nepali-words.txt', 'r', encoding='utf-8') as nepali_file, \
         open('1000-most-common-nepali-words-translated.txt', 'r', encoding='utf-8') as english_file:
        nepali_words = [line.strip() for line in nepali_file.readlines()]
        english_words = [line.strip() for line in english_file.readlines()]

    if len(nepali_words) != len(english_words):
        raise ValueError("Mismatch between the number of Nepali and English words.")

    return dict(zip(nepali_words, english_words))

translations = load_translations()

def fetch_image(english_word):
    try:
        if not english_word:
            print(f"No English translation available.")
            return None

        image_file_name = f"{english_word.replace(' ', '_')}.jpg"
        image_path = image_dir / image_file_name

        if image_path.exists():
            return image_file_name 

        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={english_word}&image_type=photo&per_page=3"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['hits']:
            img_data = requests.get(data['hits'][0]['largeImageURL']).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            return image_file_name
        else:
            return None
    except Exception as e:
        print(f"Error fetching image for '{english_word}': {e}")
        return None

def fetch_audio(text, file_name):
    try:
        audio_file_path = audio_dir / file_name

        if audio_file_path.exists():
            return file_name

        cleaned_text = re.sub(r'<.*?>', '', text)

        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "mp3"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Nepali speaker. Your task is to pronounce exactly and clearly the text provided, "
                        "without adding or modifying anything. Do not include greetings, explanations, or additional sounds."
                    )
                },
                {
                    "role": "user",
                    "content": f"{cleaned_text}"
                },
            ]
        )

        mp3_bytes = base64.b64decode(completion.choices[0].message.audio.data)
        with open(audio_file_path, "wb") as f:
            f.write(mp3_bytes)

        return file_name
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")
        return None

class TranslationResponse(BaseModel):
    english_meaning: str
    romanized_word: str
    nepali_sentence: str
    romanized_sentence: str
    english_sentence: str

def generate_translation_sentence_image_audio(nepali_word):
    """Generate translations, sentences, image, and audio for a Nepali word."""
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are a language expert. Extract structured information about the Nepali word provided."
                },
                {
                    "role": "user",
                    "content": (
                        f"For the Nepali word '{nepali_word}', provide:\n"
                        "1. Its meaning in English.\n"
                        "2. The romanized version of the Nepali word.\n"
                        "3. A simple sample sentence in Nepali where the word is used, "
                        "with the word <strong></strong>.\n"
                        "4. The same sentence romanized, also with the word <strong></strong>.\n"
                        "5. Translate the Nepali sentence into English, preserving the meaning."
                    )
                },
            ],
            response_format=TranslationResponse
        )
        parsed = response.choices[0].message.parsed

        image_path = fetch_image(parsed.english_meaning)

        word_audio = fetch_audio(nepali_word, f"{nepali_word}_word.mp3")

        sentence_audio = fetch_audio(parsed.nepali_sentence, f"{nepali_word}_sentence.mp3")

        return (
            parsed.english_meaning,
            parsed.romanized_word,
            parsed.nepali_sentence,
            parsed.romanized_sentence,
            parsed.english_sentence,
            image_path,
            word_audio,
            sentence_audio,
        )
    except Exception as e:
        print(f"Error generating for {nepali_word}: {e}")
        return "N/A", "N/A", "N/A", "N/A", "N/A", None, None, None

def load_existing_notes():
    if notes_file.exists():
        with open(notes_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_notes(notes):
    with open(notes_file, 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

def note_exists(existing_notes, nepali_word):
    return any(note['nepali'] == nepali_word for note in existing_notes)

existing_notes = load_existing_notes()
notes = existing_notes.copy()

index = len(existing_notes) + 1

for nepali_word in translations.keys(): 
    if note_exists(existing_notes, nepali_word):
        continue 

    english_word = translations[nepali_word]
    english, romanized_word, nepali_sentence, romanized_sentence, english_sentence, image_file_name, word_audio, sentence_audio = generate_translation_sentence_image_audio(nepali_word)

    new_note = {
        "index": index,
        "nepali": nepali_word,
        "romanized": romanized_word,
        "english": english,
        "sentence": nepali_sentence,
        "romanized_sentence": romanized_sentence,
        "english_sentence": english_sentence,
        "image": image_file_name or '',
        "word_audio": word_audio or '',
        "sentence_audio": sentence_audio or ''
    }
    notes.append(new_note)
    index += 1

save_notes(notes)

model = genanki.Model(
    1607392319,
    'Nepali Words Model',
    fields=[
        {'name': 'Index'},
        {'name': 'Nepali'},
        {'name': 'Romanized'},
        {'name': 'English'},
        {'name': 'Sentence'},
        {'name': 'Romanized Sentence'},
        {'name': 'English Sentence'},
        {'name': 'Image'},
        {'name': 'Word Audio'},
        {'name': 'Sentence Audio'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
<div id="nepali-word" class="nepali-text">{{Nepali}}</div>
<div id="romanized-word" class="hidden">{{Romanized}}</div>
<hr>
<div id="sentence" class="nepali-text">{{Sentence}}</div>
<div id="romanized-sentence" class="hidden">{{Romanized Sentence}}</div>
<script>
  function toggleVisibility(id) {
    const element = document.getElementById(id);
    element.classList.toggle('hidden');
  }

  document.getElementById('nepali-word').addEventListener('click', () => toggleVisibility('romanized-word'));
  document.getElementById('sentence').addEventListener('click', () => toggleVisibility('romanized-sentence'));
</script>
''',
            'afmt': '''
<div class="nepali-text">{{Nepali}}</div>
<div class="romanized">{{Romanized}}</div>
<div class="english">{{English}}</div>
<hr>
<div class="nepali-text">{{Sentence}}</div>
<div class="romanized">{{Romanized Sentence}}</div>
<div class="english">{{English Sentence}}</div>
<br>
{{#Image}}
<div class="image">
  <img src="{{Image}}">
</div>
{{/Image}}
<div></div>
{{#Word Audio}}
<audio controls>
  <source src="{{Word Audio}}" type="audio/mpeg">
</audio>
{{/Word Audio}}
'''
        }
    ],
    css='''
.hidden {
  display: none;
}

.nepali-text {
  font-size: 24px;
  cursor: pointer;
}

.romanized {
  font-size: 18px;
  color: #55dd55;
}
'''
)

deck = genanki.Deck(2059400110, 'Nepali 1k')
media_files = []

for note in notes:
    fields = [
        str(note["index"]), note["nepali"], note["romanized"], note["english"],
        note["sentence"], note["romanized_sentence"], note["english_sentence"],
        note["image"], f"[sound:{note['word_audio']}]", f"[sound:{note['sentence_audio']}]"
    ]
    anki_note = genanki.Note(
        model=model,
        fields=fields
    )
    deck.add_note(anki_note)

    if note["image"]:
        media_files.append(str(image_dir / note["image"]))
    if note["word_audio"]:
        media_files.append(str(audio_dir / note["word_audio"]))
    if note["sentence_audio"]:
        media_files.append(str(audio_dir / note["sentence_audio"]))

package = genanki.Package(deck)
package.media_files = media_files
output_file = 'Nepali-1K.apkg'
package.write_to_file(output_file)

print(f"Anki deck created with online images and audio: {output_file}")
