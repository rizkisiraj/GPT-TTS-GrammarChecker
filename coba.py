import speech_recognition as sr
import pyttsx3 
import sounddevice as sd
import time
from TTS.api import TTS
from openai import OpenAI
from playsound import playsound

#init openai
client = OpenAI(api_key="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")
assistant = client.beta.assistants.create(
    name="Friendly Friend",
    instructions="Imagine you're a friendly companion giving easygoing advice. Keep it chill, use simple words, and respond like you're chatting with a laid-back friend. What's your casual and brief reply to their everyday query or statement?. Simple words do not put it for too long",
    tools=[],
    model="gpt-3.5-turbo"
)
thread = client.beta.threads.create()


# Init TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def syn_text(text, role):
    speaker = "ariana-grande-voice.mp3"
    wav = tts.tts_with_vc_to_file(
    text=text,
    speaker_wav=speaker,
    file_path=f"output{role}.wav"
    )

def play(role):
    playsound(f"output{role}.wav")

# Initialize the recognizer 
r = sr.Recognizer() 
 
# Function to convert text to
# speech
def SpeakText(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
     
     
# Loop infinitely for user to
# speak

list_of_words = []

while(True):    
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
            
        # use the microphone as source for input.
        with sr.Microphone() as source2:
                
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.5)
                
            #listens for the user's input 
            audio2 = r.listen(source2)
                
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Did you say ",MyText)
            if MyText.strip() == "stop talking":
                print("Stopping...")
                break
            list_of_words.append(MyText)
            message = client.beta.threads.messages.create(thread_id=thread.id,role="user",
                            content=MyText
                    )
            run = client.beta.threads.runs.create(thread_id=thread.id,assistant_id=assistant.id)
            print(run.model_dump_json(indent=4))
            while True:
                # Retrieve the run status
                run_status = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
                print(run_status.model_dump_json(indent=4))
                time.sleep(2)
                if run_status.status == 'completed':
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    for index,message in enumerate(messages):
                        syn_text(message.content[0].text.value, role=message.role)
                        play(message.role)
                        break
                    break
                else:
                    ### sleep again
                    time.sleep(2)
                
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
            
    except sr.UnknownValueError:
        print("unknown error occurred")


client = OpenAI(api_key="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")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": f"{list_of_words} From these list, determine what can i improve on my english speaking skill. DON'T TELL ME ABOUT THE CAPITALS AND PUNCTUATION, I DON'T NEED IT. MAKE IT SIMPLE"
    }
  ],
  temperature=0.8,
  max_tokens=128,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

syn_text(response.choices[0].message.content, role="conclusion")
play("conclusion")