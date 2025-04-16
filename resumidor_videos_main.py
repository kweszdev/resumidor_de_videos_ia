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
versões de programa, .exe com interface, terminal, etc - 
trancrevere demora muito dependo do model
trancrever suga muita energia e memoria
oque cada função faz
oque cada blibioteca faz
avisar do subprocess
win e unix
os resumos sao salvos em txts

-- melhorias
windowns n linux
dar opção de usar resumos antigos, como resumos aprofundados ou algo do tipo em txts
versões de programa, .exe com interface, terminal, etc - 
tratamento
nao so resumir videos resumir audios
algum diferencial para so nao usar a ia - chatgpt < meu codigo
converter para wav .16khz para mais nitidez
converter e transcriber individuais - ok
tempo de cada passo
verificar se ollama esta instlado e na porta certa, verificar se a ia escolhida existe na lista 
fazer fluxo figma
tipos de prompt, nivel etc - ok
inico da interface

-- .exe
--- dependencias
empacotar com pyinstaller o binario do ffmpeg e usar o caminho relativo
empacotar blibliotecas usadas 

-- commit
adição de tratamentos, divisao de carregar modelo(verificação) e transcrever
"""

import whisper 
import subprocess
import torch
import platform
import requests
from requests import ConnectionError
import json
from pytubefix import YouTube
from pytubefix.request import RegexMatchError
from moviepy import AudioFileClip

# -- principal para organização
def main():
    # chama para verificção do ollama
    verify = verify_ollama()

    if verify:

        # chamo e guarado o result do url_cather que vai ser youtube do audio
        url_cath = url_catcher()

        # chamo o converter para converter em mp4 em mp3 
        converter_catch = converter(url_cath)

        # chamo o trancriber para trasncrever para txt
        transcriber_catch = transcriber(converter_catch)

        # chamo para carregar modelo whispér
        model_catch, model_cath = load_model()

        # chamo para resumir a trancrição do video
        resumo = resume(transcriber_catch, model_catch)

        # verificando se o usuario quer um resummo mais aprofundado (resumo vire uma apostila)
        confirm = search_create(resumo)

        # mosrando resumo caso ele nao quer um aprofundado
        if confirm == '':
            print(f"mostrando resumo \n resumo: {resumo}")

    else:
        print("fechando software")

# -- verificando se o ollama esta na maquina
def verify_ollama():
    # verificando com um subproces para ver se ollama e reconhecido (vcomo rodar o terminal enquanto usa o progrtama, tomar cuidado com antivirus etc)
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode != 0: # 0 e sucesso
            print("ollama nao instalado ou esta no path, impossivel de utilizar o software \n clique no botao 'instalar ollama automaticamente(i do lado faldno qoue faz) ou instale no : https://link/ollama/installer'") # futuramente opção de configuarr o path | chamar função do ollama nao instaldo aqui          
            return False # caso o função de certo isso aqui true
        else:
            print("\n ollama instalado, verificando se esta rodando no servidor!")

    except FileNotFoundError:
        # chamar função do ollama nao instaldo aqui   
        return False # caso o função de certo isso aqui true

    # verificando se ollma ta no localhost, atraves do request
    try:
        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            print("ollama instaldo e rodando localmente, inicializando o app!")
            return True
        elif response.status_code == 404:
            print("ollama nao rodando localmente, aperte o botao para rodar ou escreva no terminal: \n ''bash \n ollama serve \n ''")
            # chmar função do ollama nao rodando local aqui
            return False # caso o função de certo isso aqui true

        else:
            status = response.status_code
            print(f"ollama rodando localmente, porem servidor retornou: {status}")
            return False
        

    except ConnectionError:
        print("\n ollama não está rodando em http://localhost:11434 ou nao foi inicializado")
        # chmar função do ollama nao rodando local aqui
        return False # caso o função de certo isso aqui true

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

# -- converte o audio para mp3
def converter(audio_yt):
    try:
        # cria uma caminho para tranformar em mp4
        audio_yt_path = audio_yt.download(filename='audio.mp4')

        # converter para wav .16khz para mais nitidez

        # converte para mp3
        mp3_audio_path = 'audio.mp3'
        audio_converter =  AudioFileClip(audio_yt_path) # varaivel para poder converter e add o path escolhido
        print("\nConvetendo audio para mp3..")
        audio_converter.write_audiofile(mp3_audio_path)
        print("Audio convertido!")
        return mp3_audio_path
    except Exception as error:
        print(f"erro a converter, motivo: {error}")

# -- carrega o modelo whisper
def load_model():
    global model_cath
    try:
        # verifica se ha modelo ja carregado 
        if model_cath == "1":
           btn = input(f"modelo {model_user} ja carregado, deseja carregar outro modelo?")
           if btn == "":    
            model_cath = 0
            # repetição para escolher o modelo 
            while not model_cath:
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
                    print("❌ Modelo inválido!")
                else:
                    # decidindo onde vai rodar o  modelo (se disponível)
                    device = "cuda" if torch.cuda.is_available() else "cpu" # verifica se cuda(modelo do t=orch para compatibilidade, dependo da cpu) ou se nao houver usa a cpu 
                    cpu_name = platform.processor()
                    device_user = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "{cpu_name}" # para pegar o nomme do presseasdor usado ou gpu
                    print(f"\nCarregando modelo: '{model_user}' no dispositivo: {device_user}({device})...")

                    # carregando modelo
                    model = whisper.load_model(model_user).to(device)
                    print("Modelo carregado com sucesso!\n")

                    
                    return [model, True]
            else:
                return [model, True]
        else:
            model_cath = 1
            
    except Exception as error:
        print(f"erro ao carregar modelo, motivo: {error}")

# -- converte e trancreve
def transcriber(mp3_audio_path, model):
    try:
        # trancrevendo o audio
        print("\ntranscrevendo o audio...")
        audio_transcribe = model.transcribe(mp3_audio_path, fp16=True, language="pt", verbose=True, temperature=0) # verbose mostra o pregresso, fp16 e para ela nao usar ou usar gpu , taparature para fazer o ehisper nao corrigir
        print("audio trancrevido!")

        # pegando o teto da trancrisão
        audio_txt = audio_transcribe['text']
        return audio_txt
    except Exception as error:
        print("erro ao transcrever o audio!")

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
    print("\nresumindo..")
    response = requests.post(url_api, headers=header, json=body )

    data = response.json()
    tempo_em_segundos = data["total_duration"] / 1_000_000_000
    print(f"resumo gerado! \n tempo de duração: {tempo_em_segundos}")
    return data['response']
    # # a resposta e por varais linhas e o json nao consgeu lidar com esse tipo de stream, enao vamos pegar linha a linhas
    # for line in response.iter_lines():
    #     data = json.loads(line.decode("utf-8")) 
    #     if "response" in data:
    #         print(data["response"], end='', flush=True)

# -- opçoes de criaçõ com resumo
def search_create(prompt):
    btn = input("voce quer usar o resumo ?") # mais pra frente vai ser ua opção avulsa par usar qualqer resumo
    if btn == "":
        tipo_prompt_user = input("""
        Digite o voce quer fazer apartir do resumo:

        1 - aprofundar o resumo - vai buscar fontes, completar o assunto e gerar mais conteudo - tempo de resposta lento 
        2 - gerar flashcards - vai pegar o resumo e apartir dele criar flash cards (txts,txt,readme.md,notion,pdf) # add um if a mais dps - tempo de resposta medio
        3 - gerar apostila - vai gerar uma apostila buscando o tema, com tutoriais, e questoes (pdf, reade.md, notion) - tempo de resposta lento 
        4 - transforar em audiobook - pega o resumo escolhido e tranforma em audiobook - tempo de resposta lento
        5 - 

        """).strip() # tratando de forma facil
        opcoes = {"1" : "prompt1",
                  "2" : "prompt2",
                  "3" : "prompt5",
                  "4" : "prompt6",
                  "5" : "prompt7" } 
        if tipo_prompt_user in opcoes: # se existir a opção
            prompt = opcoes[tipo_prompt_user]
    else:
        btn = input("tem certeza? (mostra resumo)") # messaboz com cancel ok ou nao

        return btn 

main()
