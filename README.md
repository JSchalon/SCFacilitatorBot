# Språkcafé Facilitator Bot
A simple app to have verbal conversations with OpenAi's GPT.
Work by Julian Schalon as part of a Master Thesis in Media Technologies, modified from [Babagaboosh](https://github.com/DougDougGithub/Babagaboosh) by DougDoug.

## SETUP:
1) This was written in Python 3.9.2. Install page here: https://www.python.org/downloads/release/python-392/

2) Run `pip install -r requirements.txt` to install all modules.

3) This uses the Microsoft Azure TTS, Elevenlabs, and OpenAi services. Using these services requires an account with them, as well as generating an API key for each. To access the API keys with this app, you need to add them as windows environment variables named AZURE_TTS_KEY, AZURE_TTS_REGION, ELEVENLABS_API_KEY, and OPENAI_API_KEY respectively.

4) Per default, this app uses the GPT-4 model from OpenAi. As of this writing (Jan 13 2024), you need to pay $1 to OpenAi in order to get access to the GPT-4 model API. So after setting up your account with OpenAi, you will need to pay for at least $1 in credits so that your account is given the permission to use the GPT-4 model when running my app. See here: https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4. However, using a cheaper model such as GPT-3.5-turbo or a free model such as GPT-3.5 is also possible, though these models perform worse in non-English applications such as the Språkcafé.

## Using the App

1) Run `flask_app.py'. This then enables you to use the web-based GUI. The GUI is not necessary to run the program, as every action can also be done through the command line, but it does improve the experience.

2) Open http://127.0.0.1:5000 in your Browser to access the GUI.

2) Run `chatgpt_character.py'

2) Once both apps are running, press F4 to start the conversation, and Azure Speech-to-text will listen to your microphone and transcribe it into text.

3) Once you're done talking, press P. Then the code will send all of the recorded text as input to OpenAI. Note that it is important to wait a second or two after you're done talking before pressing P so that Azure has enough time to process all of the audio.

4) Wait a few seconds for OpenAi to generate a response and for Elevenlabs to turn that response into audio. Once it's done playing the response, you can press F4 to start the loop again and continue the conversation.