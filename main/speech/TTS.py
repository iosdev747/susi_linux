""" This module implements all Text to Speech Services.
You may use any of the speech synthesis services by calling the
respective method.
"""
import subprocess   # nosec #pylint-disable type: ignore
import json_config
from google_speech import Speech
from watson_developer_cloud import TextToSpeechV1

config = json_config.connect('config.json')

text_to_speech = TextToSpeechV1(
    username=config['watson_tts_config']['username'],
    password=config['watson_tts_config']['password'])


def speak_flite_tts(text):
    """ This method implements Text to Speech using the Flite TTS.
    Flite TTS is completely offline. Usage of Flite is recommended if
    good internet connection is not available"
    :param text: Text which is needed to be spoken
    :return: None
    """
    filename = '.response'
    file = open(filename, 'w')
    file.write(text)
    file.close()
    # Call flite tts to reply the response by Susi
    flite_speech_file = config['flite_speech_file_path']
    print('flite -voice file://{0} -f {1}'.format(flite_speech_file, filename))
    subprocess.call(   # nosec #pylint-disable type: ignore
        ['flite', '-v', '-voice', 'file://' + flite_speech_file, '-f', filename, '-o', 'extras/output.wav'])   # nosec #pylint-disable type: ignore
    subprocess.call(['play', 'extras/output.wav'])   # nosec #pylint-disable type: ignore


def speak_watson_tts(text):
    """ This method implements Text to Speech using the IBM Watson TTS.
    To use this, set username and password parameters in config file.
    :param text: Text which is needed to be spoken
    :return: None
    """
    with open('extras/output.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept='audio/wav',
                                      voice=config['watson_tts_config']['voice']))

    subprocess.call(['play', 'extras/output.wav'])   # nosec #pylint-disable type: ignore


def speak_google_tts(text):
    """ This method implements Text to Speech using the Google Translate TTS.
    It uses Google Speech Python Package.
    :param text: Text which is needed to be spoken
    :return: None
    """
    sox_effects = ("tempo", "1.2", "pitch", "2", "speed", "1")
    Speech(text=text, lang='en').play(sox_effects)
