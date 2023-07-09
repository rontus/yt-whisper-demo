import gradio as gr
import whisper
import openai
from pytube import YouTube

loaded_model = whisper.load_model("base")

openai.api_key = "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"

def generate_text_from_message(message, model='gpt-4'):
  response = openai_chat_completion([{'role': 'user', 'content': "Summarize IN DETAIL, adjusting the summary length according to the transcription's legnth, the YouTube-video transcription below. Also make guess how many different characters' speech is included in the transcription. Also analyze the style of this video (comedy, drama, instructional, educational, etc.). Transcription:" + message}], model)
  return response

def openai_chat_completion(messages, model='gpt-4'):
  try:
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response['choices'][0]['message']['content']
  except (openai.error.APIConnectionError,
          openai.error.APIError,
          openai.error.AuthenticationError,
          openai.error.InvalidRequestError,
          openai.error.PermissionError,
          openai.error.RateLimitError,
          openai.error.ServiceUnavailableError,
          openai.error.Timeout) as err:
    return f"OpenAI API Error: {err}"

def inference(link):
  yt = YouTube(link)
  path = yt.streams.filter(only_audio=True)[0].download(filename="audio.mp4")
  options = whisper.DecodingOptions(without_timestamps=True)
  results = loaded_model.transcribe(path)
#  summary = generate_text_from_message(results['text'])
  return results['text']

def change_model(size):
  loaded_model = whisper.load_model(size)

title="Youtube Whisperer"
description="Speech to text transcription of Youtube videos using OpenAI's Whisper"
block = gr.Blocks()

with block:
    gr.HTML(
        """
            <div style="text-align: center; max-width: 500px; margin: 0 auto;">
              <div>
                <h1>Youtube Whisperer</h1>
              </div>
              <p style="margin-bottom: 10px; font-size: 94%">
                Speech to text transcription and summarization of Youtube videos using OpenAI's Whisper and GPT-4
              </p>
            </div>
        """
    )
    with gr.Group():
        with gr.Box():
          sz = gr.Dropdown(label="Model Size", choices=['base','small', 'medium', 'large'], value='base')
          sz.change(change_model, inputs=[sz], outputs=[])
          link = gr.Textbox(label="YouTube Link")
          transcription = gr.Textbox(
              label="Transcription", 
              placeholder="Transcription Output",
              lines=5)
#          summary = gr.Textbox(
#              label="Summary", 
#              placeholder="Summary Output",
#              lines=5)
          with gr.Row().style(mobile_collapse=False, equal_height=True): 
              btn = gr.Button("Summarize")       
              btn.click(inference, inputs=[link], outputs=[transcription])

block.launch(server_name='0.0.0.0', share=True)
