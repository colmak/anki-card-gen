import os
import json
from pathlib import Path
import requests
import genanki
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
NARAKEET_API_KEY = os.getenv('NARAKEET_API_KEY')

# Directories
image_dir = Path(r"C:\anki_images")
audio_dir = Path(r"C:\anki_audio")
image_dir.mkdir(exist_ok=True)
audio_dir.mkdir(exist_ok=True)
notes_file = Path(r"processed_notes.json")

# Load notes
if not notes_file.exists():
    raise FileNotFoundError("processed_notes.json not found.")

with open(notes_file, 'r', encoding='utf-8') as file:
    notes = json.load(file)

# Function to fetch audio using Narakeet API
def fetch_audio(text, file_name):
    try:
        audio_file_path = audio_dir / file_name

        if audio_file_path.exists():
            return file_name  # Return only the short filename

        url = f"https://api.narakeet.com/text-to-speech/m4a?voice=lhakpa"
        headers = {
            'Accept': 'application/octet-stream',
            'Content-Type': 'text/plain',
            'x-api-key': NARAKEET_API_KEY,
        }
        response = requests.post(url, headers=headers, data=text.encode('utf-8'))

        if response.status_code == 200:
            with open(audio_file_path, 'wb') as f:
                f.write(response.content)
            return file_name  # Return only the short filename
        else:
            print(f"Error fetching audio: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")
        return None

# Function to fetch image using Pixabay API
def fetch_image(english_word):
    try:
        if not english_word:
            return None

        image_file_name = f"{english_word.replace(' ', '_')}.jpg"
        image_path = image_dir / image_file_name

        if image_path.exists():
            return image_file_name  # Return only the short filename

        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={english_word}&image_type=photo&per_page=3"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['hits']:
            img_data = requests.get(data['hits'][0]['largeImageURL']).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            return image_file_name  # Return only the short filename
        else:
            return None
    except Exception as e:
        print(f"Error fetching image for '{english_word}': {e}")
        return None

notes = notes

for note in notes:
    nepali_word = note['nepali']
    nepali_sentence = note['sentence']
    english_word = note['english']

    # Fetch audio and image
    note['word_audio'] = fetch_audio(nepali_word, f"{nepali_word}_word.m4a") or note.get('word_audio', '')
    note['sentence_audio'] = fetch_audio(nepali_sentence, f"{nepali_word}_sentence.m4a") or note.get('sentence_audio', '')
    note['image'] = fetch_image(english_word) or note.get('image', '')

# Create Anki Deck
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
<div>{{Nepali}}</div>
<div>{{Romanized}}</div>
<hr>
<div>{{Sentence}}</div>
{{#Image}}
<img src="{{Image}}" alt="Image">
{{/Image}}
<audio controls>
  <source src="{{Word Audio}}" type="audio/mpeg">
</audio>
<audio controls>
  <source src="{{Sentence Audio}}" type="audio/mpeg">
</audio>
''',
            'afmt': '''
<div>{{English}}</div>
<div>{{Romanized Sentence}}</div>
{{#Image}}
<img src="{{Image}}" alt="Image">
{{/Image}}
<audio controls>
  <source src="{{Word Audio}}" type="audio/mpeg">
</audio>
<audio controls>
  <source src="{{Sentence Audio}}" type="audio/mpeg">
</audio>
''',
        }
    ],
)

deck = genanki.Deck(2059400110, 'Nepali 1000')
media_files = []

for note in notes:  
    fields = [
        str(note["index"]),
        note["nepali"],
        note["romanized"],
        note["english"],
        note["sentence"],
        note["romanized_sentence"],
        note["english_sentence"],
        note["image"] if note["image"] else '',
        f"[sound:{note['word_audio']}]" if note['word_audio'] else '',
        f"[sound:{note['sentence_audio']}]" if note['sentence_audio'] else ''
    ]
    anki_note = genanki.Note(
        model=model,
        fields=fields
    )
    print("Note Created: ", note)
    deck.add_note(anki_note)

    if note["image"]:
        media_files.append(str(image_dir / note["image"]))
    if note["word_audio"]:
        media_files.append(str(audio_dir / note["word_audio"]))
    if note["sentence_audio"]:
        media_files.append(str(audio_dir / note["sentence_audio"]))

package = genanki.Package(deck)
package.media_files = media_files
output_file = 'Nepali-1000.apkg'
package.write_to_file(output_file)

print(f"Deck Created {output_file}")
