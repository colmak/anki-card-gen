from google.cloud import translate_v2 as translate
import os

# Set the environment variable for the Google API credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\rvand\Downloads\anki-translation-442303-7b1c82eb3428.json"


# File paths
input_file = '1000-most-common-nepali-words.txt'
output_file = '1000-most-common-nepali-words-translated.txt'  

def translate_words(input_path, output_path):
    try:
        # Initialize the translation client
        translate_client = translate.Client()

        # Read Nepali words
        with open(input_path, 'r', encoding='utf-8') as infile:
            nepali_words = [line.strip() for line in infile.readlines()]

        translated_words = []
        for word in nepali_words:
            # Translate the word to English
            result = translate_client.translate(word, source_language='ne', target_language='en')
            translated_word = result['translatedText']
            translated_words.append(translated_word)

        # Write translated words to output file
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write('\n'.join(translated_words))
        print(f"Translated words saved to {output_path}")

    except Exception as e:
        print(f"Error during translation: {e}")

# Run translation
translate_words(input_file, output_file)
