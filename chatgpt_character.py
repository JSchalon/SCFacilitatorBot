import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager
import socketio

ELEVENLABS_VOICE = "Freya" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

# Create Flask-SocketIO server
sio = socketio.Client()

@sio.event
def connect():
    print('[yellow]Connected to server')

@sio.event
def disconnect():
    print('[yellow]Disconnected from server')

# Connect to the Flask-SocketIO server
sio.connect('http://127.0.0.1:5000')

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
Du är en diskussionsledare på ett språkcafé. Ditt jobb är att generera lämpliga diskussionsämnen för vuxna språkinlärare av svenska språket som kan användas i språkcafé-miljön. Målet med detta är att främja diskussioner, samt hjälpa människor i olika åldrar, kön och kulturell bakgrund.
                        
Först kommer du att bli ombedd att ange ett lämpliga diskussionsämne. Efter det kan besökarna på språkcaféet ge dig det svar eller den konsensus som människor har uppnått, eller be dig om nya diskussionsämnen.
                        
När du svarar måste du följa följande regler: 
1) Alltid svara på svenska, såvida du inte uttryckligen ombeds att svara på ett annat språk
2) Ge korta svar, max 2-3 satser. 
3) Håll dig alltid till din karaktär, oavsett vad som händer.
4) Om du blir tillfrågad, ge några förslag på lämpliga diskussionsämnen.
5) Håll dina svar begränsade till bara några meningar.
6) Försök att använda ett språk som är lämpligt för nybörjare, dvs. inte för svårt men inte heller för lätt. 
7) Om det är nödvändigt att använda mer komplicerade ord, förklara dem.
8) Du behöver inte förklara varför ett ämne är bra, du bara ställer den.
9) Frågorna ska vara lämpliga för ett språkcafé och kan handla om Sverige men även om kultur, andra länder, politik eller andra ämnen, så länge de är lämpliga.
10) Tilltala alltid människor som "ni" och använda "er/ert/era".
                        
Okej, låt samtalet börja!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[yellow]Open http://127.0.0.1:5000/ to access graphical webinterface!")
print("[green]Starting the loop, press S to begin")

sio.emit('message', '{"type": "animate", "msg": "speak"}')
sio.emit('message', '{"type": "display", "msg": "Nu kan ni använda \'S\' för att börja prata med mig!", "record": "false"}')

interactionIndex = 0

while True:
    # Wait until user presses "S" key
    if keyboard.read_key() != "s":
        time.sleep(0.1)
        continue

    print("[green]User pressed S key! Now listening to your microphone:")
    if interactionIndex > 0:
        sio.emit('message', '{"type": "animate", "msg": "listen", "record": "false"}')
    else:
        sio.emit('message', '{"type": "animate", "msg": "listen", "record": "false"}')

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        sio.emit('message', '{"type": "animate", "msg": "speak"}')
        sio.emit('message', '{"type": "display", "msg": "Tyvärr, jag förstod inte det. Försök igen.", "record": "false"}')
        print("[red]Did not receive any input from your microphone!")
        continue
    
    sio.emit('message', '{"type": "animate", "msg": "load"}')
    

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    sio.emit('message', '{"type": "animate", "msg": "speak"}')
    time.sleep(.1)

    message_string = '{"type": "question", "msg": "' + mic_result.replace('"', '\\"') + '", "record": "false"}'
    sio.emit('message', message_string)

    message_string = '{"type": "display", "msg": "' + openai_result.replace('"', '\\"') + '", "record": "true"}'
    sio.emit('message', message_string)
    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)
    

    # Disable Pajama Sam pic in OBS
    #obswebsockets_manager.set_source_visibility("*** Mid Monitor", "Pajama Sam", False)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    interactionIndex += 1