# -- resumidor de videos com ias da openai by kweszdev 2025 -- 
# -- v0.1

''' -- documentação: 
- openai-whisper nao funciona no python 3.13 e re'uer o fmmpeg instalado no pc, ele utiliza de alto procesamento, memoria
e internet, esteja ciente.
- estou adiconando uma versao do pythorch que indenfique o cuda(12.6 usado) da gpu para rodar no whisper e torna-lo mais rapido, 
cuda so existe nas placas de video NVIDIA, ele indenfica automatico se tem o cuda na placa e se e compativel, se nao roda todo processo na 
cpu, caso tenha uma placa NVIDIA e mesmo assim nao esta indentficando rode "nvidia-smi", e veja se tem o cuda.
- caso nao queira utilizar a gpu 


'''
# pip install pytubefix
# pip install openai-whisper
# pip install moviepy
# pip install torch

import whisper
import torch
import platform
from pytubefix import YouTube
from pytubefix.request import RegexMatchError
from moviepy import AudioFileClip

# criando uma variavel para repetição e para verificção da partes eguintes do codigo
url_catch = False
while not url_catch:
    # pedindo a url do video para o usuario
    url = input("digite a url do video do youtube (Ex: 'https://www.youtube.com/watch?v=dl-ZgxlHUtI&t=4s'): ")
    try:
        video_yt = YouTube(url) # mostrar o processo
        # pegando o titulo do video e thumb para mostar ao usuario
        title_yt = video_yt.title
        thumb_yt = video_yt.thumbnail_url
        creator_yt = video_yt._author
        # na interface teriamos um botao para verificação
        btn = input(f' o seu video e esse? \n "{title_yt}" - by "{creator_yt}"\n')
        if btn == '':
            # pegendo o audio do video para trancrever
            audio_yt = video_yt.streams.get_audio_only()
            url_catch = True
        # qualuer outra coisa a nao ser enter ta cancelando
        else:
            print("digite a url novamente!")
        
    # verificção de erro caso a url seja invalida
    except RegexMatchError:
        print("url invalida")

# se o video pego for certo
if url_catch:
    # escolhendo o medlo da ia whisper
    model_user = input("""
    Digite o modelo do Whisper a ser usado:

    tiny    - Muito rápido, mas pouca precisão
    base    - Rápido, mas ainda com erros
    small   - Equilíbrio entre velocidade e precisão
    medium  - Mais preciso, porém mais pesado
    large   - Alta precisão (requer mais memória da GPU)

    Modelo escolhido: 
    """).strip().lower() # tratando de forma facil

    # Verificando se o modelo é válido
    modelos_validos = ["tiny", "base", "small", "medium", "large"]
    if model_user not in modelos_validos:
        print("❌ Modelo inválido! Usando 'base' como padrão.")
        model_user = "base"

    # Carregando modelo com GPU (se disponível)
    device = "cuda" if torch.cuda.is_available() else "cpu" # verifica se cuda(modelo do t=orch para compatibilidade, dependo da cpu) ou se nao houver usa a cpu 
    cpu_name = platform.processor()
    device_user = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "{cpu_name}" # para pegar o nomme do presseasdor usado ou gpu
    print(f"\nCarregando modelo: '{model_user}' no dispositivo: {device_user}({device})...")
    model = whisper.load_model(model_user).to(device)
    print("Modelo carregado com sucesso!\n")

    # cria uma caminho para tranformar em mp4
    audio_yt_path = audio_yt.download(filename='audio.mp4')

    # converter para wav .16khz para mais nitidez

    # converte para mp3
    mp3_audio_path = 'audio.mp3'
    audio_converter =  AudioFileClip(audio_yt_path) # varaivel para poder converter e add o path escolhido
    print("\nConvetendo audio para mp3..")
    audio_converter.write_audiofile(mp3_audio_path)
    print("Audio convertido!")

    # trancrevendo o audio
    print("\ntranscrevendo o audio...")
    audio_transcribe = model.transcribe(mp3_audio_path, fp16=True, language="pt", verbose=True, temperature=0) # verbose mostra o pregresso, fp16 e para ela nao usar ou usar gpu , taparature para fazer o ehisper nao corrigir
    print("audio trancrevido!")

    # pegando o teto da trancrisão
    audio_txt = audio_transcribe['text']
    print(audio_txt)







     
