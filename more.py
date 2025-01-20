import os
from pathlib import Path
import genanki
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

base_audio_dir = Path(r"C:\anki_audio")
question_audio_dir = base_audio_dir / "questions2"
answer_audio_dir = base_audio_dir / "answers2"
question_audio_dir.mkdir(parents=True, exist_ok=True)
answer_audio_dir.mkdir(parents=True, exist_ok=True)

qa_data = [
    {
        "question_nep": "कति बज्यो?",
        "question_eng": "What time is it?",
        "answer_nep": "अहिले तीन बज्यो।",
        "answer_eng": "It's 3 o'clock now.",
        "transliteration": "Kati bajyo?\nAhile teen bajyo.",
    },
    {
        "question_nep": "मौसम कस्तो छ?",
        "question_eng": "How is the weather?",
        "answer_nep": "आज धेरै गर्मी छ।",
        "answer_eng": "It's very hot today.",
        "transliteration": "Mausam kasto chha?\nAaja dherai garmi chha.",
    },
    {
        "question_nep": "हामी जाने गरौँ?",
        "question_eng": "Shall we go? / Let's go?",
        "answer_nep": "हुन्छ, जाऔँ!",
        "answer_eng": "Sure, let's go!",
        "transliteration": "Haami jaane garaum?\nHunchha, jaaũ!",
    },
    {
        "question_nep": "तिमी कहाँ छौ?",
        "question_eng": "Where are you?",
        "answer_nep": "म घरमै छु।",
        "answer_eng": "I am at home.",
        "transliteration": "Timī kahã chhau?\nMa gharmai chhu.",
    },
    {
        "question_nep": "तिमी किन आउँदिनौ भने के हुन्छ?",
        "question_eng": "What happens if you do not come?",
        "answer_nep": "भोली थप गाह्रो हुन्छ।",
        "answer_eng": "It will be more difficult tomorrow.",
        "transliteration": "Timī kinā aaudinaū bhane ke hunchha?\nBholī thap gāhro hunchha.",
    },
    {
        "question_nep": "यो सजिलो छ कि गाह्रो?",
        "question_eng": "Is this easy or difficult?",
        "answer_nep": "यो सजिलो छ, तर कहिलेकाहीँ गाह्रो पनि हुन्छ।",
        "answer_eng": "It's easy, but sometimes it's also difficult.",
        "transliteration": "Yo sajilo chha ki gāhro?\nYo sajilo chha, tara kailekāhī gāhro pani hunchha.",
    },
    {
        "question_nep": "तिमी किन यहाँ थियौ?",
        "question_eng": "Why were you here (in the past)?",
        "answer_nep": "म केही कामका लागि यहाँ आएको थिएँ।",
        "answer_eng": "I had come here for some work.",
        "transliteration": "Timī kinā yahā thiyau?\nMa kehi kaamkā lāgi yahā āeko thiẽ.",
    },
    {
        "question_nep": "यो घर ठूलो छ?",
        "question_eng": "Is this house big?",
        "answer_nep": "हो, यो घर निकै ठूलो छ।",
        "answer_eng": "Yes, this house is very big.",
        "transliteration": "Yo ghar thulo chha?\nHo, yo ghar nikai thulo chha.",
    },
    {
        "question_nep": "हामी क्लासमा पढ्ने गरौँ?",
        "question_eng": "Shall we study in the class?",
        "answer_nep": "हो, हामी क्लासमा पढ्ने गरौँ।",
        "answer_eng": "Yes, let's study in the class.",
        "transliteration": "Haami klassmā paḍhne garaum?\nHo, haami klassmā paḍhne garaum.",
    },
    {
        "question_nep": "अचेल मौसम कस्तो छ?",
        "question_eng": "How is the weather these days?",
        "answer_nep": "अचेल मौसम चिसो छ।",
        "answer_eng": "These days, the weather is cold.",
        "transliteration": "Acel mausam kasto chha?\nAcel mausam ciso chha.",
    },
    {
        "question_nep": "तिमीले खाजा खायौ?",
        "question_eng": "Did you eat breakfast?",
        "answer_nep": "हो, मैले खाजा खाएको थिएँ।",
        "answer_eng": "Yes, I had eaten breakfast.",
        "transliteration": "Timīle khājā khāyau?\nHo, maile khājā khāeko thiẽ.",
    },
    {
        "question_nep": "तिमी मसँग भिज्न चाहन्छौ?",
        "question_eng": "Do you want to get wet with me? (e.g., during rain)",
        "answer_nep": "होइन, म भिज्न चाहन्न।",
        "answer_eng": "No, I don't want to get wet.",
        "transliteration": "Timī maśaṅga bhijna chahanchhau?\nHoin, ma bhijna chahanna.",
    },
    {
        "question_nep": "तिमीले गरेको काम राम्रो छ?",
        "question_eng": "Is the work you did good?",
        "answer_nep": "हो, मैले गरेको काम राम्रो थियो।",
        "answer_eng": "Yes, the work I did was good.",
        "transliteration": "Timīle gareko kām ramro chha?\nHo, maile gareko kām ramro thiyo.",
    },
    {
        "question_nep": "हामी खेल्न जाऔँ?",
        "question_eng": "Shall we go play?",
        "answer_nep": "हुन्छ, खेल्न जाऔँ।",
        "answer_eng": "Sure, let's go play.",
        "transliteration": "Haami kheln jāũ?\nHunchha, kheln jāũ.",
    },
    {
        "question_nep": "पनि यस्तो हुन्छ?",
        "question_eng": "Will it also be like this?",
        "answer_nep": "हो, भविष्यमा पनि यस्तो हुनेछ।",
        "answer_eng": "Yes, it will be like this in the future as well.",
        "transliteration": "Pani yasto hunchha?\nHo, bhavisyamā pani yasto hunechha.",
    },
]

def generate_audio(text, filename, directory):
    audio_path = directory / filename

    if audio_path.exists():
        return f"[sound:{audio_path.name}]"

    try:
        audio_content = eleven_client.text_to_speech.convert(
            voice_id="XrExE9yKIg1WjnnlVkGX",  
            output_format="mp3_44100_64",
            text=text,
            model_id="eleven_multilingual_v2",
        )

        if hasattr(audio_content, "__iter__") and not isinstance(audio_content, (bytes, bytearray)):
            audio_content = b"".join(audio_content)

        with open(audio_path, "wb") as f:
            f.write(audio_content)

        return f"[sound:{audio_path.name}]"
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")
        return ""

def create_deck(deck_id, deck_name, model, data, media_files, audio_dirs):
    deck = genanki.Deck(deck_id, deck_name)

    for idx, entry in enumerate(data):
        q_audio_file = f"question_{idx}.mp3"
        a_audio_file = f"answer_{idx}.mp3"
        
        question_audio = generate_audio(entry["question_nep"], q_audio_file, audio_dirs["question"])
        answer_audio = generate_audio(entry["answer_nep"], a_audio_file, audio_dirs["answer"])

        note = genanki.Note(
            model=model,
            fields=[
                entry["question_nep"],
                entry["transliteration"].split("\n")[0],
                entry["question_eng"],
                entry["answer_nep"],
                entry["transliteration"].split("\n")[1],
                entry["answer_eng"],
                question_audio,
                answer_audio,
            ],
        )
        deck.add_note(note)

        if question_audio:
            media_files.append(str(audio_dirs["question"] / q_audio_file))
        if answer_audio:
            media_files.append(str(audio_dirs["answer"] / a_audio_file))

    return deck

model = genanki.Model(
    1607392319,
    "Nepali Q&A Model",
    fields=[
        {"name": "QuestionNepali"},
        {"name": "TransliterationQ"},
        {"name": "QuestionEnglish"},
        {"name": "AnswerNepali"},
        {"name": "TransliterationAns"},
        {"name": "AnswerEnglish"},
        {"name": "QuestionAudio"},
        {"name": "AnswerAudio"},
    ],
    templates=[
        {
            "name": "Q&A Format",
            "qfmt": "{{QuestionNepali}}<br>{{TransliterationQ}}<br>{{QuestionEnglish}}<br><br>{{AnswerNepali}}<br>{{TransliterationAns}}<br>{{AnswerEnglish}}<br>{{AnswerAudio}} {{QuestionAudio}}",
            "afmt": "{{FrontSide}}<hr id=\"answer\">{{AnswerNepali}}<br>{{TransliterationAns}}<br>{{AnswerEnglish}}<br>{{AnswerAudio}}",
        },
    ],
    css=".card { font-size: 5vw; }",
)

media_files = []

deck = create_deck(
    deck_id=2059400112,
    deck_name="Nepali Time, Weather, and Verbs",
    model=model,
    data=qa_data,
    media_files=media_files,
    audio_dirs={"question": question_audio_dir, "answer": answer_audio_dir},
)

package = genanki.Package(deck)
package.media_files = media_files
output_file = f"Nepali_Practice_Sentences.apkg"
package.write_to_file(output_file)
print(f"Deck created: {output_file}")