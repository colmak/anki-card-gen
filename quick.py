import os 
from pathlib import Path 
import genanki 
from dotenv import load_dotenv 
from elevenlabs import ElevenLabs 

load_dotenv() 
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY') 

eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) 

base_audio_dir = Path(r"C:\anki_audio") 
question_audio_dir = base_audio_dir / "questions" 
answer_audio_dir = base_audio_dir / "answers" 
question_audio_dir.mkdir(parents=True, exist_ok=True) 
answer_audio_dir.mkdir(parents=True, exist_ok=True) 

qa_data = [ 
    { 
        "question_nep": "तपाईंको नाम के हो?", 
        "question_eng": "What is your name?", 
        "transliteration_q": "Tapaaiko naam ke ho?", 
        "answer_nep": "मेरो नाम रोल्यान्ड भान डुइन हो।", 
        "answer_eng": "My name is Roland Van Duine.", 
        "transliteration_ans": "Mero naam Roland Vhaan Duin ho.", 
    }, 
    { 
        "question_nep": "तपाईं कहाँबाट हुनुहुन्छ?", 
        "question_eng": "Where are you from?", 
        "transliteration_q": "Tapaaĩ kahãbãt hunuhunchha?", 
        "answer_nep": "म अमेरिका बाट आएको हुँ।", 
        "answer_eng": "I am from America.", 
        "transliteration_ans": "Ma Amerika baata aayeko hu.", 
    }, 
    { 
        "question_nep": "तपाईंको उमेर कति हो?", 
        "question_eng": "How old are you?", 
        "transliteration_q": "Tapaaiko umar kati ho?", 
        "answer_nep": "मेरो उमेर एक्काइस वर्ष हो।", 
        "answer_eng": "I am 21 years old.", 
        "transliteration_ans": "Mero umar ekkais barsha ho.", 
    }, 
    { 
        "question_nep": "तपाईंले कुन भाषाहरू बोल्नुहुन्छ?", 
        "question_eng": "What languages do you speak?", 
        "transliteration_q": "Tapaaile kun bhaashaa bolnuhunchha?", 
        "answer_nep": "म अङ्ग्रेजी, अलि स्पेनिश, र अलि नेपाली बोल्छु।", 
        "answer_eng": "I speak English, some Spanish, and some Nepali.", 
        "transliteration_ans": "Ma Angrezi, ali Spanish, ra ali Nepali bolchhu.", 
    }, 
    { 
        "question_nep": "तपाईंको काम के हो?", 
        "question_eng": "What is your occupation or job?", 
        "transliteration_q": "Tapaaiko kaam ke ho?", 
        "answer_nep": "म सफ्टवेयर इन्जिनियरको रूपमा काम गर्छु।", 
        "answer_eng": "I work as a software engineer.", 
        "transliteration_ans": "Ma software engineerko roopmaa kaam garchhu.", 
    }, 
    { 
        "question_nep": "तपाईंका शौखहरू के के हुन्?", 
        "question_eng": "What are your hobbies or interests?", 
        "transliteration_q": "Tapaaikaa shaukh ke ke hun?", 
        "answer_nep": "मलाई दौडन, पढ्न, रक क्लाइम्बिंग गर्न, र केहि बनाउन मनपर्छ।", 
        "answer_eng": "I like to run, read, rock climb, and make things.", 
        "transliteration_ans": "Malai daudan, padhna, rock climbing garna, ra kehi banana manparchha.", 
    }, 
    { 
        "question_nep": "तपाईंलाई दाजुभाइ वा दिदीबहिनी छन्?", 
        "question_eng": "Do you have any siblings?", 
        "transliteration_q": "Tapaaĩlai daajubhaai wa didibahini chhan?", 
        "answer_nep": "हो, मेरो ठूला दाजु र ठूला दिदी छन्।", 
        "answer_eng": "Yes, I have an older brother and an older sister.", 
        "transliteration_ans": "Ho, mero thula daaju ra thula didi chhan.", 
    }, 
    { 
        "question_nep": "तपाईंलाई मनपर्ने खाना के हो?", 
        "question_eng": "What is your favorite food?", 
        "transliteration_q": "Tapaaĩlai manparne khaanaa ke ho?", 
        "answer_nep": "मलाई स्वीडिश मिटबल्स मनपर्छ।", 
        "answer_eng": "My favorite food is Swedish Meatballs.", 
        "transliteration_ans": "Malai Swedish Meatballs manparchha.", 
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
                entry["answer_nep"], 
                entry.get("transliteration_q", ""), 
                entry["question_eng"], 
                entry["answer_eng"], 
                entry.get("transliteration_ans", ""), 
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
    "Nepali Q&A Model with Transliteration", 
    fields=[ 
        {"name": "QuestionNepali"}, 
        {"name": "AnswerNepali"}, 
        {"name": "TransliterationQ"}, 
        {"name": "QuestionEnglish"}, 
        {"name": "AnswerEnglish"}, 
        {"name": "TransliterationAns"}, 
        {"name": "QuestionAudio"}, 
        {"name": "AnswerAudio"}, 
    ], 
    templates=[ 
        { 
            "name": "Question and Transliteration", 
            "qfmt": "{{QuestionNepali}}<br>{{TransliterationQ}}<br>{{QuestionAudio}}", 
            "afmt": "{{QuestionEnglish}}<br>{{AnswerNepali}}<br>{{TransliterationAns}}<br>{{AnswerEnglish}}<br>{{AnswerAudio}}", 
        }, 
        { 
            "name": "Q&A Format", 
            "qfmt": "{{QuestionNepali}}<br>{{QuestionAudio}}", 
            "afmt": "{{AnswerNepali}}<br>{{TransliterationAns}}<br>{{AnswerAudio}}", 
        }, 
    ], 
) 

media_files = [] 

decks = [ 
    create_deck( 
        deck_id=2059400111, 
        deck_name="Nepali Questions and Translations with Transliteration", 
        model=model, 
        data=qa_data, 
        media_files=media_files, 
        audio_dirs={"question": question_audio_dir, "answer": answer_audio_dir}, 
    ) 
] 

for deck in decks: 
    package = genanki.Package(deck) 
    package.media_files = media_files 
    output_file = f"{deck.deck_id}.apkg" 
    package.write_to_file(output_file) 
    print(f"Deck created: {output_file}") 