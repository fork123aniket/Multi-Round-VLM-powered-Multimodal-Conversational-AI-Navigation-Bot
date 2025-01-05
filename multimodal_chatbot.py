import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import hashlib
import cloudinary
import cloudinary.uploader
import cloudinary.api
import speech_recognition as sr
import pyttsx3

# OpenAI API Key (Replace with your key or use environment variable)
api_key = "your_openai_api_key"
pod_endpoint = "your_vllm_endpoint_id"
client = OpenAI(api_key=api_key, base_url=pod_endpoint)

# Function to upload an image and return a URL or encoded string
def get_image_url(image_path):
    # Configure Cloudinary with your credentials
    cloudinary.config(
        cloud_name='cloud_name',  # Replace with your Cloudinary cloud name
        api_key='api_key',        # Replace with your Cloudinary API key
        api_secret='secret_key'   # Replace with your Cloudinary API secret
)

    # Upload the image to Cloudinary
    upload_result = cloudinary.uploader.upload(image_path)
    
    # Get the public URL of the uploaded image
    image_url = upload_result.get('secure_url')
    if image_url:
        print(f"Image uploaded successfully! Public URL: {image_url}")
        return image_url
    else:
        print("Failed to upload image.")
        return None

# Function to hash an image
def hash_image(image):
    """Generate a hash for the image to detect changes."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    return hashlib.md5(img_byte_arr.getvalue()).hexdigest()

# Function to speak text
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Callback function for button press
def handle_speak(index):
    bot_message = st.session_state.chat_history[index]["content"]
    st.session_state.speak_triggered = False
    speak_text(bot_message)

# Function to perform speech-to-text using Google SpeechRecognition API
def speech_to_text():
    r = sr.Recognizer()
    
    with sr.Microphone() as source2:
        try:                
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            
            #listens for the user's input 
            st.info("Listening... Please speak into the microphone.")
            audio2 = r.listen(source2, timeout=10)

            with st.spinner("Converting question to text..."):
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print(f"Did you say: {MyText[0].upper() + MyText[1:] + '?'}")
                return MyText[0].upper() + MyText[1:] + '?'
        
        except sr.RequestError as e:
            print(f"Google Speech Recognition service is unavailable: {e}")

        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            
        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")

# Chat payload generator
def generate_payload(question, image_url, history):
    """Generate the payload for the multimodal API."""
    messages = history + [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        }
    ]
    return messages

# Function to communicate with OpenAI or other multimodal API
def multimodal_chat(payload):
    """Send payload to the multimodal API and receive response."""
    # Replace the API interaction with the actual multimodal model if necessary.
    response = client.chat.completions.create(
        model="OpenGVLab/InternVL2-1B",  # Use your multimodal model
        messages=payload,
        temperature=0.7,
        max_tokens=512
    )

    answer = response.choices[0].message.content

    return answer

# Streamlit layout
st.title("VLM-powered Multimodal Conversational AI Bot")
st.info("Enable users to upload an image and pose a question to receive real-time responses delivered in both text and audio formats.")

# Session state to maintain history and image hash
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "image_hash" not in st.session_state:
    st.session_state.image_hash = None
if "question" not in st.session_state:
    st.session_state.question = ""
if "photo" not in st.session_state:
    st.session_state.photo = False
if "speak_triggered" not in st.session_state:
    st.session_state.speak_triggered = False  # To track which message's Speak button was pressed


# Image upload section
# Choices
choices = ["Upload an image", "Take a photo"]

# Radio button
selected_action = st.radio("Choose the Input Image Format:", choices)

if selected_action == "Take a photo":
    photo = st.camera_input("Take a photo:")

    # If a photo is taken, display it
    if photo:
        # Convert the photo to a PIL Image
        cap_photo = Image.open(photo)
        
        # Save the image to a file
        cap_photo.save("captured_photo.png")

        # Get image URL or encode image
        image_url = get_image_url("captured_photo.png")
        st.info(f"Image is accessible at: {image_url}")
        st.session_state.photo = True

        # Check if the image has changed
        current_image_hash = hash_image(cap_photo)
        if st.session_state.image_hash is None:
            st.session_state.image_hash = current_image_hash
        elif st.session_state.image_hash != current_image_hash:
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.image_hash = current_image_hash
            st.session_state.photo = True
            st.warning("Image changed! Conversation history reset.")
    else:
        st.warning("No frame captured yet. Please try again.")
elif selected_action == "Upload an image":
    uploaded_image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Save the image to a file
        image.save("git_photo.png")

        # Get image URL or encode image
        image_url = get_image_url("git_photo.png")
        st.info(f"Image is accessible at: {image_url}")
        st.session_state.photo = True

        # Check if the image has changed
        current_image_hash = hash_image(image)
        if st.session_state.image_hash is None:
            st.session_state.image_hash = current_image_hash
        elif st.session_state.image_hash != current_image_hash:
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.image_hash = current_image_hash
            st.session_state.photo = True
            st.warning("Image changed! Conversation history reset.")

if st.button("Ask Me Anything!"):
        transcription = speech_to_text()
        question = str(transcription)
        st.session_state.question = question
            
        # Display the transcribed text
        st.write("**Transcribed Question:**")
        st.text_area("Text:", transcription, height=200)

if st.button("Submit"):
    if not st.session_state.photo:
        st.error("Please upload an image before asking a question.")
    elif not st.session_state.question:
        st.error("Please enter a question.")
    else:
        st.session_state.speak_triggered = True
        # Generate payload and get response
        payload = generate_payload(st.session_state.question, image_url, st.session_state.chat_history)
        response = multimodal_chat(payload)

        # Update history
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": st.session_state.question},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]
            }
        )
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

        # Display conversation
        st.markdown("### Conversation History")
        for idx, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown("**You:** " + message["content"][0]["text"])
            else:
                st.markdown("**Bot:** " + message["content"])
                button_key = f"speak_button_{idx}"  # Unique key for each button
                # Add a button with an `on_click` callback
                st.button(
                    "Speak",
                    key=button_key,
                    on_click=handle_speak,
                    args=(idx,),  # Pass the index as an argument to the callback
                )

# Display conversation
if not st.session_state.speak_triggered:
    st.markdown("### Conversation History")
    for idx, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown("**You:** " + message["content"][0]["text"])
        else:
            st.markdown("**Bot:** " + message["content"])
            button_key = f"speak_button_{idx}"  # Unique key for each button
            # Add a button with an `on_click` callback
            st.button(
                "Speak",
                key=button_key,
                on_click=handle_speak,
                args=(idx,),  # Pass the index as an argument to the callback
            )
