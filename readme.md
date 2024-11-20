# Anki Card Generator

This project is a script for generating **Anki flashcards** for Nepali words with the following format:

## Card Format
### Front:
- **Word**: The word in Nepali script.
- **Romanized**: The pronunciation of the word (appears on hover).

### Back:
- **English**: The English translation of the word.
- **Sentence Example**: A sample sentence in Nepali where the word is used.
- **Sentence Romanized**: The sample sentence written in Romanized script.
- **Sentence Translated**: The sample sentence translated into English.
- **Image**: A relevant image (if available) that represents the word.

---

## How It Works

The script:
1. **Loads Nepali words** from a provided text file where each line contains one word.
2. **Generates translations and example sentences** using AI.
3. **Fetches relevant images** from Pixabay's API (or skips if none are found).
4. **Creates an Anki deck** with the specified card format.

---

## Prerequisites

### Install Required Libraries:
```bash
pip install requests genanki openai
```

### Obtain API Keys:
1. **OpenAI API Key**:
   - Used for generating translations, Romanizations, and sentences.
   - [Sign up here](https://platform.openai.com/signup/).
   
2. **Pixabay API Key** (optional):
   - Used for fetching images related to the words.
   - [Sign up here](https://pixabay.com/).

---

## Usage

1. Place your Nepali words in a text file (e.g., `1000-most-common-nepali-words.txt`), with **one word per line**.
2. Update the script:
   - Replace `your_openai_api_key` and `your_pixabay_api_key` with your respective API keys.
3. Run the script:
   ```bash
   python anki_card_generator.py
   ```
4. The script will generate a `.apkg` file (e.g., `nepali_vocabulary_with_images.apkg`).
5. Import the `.apkg` file into **Anki** to start studying!

---

## Features

- **AI-Generated Content**:
  - Automatically generates English translations, Romanizations, and example sentences.
- **Images**:
  - Fetches relevant images to visually represent each word.
  - Skips image fetching gracefully if no suitable match is found.
- **Rate Limiting**:
  - Ensures compliance with API rate limits for Pixabay (or other image providers).

---

## Example Card

### Front:
**Word**: रूप  
**Romanized**: *roop* (appears on hover)

### Back:
- **English**: Form  
- **Sentence Example**: यो शब्दको **रूप**ले महत्त्वपूर्ण छ।  
- **Sentence Romanized**: Yo śabdako **roop**le mahatvapūrṇa cha.  
- **Sentence Translated**: The form of this word is significant.  
- **Image**: *(Relevant illustration of "form")*  

---

## Known Limitations

1. **API Dependency**:
   - Requires access to OpenAI and Pixabay APIs for generation and image retrieval.
2. **Romanization**:
   - Needs enhancement for more accurate pronunciation logic.
3. **Fallbacks**:
   - Cards may not include images if no match is found.

---

## Contributing

Feel free to contribute by:
- Enhancing Romanization logic.
- Adding support for other image APIs.
- Improving translations and example sentence generation.

---

Happy studying! 🎓
