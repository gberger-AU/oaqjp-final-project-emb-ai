import requests
import json

def emotion_detector(text_to_analyze):
    # URL of the sentiment analysis service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Constructing the request payload in the expected format
    myobj = { "raw_document": { "text": text_to_analyze } }

    # Custom header specifying the model ID for the sentiment analysis service
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Sending a POST request to the sentiment analysis API
    response = requests.post(url, json=myobj, headers=header)

    # Default response for error cases
    default_response = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    if response.status_code != 200:
        return response.status_code, default_response

    formatted_response = response.json()

    # Check if the response contains emotion predictions
    if 'emotionPredictions' not in formatted_response:
        return 400, default_response

    emotion_data = formatted_response['emotionPredictions'][0]['emotion']

    # Extracting sentiment label and score from the response
    emotion_scores = {emotion: score for emotion, score in emotion_data.items()}
    max_emotion = max(emotion_scores, key=emotion_scores.get)

    # Returning the status code and a dictionary containing sentiment analysis results
    return response.status_code, {**emotion_scores, 'dominant_emotion': max_emotion}
