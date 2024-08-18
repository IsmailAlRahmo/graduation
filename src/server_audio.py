from flask import Flask,jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import librosa
from array import array
import wave
import pickle
from sys import byteorder
from io import BytesIO
import soundfile
import pyaudio
from struct import pack

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


# model = pickle.load(open("mlp_classifier.model", "rb"))
audio_frames = []
BUFFER_DURATION = 5  # seconds (adjust according to your needs)
RATE = 16000
THRESHOLD = 500


@app.route("/")
def index():
    return "Socket.IO Flask Server"


def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(
                librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0
            )
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(
                librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0
            )
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)

            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(
                librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0
            )
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(
                librosa.feature.tonnetz(
                    y=librosa.effects.harmonic(X), sr=sample_rate
                ).T,
                axis=0,
            )
            result = np.hstack((result, tonnetz))
    return result


THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 16000
MODEL = pickle.load(open("mlp_classifier.model", "rb"))
SILENCE = 30


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array("h")
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        r = array("h")

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array("h", [0 for i in range(int(seconds * RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds * RATE))])
    return r


def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    num_silent = 0
    snd_started = False

    r = array("h")

    while 1:
        # little endian, signed short
        snd_data = array("h", stream.read(CHUNK_SIZE))
        if byteorder == "big":
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > SILENCE:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack("<" + ("h" * len(data)), *data)

    wf = wave.open(path, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


advice = {
    "angry": "It's important to channel your passion into your speech, but try not to let anger take over. Take a few deep breaths and try to calm down before continuing. Remember, you want to persuade your audience, not alienate them.",
    "sad": "It's okay to show vulnerability in your speech, but don't let sadness dominate. Try to bring in some positive or hopeful elements to balance it out. Remember, your audience will likely mirror your emotions.",
    "calm": "You're doing great! A calm demeanor can help your audience focus on your message. Just make sure you're also showing enthusiasm where appropriate to keep your audience engaged.",
    "happy": "Your positive energy is infectious and can help engage your audience. Just make sure your happiness is appropriate for the topic of your speech.",
    "fearful": "It's natural to feel nervous, especially when speaking in public. Try to take some deep breaths and slow down your speech. Remember, it's okay to take a few moments to collect your thoughts.",
    "motivation": "You're doing an excellent job! Your improvement is clearly noticeable. Keep practicing and challenging yourself, and remember that every great speaker was once a beginner. Keep up the good work!",
}


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack("<" + ("h" * len(data)), *data)

    wf = wave.open(path, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


@socketio.on("start_recording")
def handle_audio():
    print("Recording started")
    # You can emit a response here to notify the client
    socketio.emit("audio_status", {"status": "Recording started"})
    try:  # Set the desired number of iterations
        # model = pickle.load(open("mlp_classifier.model", "rb"))
        print("Please talk")

        last_result = None  # Store the last predicted emotion
        accumulated_probabilities = {
            emotion: 0.0 for emotion in MODEL.classes_
        }  # Initialize accumulated probabilities

        # Iterate a specific number of times
        filename = "test.wav"
        # Record the file (start talking)
        record_to_file(filename)
        # Extract features and reshape them
        features = extract_feature(filename, mfcc=True, chroma=True, mel=True).reshape(
            1, -1
        )
        # Predict
        result = MODEL.predict(features)[0]

        # Update the accumulated probabilities
        for emotion, prob in zip(MODEL.classes_, MODEL.predict_proba(features)[0]):
            accumulated_probabilities[emotion] += prob

        # Normalize the accumulated probabilities
        total_sum = sum(accumulated_probabilities.values())
        normalized_probabilities = {
            emotion: prob / total_sum
            for emotion, prob in accumulated_probabilities.items()
        }

        # Show the normalized probabilities
        for emotion, prob in normalized_probabilities.items():
            print(f"{emotion}: {prob:.2f}")

        # Print the advice if the result is different from the last result
        if result != last_result:
            print("result:", result)
            print(
                "advice:",
                advice.get(result, "No advice available for this emotion."),
            )
        last_result = result  # Update the last predicted emotion
        socketio.emit("audio_message", {"message": [advice.get(last_result)]})
    except Exception as e:
        print(f"Error processing audio: {e}")
        socketio.emit("server_message", {"message": "Error processing audio."})


@socketio.on("connect")
def handle_connect():
    print("connect called")
    socketio.emit(
        "server_message", {"message": "Welcome! You are connected to the server."}
    )

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)
