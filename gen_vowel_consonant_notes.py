import genanki
import os
from pathlib import Path
import re
import base64
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup directories for media files
audio_dir = Path(r"C:\anki_audio\scripts")
audio_dir.mkdir(exist_ok=True)

# Model for Devanagari deck
model = genanki.Model(
    1607392320,
    'Devanagari Model',
    fields=[
        {'name': 'Devanagari'},
        {'name': 'Romanized'},
        {'name': 'Approximate Sound'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Devanagari}}<br>{{Approximate Sound}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Romanized}}<br>{{#Audio}}<audio controls><source src="{{Audio}}" type="audio/mpeg"></audio>{{/Audio}}',
        }
    ],
    css="""
    .card {
        font-family: Arial, sans-serif;
        text-align: center;
        font-size: 20px;
        color: black;
        background-color: white;
    }
    """
)

# Vowel data
vowels = [
    ("अ", "a", "shut", "a.mp3"),
    ("आ", "ā", "father", "aa.mp3"),
    ("इ", "i", "free", "i.mp3"),
    ("ई", "ī", "free", "ii.mp3"),
    ("उ", "u", "boot", "u.mp3"),
    ("ऊ", "ū", "boot", "uu.mp3"),
    ("ए", "e", "may", "e.mp3"),
    ("ऐ", "ai", "a+i (like night)", "ai.mp3"),
    ("ओ", "o", "oh", "o.mp3"),
    ("औ", "au", "a+u (like yowl)", "au.mp3"),
]

# Consonant data
consonants = [
    ("क", "k(a)", "alcohol", "ka.mp3"),
    ("ख", "kh(a)", "Khalifa", "kha.mp3"),
    ("ग", "g(a)", "gun", "ga.mp3"),
    ("घ", "gh(a)", "Ghana", "gha.mp3"),
    ("ङ", "ṅ(a)", "sing", "nga.mp3"),
    ("च", "c(a)", "cats", "ca.mp3"),
    ("छ", "ch(a)", "cats (with more aspiration)", "cha.mp3"),
    ("ज", "j(a)", "jug", "ja.mp3"),
    ("झ", "jh(a)", "jug (with more aspiration)", "jha.mp3"),
    ("ञ", "ñ(a)", "canyon", "nya.mp3"),
    ("ट", "ṭ(a)", "master", "ta.mp3"),
    ("ठ", "ṭh(a)", "Thomas", "tha.mp3"),
    ("ड", "ḍ(a)", "dog", "da.mp3"),
    ("ढ", "ḍh(a)", "dog (with more aspiration)", "dha.mp3"),
    ("ण", "ṇ(a)", "panda", "na.mp3"),
    ("त", "t(a)", "like the Spanish 't'", "ta2.mp3"),
    ("थ", "th(a)", "thunder", "tha2.mp3"),
    ("द", "d(a)", "the (rhymes with uh)", "da2.mp3"),
    ("ध", "dh(a)", "the (with more aspiration)", "dha2.mp3"),
    ("न", "n(a)", "nun", "na2.mp3"),
    ("प", "p(a)", "spun", "pa.mp3"),
    ("फ", "ph(a)", "fun", "pha.mp3"),
    ("ब", "b(a)", "bun", "ba.mp3"),
    ("भ", "bh(a)", "vault", "bha.mp3"),
    ("म", "m(a)", "mall", "ma.mp3"),
    ("य", "y(a)", "yawn", "ya.mp3"),
    ("र", "r(a)", "run", "ra.mp3"),
    ("ल", "l(a)", "lawn", "la.mp3"),
    ("व", "w(a)/v(a)", "want", "va.mp3"),
    ("श", "ś(a)", "shawl", "sha.mp3"),
    ("ष", "ṣ(a)", "shawl", "sha2.mp3"),
    ("स", "s(a)", "sun", "sa.mp3"),
    ("ह", "h(a)", "hum", "ha.mp3"),
]

# Vowel diacritics data
diacritics = [
    ("प", "a", "spun", "pa.mp3"),
    ("पा", "ā", "father", "paa.mp3"),
    ("पि", "i", "free", "pi.mp3"),
    ("पी", "ī", "free", "pii.mp3"),
    ("पु", "u", "boot", "pu.mp3"),
    ("पू", "ū", "boot", "puu.mp3"),
    ("पे", "e", "may", "pe.mp3"),
    ("पै", "ai", "a+i (like night)", "pai.mp3"),
    ("पो", "o", "oh", "po.mp3"),
    ("पौ", "au", "a+u (like yowl)", "pau.mp3"),
]

# Create decks
vowel_deck = genanki.Deck(2059400120, 'Devanagari Vowels')
consonant_deck = genanki.Deck(2059400130, 'Devanagari Consonants')
diacritics_deck = genanki.Deck(2059400140, 'Devanagari Vowel Diacritics')

media_files = []

def gen_audio(text, file_name):
    try:
        audio_file_path = audio_dir / file_name

        if audio_file_path.exists() and audio_file_path.stat().st_size > 0:
            return file_name

        cleaned_text = re.sub(r'<.*?>', '', text)

        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "mp3"},
            messages=[
                {
                    "role": "user",
                    "content": "Say this: " + cleaned_text
                }
            ]
        )

        mp3_bytes = base64.b64decode(completion.choices[0].message.audio.data)
        with open(audio_file_path, "wb") as f:
            f.write(mp3_bytes)

        return file_name
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")
        return None

def add_notes_to_deck(deck, data):
    for devanagari, romanized, approx_sound, audio in data:
        audio = gen_audio(devanagari, audio)  # Generate audio dynamically
        note = genanki.Note(
            model=model,
            fields=[devanagari, romanized, approx_sound, f"[sound:{audio}]"],
        )
        deck.add_note(note)
        if audio:
            media_files.append(str(audio_dir / audio))

# Add notes to decks
add_notes_to_deck(vowel_deck, vowels)
add_notes_to_deck(consonant_deck, consonants)
add_notes_to_deck(diacritics_deck, diacritics)

# Save the decks to .apkg files
vowel_package = genanki.Package(vowel_deck)
vowel_package.media_files = media_files
vowel_package.write_to_file('Devanagari_Vowels.apkg')

consonant_package = genanki.Package(consonant_deck)
consonant_package.media_files = media_files
consonant_package.write_to_file('Devanagari_Consonants.apkg')

diacritics_package = genanki.Package(diacritics_deck)
diacritics_package.media_files = media_files
diacritics_package.write_to_file('Devanagari_Vowel_Diacritics.apkg')

print("Anki decks created: Devanagari_Vowels.apkg, Devanagari_Consonants.apkg, Devanagari_Vowel_Diacritics.apkg")
