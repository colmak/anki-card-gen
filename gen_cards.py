import genanki
import requests
from pathlib import Path

# Pixabay API key (replace with your key if using Pixabay)
PIXABAY_API_KEY = "your_pixabay_api_key"

# Directory to save images
image_dir = Path("nepali_images")
image_dir.mkdir(exist_ok=True)

REQUESTS_PER_MINUTE = 100
DELAY_BETWEEN_REQUESTS = 60 / REQUESTS_PER_MINUTE

# Function to fetch an image from Pixabay
def fetch_image(word):
    try:
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={word}&lang=ne&image_type=photo&per_page=3"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['hits']:
            image_url = data['hits'][0]['largeImageURL']
            image_path = image_dir / f"{word}.jpg"
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            return str(image_path)
    except Exception as e:
        print(f"Image not found for {word}: {e}")
        return None

# Function to generate translations, sentences, and fetch image
def generate_translation_sentence_image(nepali_word):
    prompt = f"""You are a language expert. For the Nepali word "{nepali_word}", provide:
    1. Its meaning in English.
    2. A sample sentence in Nepali where the word is used, with the word **bolded**.
    3. The same sentence romanized, also with the word **bolded**.
    4. Translate the Nepali sentence into English, preserving the meaning."""
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        content = response.choices[0].text.strip().split('\n')
        english_meaning = content[0].split(':')[1].strip()
        nepali_sentence = content[1].split(':')[1].strip()
        romanized_sentence = content[2].split(':')[1].strip()
        english_sentence = content[3].split(':')[1].strip()
        image_path = fetch_image(english_meaning)
        return english_meaning, nepali_sentence, romanized_sentence, english_sentence, image_path
    except Exception as e:
        print(f"Error generating for {nepali_word}: {e}")
        return "N/A", "N/A", "N/A", "N/A", None

# Define the Anki model
model = genanki.Model(
    1607392319,
    'Nepali Words Model',
    fields=[
        {'name': 'Nepali'},
        {'name': 'Romanized'},
        {'name': 'English'},
        {'name': 'Sentence'},
        {'name': 'Romanized Sentence'},
        {'name': 'English Sentence'},
        {'name': 'Image'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Nepali}}<br><span style="color:gray; font-size:12px;">{{Romanized}}</span>',
            'afmt': '''{{FrontSide}}<hr id="answer">
            {{English}}<br>{{Sentence}}<br>
            <span style="font-style:italic; color:gray;">{{Romanized Sentence}}</span><br>
            <span style="font-style:italic;">{{English Sentence}}</span><br>
            {{#Image}}<img src="{{Image}}" alt="Image for {{Nepali}}"><br>{{/Image}}'''
        }
    ],
)

deck = genanki.Deck(
    2059400110,
    'Nepali 1k'
)

# Load the words from the text file
with open('1000-most-common-nepali-words.txt', 'r', encoding='utf-8') as file:
    words = file.readlines()

# Generate cards for each word
for word in words:
    nepali_word = word.strip()
    english, nepali_sentence, romanized_sentence, english_sentence, image_path = generate_translation_sentence_image(nepali_word)
    romanized_word = "romanized logic here"  # Replace or integrate Romanization for individual words
    fields = [nepali_word, romanized_word, english, nepali_sentence, romanized_sentence, english_sentence, image_path or '']
    note = genanki.Note(
        model=model,
        fields=fields
    )
    deck.add_note(note)

# Save the deck
output_file = 'nepali_vocabulary_with_images.apkg'
package = genanki.Package(deck)

# Include media (images)
if image_dir.exists():
    package.media_files = list(image_dir.glob("*.jpg"))

package.write_to_file(output_file)
print(f"Anki deck created with online images: {output_file}")