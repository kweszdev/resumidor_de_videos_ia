# -- resumidor de videos com ias da openai by kweszdev 2025 -- 
# -- v0.1

# pip install pytubefix
# pip install openai-whisper
# pip install moviepy
# pip install torch
# pip install requests

"""
-- documentação
so sai do looping do cather se o video for escolihdo e dar certo em pegar o youtube
ollama necessario - ok
resquests
problemas
versões
possivel converter e transcriber individuais
add prints para passo a apasso 
tempo de cada passo
trancrevere demora muito dependo do model
melhoarar o prompt ou fazer mais de um camada 
verificar se ollama esta instlado e na porta certa, verificar se a ia escolhida existe na lista 
tipos de prompt
inico da interface
"""

import whisper 
import torch
import platform
import requests
import json
from pytubefix import YouTube
from pytubefix.request import RegexMatchError
from moviepy import AudioFileClip

# -- principal para organização
def main():
    # chamo e guarado o resultado do url_cather que vai ser youtube do audio
    url_cath = url_catcher()

    # chamo o transcriber_converter para converter em mp3 e trasncrever para txt
    transcibe_catch = transcriber_converter(url_cath)

    # chamo para resumir a trancrição do video
    resume(transcibe_catch)

# -- pega a url do video
def url_catcher():
    # criando uma variavel para repetição e para verificção da partes eguintes do codigo
    repeticao_url = True
    while repeticao_url:
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
                return audio_yt
                break
            # qualuer outra coisa a nao ser enter ta cancelando
            else:
                print("digite a url novamente!")
            
        # verificção de erro caso a url seja invalida
        except RegexMatchError:
            print("url invalida")

# -- converte e trancreve
def transcriber_converter(audio_yt):
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
    return audio_txt

# -- resume o video (atraves da comunicaçao com o ollama e a ia selecionada, api)
def resume(audio_txt):
    # url da api (no caso ela ta rodando em local host)
    url_api = "http://localhost:11434/api/generate"

    #dar a escolha do ia a ser usada (experimentyal, vir um pacote de ias baixadas junto e ele poder instalar outras)
    ia = input("digite a ia a ser usado: ")
    # ollama run {ia}

    # -- montando a requisiçaõ par api 
    header = {"content-type": "application/json"}
    prompt = (
    "Resuma o seguinte texto, que foi transcrito de um vídeo. "
    "Comece identificando e declarando explicitamente o tema principal ou os temas abordados. "
    "Em seguida, elabore um resumo claro e objetivo, destacando os pontos mais importantes discutidos no vídeo. "
    "Use linguagem simples e direta, mantendo o conteúdo fiel ao original."
    f"texto: {audio_txt}"
    )
    body = {"model":f"{ia}", "prompt":f"{prompt}", "stream":False}

    # enviando requisição
    response = requests.post(url_api, headers=header, json=body )

    data = response.json()
    tempo_em_segundos = data["total_duration"] / 1_000_000_000
    print(f"R:{data['response']} \n tempo de duração: {tempo_em_segundos}")

    # # a resposta e por varais linhas e o json nao consgeu lidar com esse tipo de stream, enao vamos pegar linha a linhas
    # for line in response.iter_lines():
    #     data = json.loads(line.decode("utf-8")) 
    #     if "response" in data:
    #         print(data["response"], end='', flush=True)

    print("\nresumindo..")

# -- pesquisa e aprofunda o resumo ou temma do video
def search_create():
    print("pesquisando sobre o tema e o resumo, para criar flash cards ou outros resumos mais aprofundados")

main()
