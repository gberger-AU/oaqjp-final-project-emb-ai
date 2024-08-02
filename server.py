from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emo_detector():
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the emotion_detector function and store the response
    status_code, response = emotion_detector(text_to_analyze)

    if status_code == 400:
        rDict = {key: None for key in ["anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"]}
    if status_code != 200 or response['dominant_emotion'] is 'None':
        return "Invalid text! Please try again!"
    else:
        rDict = response

    # Return a formatted string with the sentiment label and score
    return ("For the given statement, the system response is 'anger': {}, "
    "'disgust': {}, 'fear': {}, 'joy': {} and 'sadness': {}. "
    "The dominant emotion is {}.").format(
        rDict['anger'], rDict['disgust'], rDict['fear'],
        rDict['joy'], rDict['sadness'], rDict['dominant_emotion'])
    

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
