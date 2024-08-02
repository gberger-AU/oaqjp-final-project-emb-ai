"""
This module provides a Flask web application for emotion detection.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detector():
    """
    Endpoint for emotion detection. Analyzes the provided text and returns the detected emotions.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the emotion_detector function and store the response
    status_code, response = emotion_detector(text_to_analyze)

    if status_code == 400:
        r_dict = {key: None for key in [
            "anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"
        ]}
    if status_code != 200 or response['dominant_emotion'] == 'None':
        return "Invalid text! Please try again!"
    r_dict = response

    # Return a formatted string with the sentiment label and score
    return (
        f"For the given statement, the system response is 'anger': {r_dict['anger']}, "
        f"'disgust': {r_dict['disgust']}, 'fear': {r_dict['fear']}, 'joy': {r_dict['joy']} and "
        f"'sadness': {r_dict['sadness']}. The dominant emotion is {r_dict['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    """
    Renders the index page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
