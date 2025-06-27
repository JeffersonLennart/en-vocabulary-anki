import os
import uuid
from datetime import datetime
import json
import urllib.request
from english_ipa.cambridge import CambridgeDictScraper
import eng_to_ipa as ipa
from gtts import gTTS

def request(action : str, **params : dict[str, str]) -> dict[str, str]:
    '''Create a dictionary that represents the body of the request in JSON format'''
    return {'action': action, 'params': params, 'version': 6}

def invoke(action : str, **params : dict[str, str]) -> any:
    '''Return the response from the Anki-Connect actions'''
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def get_deck_names() -> list[str]:
    '''Return a list of the deck names'''
    result = invoke('deckNames')
    return result

def get_model_names() -> list[str]:
    '''Return a list of the model names'''
    result = invoke('modelNames')
    return result

def get_model_field_names(model_name : str) -> list[str]:
    '''Return a list of the field names for the given model name'''
    result = invoke('modelFieldNames', modelName = model_name)
    return result

def get_media_dir_path() -> str:
    '''Return the full path to the collection.media folder'''
    result = invoke('getMediaDirPath')
    return result

def get_word_ipa(word : str, slash : bool = False) -> str:
    '''Return the IPA representation for the given word.

    It first attempts to retrieve the IPA from the Cambridge Dictionary via web scraping. If that fails, it falls back to using the eng-to-ipa Python library
    
    Args:
        word (string): The word that will be converted to IPA.
        slash (bool): Flag to keep the slashes (/) at the beginning and end. Default (False)        
    '''
    word_ipa = str()
    scraper = CambridgeDictScraper()
    cambridge_response = scraper.get_ipa_in_dict(word)
    if cambridge_response["ipas"]:
        word_ipa = cambridge_response["ipas"][1]["ipas"][0]
        word_ipa = word_ipa if slash else word_ipa.strip('/')
    else:
        word_ipa = f"/{ipa.convert(word)}/" if slash else ipa.convert(word)
        # Check if the word exists
        if word.lower() in word_ipa.lower():
            raise Exception("The word doesn't exist")
    return word_ipa

def generate_file_name(name : str) -> str:
    '''Generate a file name that is hard to duplicate'''
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex
    return f"{name}_{timestamp}_{unique_id}"

def create_word_pronunciation(word : str):
    '''Create an audio file of the pronunciation for the given word and store it in the collection.media folder.
    Return the file name'''
    file_name = generate_file_name(word) + '.mp3'
    path = os.path.join(get_media_dir_path(), file_name)
    tts = gTTS(text=word, lang='en')
    tts.save(path)
    return file_name

def add_note(**params):
    '''Create a note. 
    
            "deckName": "Default",
            "modelName": "Basic",
            "fields": {
                "Front": "front content",
                "Back": "back content"
            },
            "options": {
                "allowDuplicate": false,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": false,
                    "checkAllModels": false
                }
            },
            "tags": [
                "yomichan"
            ],
            "audio": [{
                "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                "filename": "yomichan_ねこ_猫.mp3",
                "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                "fields": [
                    "Front"
                ]
            }],
            "video": [{
                "url": "https://cdn.videvo.net/videvo_files/video/free/2015-06/small_watermarked/Contador_Glam_preview.mp4",
                "filename": "countdown.mp4",
                "skipHash": "4117e8aab0d37534d9c8eac362388bbe",
                "fields": [
                    "Back"
                ]
            }],
            "picture": [{
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                "filename": "black_cat.jpg",
                "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                "fields": [
                    "Back"
                ]
            }]

    For more details, check the Anki-Connect library.'''    
    result = invoke('addNote', note = params)
    return result