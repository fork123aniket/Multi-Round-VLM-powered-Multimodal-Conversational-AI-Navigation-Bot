# VLM-powered-Multimodal-Conversational-AI-Bot

An advanced AI-powered chatbot that enables users to upload images, ask questions in text or audio, and receive real-time responses in both text and audio formats.  

## Features  
- **Image Upload and Analysis**: Accepts uploaded images or captures photos directly via webcam.  
- **Speech-to-Text**: Converts spoken questions into text using Google SpeechRecognition API.  
- **Multimodal Chat Interaction**: Integrates visual (image), text, and audio data for comprehensive user interaction.  
- **Real-Time Responses**: Provides responses powered by OpenAI's multimodal models.  
- **Text-to-Speech**: Reads out chatbot responses using pyttsx3 for enhanced accessibility.  

## Technology Stack  
- **Frontend**: [Streamlit](https://streamlit.io/) for building an interactive user interface.  
- **Backend**: OpenAI's multimodal API integration for intelligent conversational processing using state-of-the-art InternVL VLLM model.
- **RunPod**: InternVL model's responses are made available by serving and inferring the model using [vLLM](https://docs.vllm.ai/en/latest/)-powered endpoints provided by [RunPod Platform](https://www.runpod.io/).
- **Cloudinary**: For secure image upload and hosting.  
- **Google SpeechRecognition API**: Converts spoken input to text.  
- **Pyttsx3**: For generating voice responses.  
- **Pillow (PIL)**: Processes and displays images.  

## How It Works  
1. **Upload or Capture an Image**:  
   - Upload an image file in `.png`, `.jpg`, or `.jpeg` formats.  
   - Alternatively, use your webcam to capture a photo directly.  

2. **Ask Your Question**:  
   - Speak into your microphone or type your question.  
   - The bot processes both your question and the image for context.  

3. **Receive Responses**:  
   - Textual responses appear on-screen.  
   - Optionally, listen to the response via the text-to-speech feature.  

## Installation  

### Prerequisites  
- Python 3.8 or higher.  
- Install dependencies using `pip`.  

### Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/fork123aniket/VLM-powered-Multimodal-Conversational-AI-Bot.git
   cd VLM-powered-Multimodal-Conversational-AI-Bot
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
3. Set up API Keys and Endpoint:
    - Replace placeholders in the script for OpenAI, RunPod Endpoint, and Cloudinary.
4. Run the application:
    ```bash
    streamlit run multimodal_chatbot.py

## Usage
1. Launch the Web App: Open the provided local server link in your browser.
2. Interact: Upload or capture an image, speak, or type your question by pressing the `Ask Me Anything!` button.
3. Explore Responses: Read or listen to the chatbot's answers by pressing the `Submit` button.

## Project Structure

    ├── multimodal_chatbot.py   # Main application script  
    ├── requirements.txt        # Dependencies  
    └── README.md               # Project documentation  
