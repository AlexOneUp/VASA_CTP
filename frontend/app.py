import os
import random
import streamlit as st
import sys

from dotenv import load_dotenv
from sounddevice import rec, wait
from scipy.io.wavfile import write


load_dotenv()

# Absolute paths must be used.
backend_path = os.getenv("backend_path")
project_path = os.getenv("project_path")
sys.path.append(backend_path)
from audio_processing import get_features, increase_array_size, predict


def local_css(file_name):  # Use local CSS
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles/style.css")

# Prompts used in training data.
prompts = [
    "Kids are talking by the door",
    "Dogs are sitting by the door",
    "It's eleven o'clock",
    "That is exactly what happened",
    "I'm on my way to the meeting",
    "I wonder what this is about",
    "The airplane is almost full",
    "Maybe tomorrow it will be cold",
    "I think I have a doctor's appointment",
    "Say the word apple",
]

# emotions = ['angry 😡', 'calm 😌', 'disgusted 🤢', 'fearful 😨', 'happy 😆',
# 'neutral 🙂', 'sad 😢', 'surprised 😳']

emotion_dict = {
    "angry": "angry 😡",
    "calm": "calm 😌",
    "disgust": "disgusted 🤢",
    "fear": "scared 😨",
    "happy": "happy 😆",
    "neutral": "neutral 🙂",
    "sad": "sad 😢",
    "surprise": "surprised 😳",
}

# Session states.
if "initial_styling" not in st.session_state:
    st.session_state["initial_styling"] = True

if "particle" not in st.session_state:
    st.session_state["particle"] = "👋🏻"

if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

if "emotion" not in st.session_state:
    st.session_state["emotion"] = ""

if "is_prompt" not in st.session_state:
    st.session_state["is_prompt"] = False

if "is_emotion" not in st.session_state:
    st.session_state["is_emotion"] = False

if "is_first_time_prompt" not in st.session_state:
    st.session_state["is_first_time_prompt"] = True


# emotion = random.choice(list(emotion_dict))
# partition = emotion_dict.get(emotion).split(" ")


def styling(particle):  # model for 'snowfall' animation
    return st.markdown(
        f"""
      <div class="snowflake">{particle}</div>
      <div class="snowflake">{particle}</div>
      <div class="snowflake">{particle}</div>
      <div class="snowflake">{particle}</div>
      <div class="snowflake">{particle}</div>

      <div class='box'>
        <div class='wave -one'></div>
        <div class='wave -two'></div>
        <div class='wave -three'></div>
      </div>
    """,
        unsafe_allow_html=True,
    )


# def card():
#   return """
#     <div class="card" style="width: 100%;">
#       <div class="card-header">
#       Card Header
#       </div>

#       <img class="card-img-top" src="https://t4.ftcdn.net/jpg/03/27/36/95/360_F_327369570_CAxxxHHLvjk6IJ3wGi1kuW6WTtqjaMpc.jpg" alt="Card image cap">
#       <div class="card-body">
#         <h5 class="card-title">Voice Emotion Recognition on Audio</h5>
#         <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
#         <a href="#" class="btn btn-primary col-md-3">Go somewhere</a>
#         <a href="#" class="btn btn-primary col-md-3">Go somewhere</a>
#         <a href="#" class="btn btn-primary col-md-3">Go somewhere</a>
#         <div class='btn-toolbar'>
#           <div class='btn-group'>
#             <button class="btn-danger signin">Sign In</button>
#             <button class="btn-success signup">Sign Up</button>
#           </div>
#         </div>
#       </div>
#     </div>
#   """
#


# Bootstrap cards w/ reference to CSS.
st.markdown(
    """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
        integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    """, unsafe_allow_html=True,
)


# st.markdown(card(), unsafe_allow_html=True)


def make_grid(rows, cols):
    grid = [0] * rows
    for i in range(rows):
        with st.container():
            grid[i] = st.columns(cols)
    return grid


# Title.
title = f"""<p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.3rem;">
            Voice Emotion Recognition on Audio</p>"""
st.markdown(title, unsafe_allow_html=True)

# Image.
image = "https://t4.ftcdn.net/jpg/03/27/36/95/360_F_327369570_CAxxxHHLvjk6IJ3wGi1kuW6WTtqjaMpc.jpg"
st.image(image, use_column_width=True)

# Header.
header = f"""<p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 1.7rem;">
            Click to generate a random prompt and emotion:</p>"""
st.markdown(header, unsafe_allow_html=True)


def prompt_btn():
    if not (st.session_state["is_first_time_prompt"]):
        styling(particle=st.session_state["particle"])

    prompt = '"' + random.choice(prompts) + '"'
    st.session_state["prompt"] = prompt

    st.markdown(
        f"""
            <p align="center" style="font-family: monospace; color: #ffffff; font-size: 2rem;">
            {st.session_state["prompt"]}</p>
        """, unsafe_allow_html=True,
    )

    if not (st.session_state["is_first_time_prompt"]):
        st.markdown(
            f"""
                <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                Try to sound {emotion_dict.get(st.session_state["emotion"])}</p>
            """, unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
                <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                Please generate an emotion!</p>
            """, unsafe_allow_html=True,
        )


def emotion_btn():
    st.session_state["initial_styling"] = False
    st.session_state["is_first_time_prompt"] = False

    emotion = random.choice(list(emotion_dict))
    partition = emotion_dict.get(emotion).split(" ")
    emotion = partition[0]
    st.session_state["emotion"] = emotion

    particle = partition[1]
    st.session_state["particle"] = particle
    styling(particle=st.session_state["particle"])

    st.markdown(
        f"""
            <p align="center" style="font-family: monospace; color: #ffffff; font-size: 2rem;">
            {st.session_state["prompt"]}</p>
        """, unsafe_allow_html=True,
    )
    st.markdown(
        f"""
            <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
            Try to sound {emotion_dict.get(st.session_state["emotion"])}</p>
        """, unsafe_allow_html=True,
    )


# Record button.
def record_btn():
    fs = 44100  # Sample rate.
    seconds = 3  # Duration of recording.

    with st.spinner(f"Recording for {seconds} seconds ...."):
        myrecording = rec(int(seconds * fs), samplerate=fs, channels=1)
        wait()  # Wait until recording is finished.

        write(
            project_path + "frontend/soundfiles/recording.wav", fs, myrecording
        )  # Save as .wav file.
        st.success("Recording completed.")


# Play button.
def play_btn():  # Play the recorded audio.
    styling(particle=st.session_state["particle"])
    st.markdown(
        f"""
            <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2rem;">
            {st.session_state["prompt"]}</p>
        """, unsafe_allow_html=True,
    )
    if not (st.session_state["is_first_time_prompt"]):
        st.markdown(
            f"""
                <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                Try to sound {emotion_dict.get(st.session_state["emotion"])}</p>
            """, unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
                <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                Please generate a prompt and an emotion!</p>
                <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">Then, record your audio.</p>
            """, unsafe_allow_html=True,
        )
    try:  # Load audio file.
        audio_file = open(project_path + "frontend/soundfiles/recording.wav", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
    
    except: st.write("Please record sound first.")


# Classify button.
def classify_btn():
    try:
        wav_path = project_path + "frontend/soundfiles/recording.wav"
        audio_features = get_features(wav_path, 3)
        
        audio_features = increase_array_size(audio_features)
        emotion = predict(audio_features)

        if(st.session_state["emotion"] != ""): # what happens when st.session_state["emotion"] == ""
            if(emotion in st.session_state["emotion"]):
                st.session_state["particle"] = "😆"
                styling(particle=st.session_state["particle"])
                st.markdown(
                    f"""
                        <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                        You tried to sound {st.session_state["emotion"].upper()} and you sounded {emotion.upper()}</p>
                        <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">Well done!👍</p>
                    """, unsafe_allow_html=True,
                )

                try:  # Load audio file.
                    audio_file = open(project_path + "frontend/soundfiles/recording.wav", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
               
                except: st.write("Please record sound first.")
                st.balloons()
            
            else:
                st.session_state["particle"] = "😢"
                styling(particle=st.session_state["particle"])
                st.markdown(
                    f"""
                        <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 2.5rem;">
                        You tried to sound {st.session_state["emotion"].upper()} however you sounded {emotion.upper()}👎</p>
                    """, unsafe_allow_html=True,
                )

                try:  # Load audio file.
                    audio_file = open(project_path + "frontend/soundfiles/recording.wav", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
                
                except: st.write("Please record sound first.")
    except: st.write("Something went wrong. Please try again.")


# User Interface.
if st.session_state["initial_styling"]:
    styling(particle=st.session_state["particle"])

# Create custom grid.
grid1 = make_grid(1, 14)

# Prompt Button.
prompt = grid1[0][5].button("Prompt")
if prompt or st.session_state["is_prompt"]:
    st.session_state["is_emotion"] = False
    prompt_btn()

# Emotion Button.
emotion = grid1[0][7].button("Emotion")
if emotion or st.session_state["is_emotion"]:
    st.session_state["is_prompt"] = False
    emotion_btn()

# Create custom grid.
grid2 = make_grid(3, (12, 12, 3))


# Record Button.
record = grid2[0][0].button("Record")
if record:
    record_btn()

# Play Button.
play = grid2[0][1].button("Play")
if play:
    play_btn()

# Classify Button.
classify = grid2[0][2].button("Classify")
if classify:
    classify_btn()

# GitHub repository of project.
st.markdown(
    f"""
        <p align="center" style="font-family: monospace; color: #FAF9F6; font-size: 1rem;"><b> Check out our
        <a href="https://github.com/Alexoneup/VERA_CTP" style="color: #FAF9F6;"> GitHub repository</a></b>
        </p>
   """, unsafe_allow_html=True,
)


# Skeleton on Predicted Value of the audio.
# def state_emotion():

#   # In the case of persistent emotion data from a previous session:
#   try:
#     st.write("Are you still", st.session_state.emotion, "?")

# # Prompt 'Yes' or 'No' buttons
#   # Then let's you predict again

# # Show the Predict Emotion first.
#   except:
#     play = st.button('Predict Emotion', key='emotion', on_click=state_emotion)
