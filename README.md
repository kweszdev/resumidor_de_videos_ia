# Resumidor de Videos com IA (v0.1)

## Sobre o Projeto
Este script permite transcrever vídeos do YouTube utilizando o modelo Whisper da OpenAI. Ele suporta aceleração por GPU (se disponível) e pode ser utilizado apenas com CPU, caso desejado. O áudio do vídeo é extraído e convertido para texto, permitindo um resumo do conteúdo.

## Requisitos

- **Python**: Testado no **Python 3.10.11**
- **Pip**: Versão recomendada **25.0.1**
- **FFmpeg**: Necessário para processar o áudio corretamente

## Instalação das Dependências

Execute o seguinte comando para instalar todas as bibliotecas necessárias:

```sh
pip install pytubefix openai-whisper moviepy torch
```

## Observações Importantes

- O **Whisper não funciona no Python 3.13**.
- O **FFmpeg deve estar instalado no sistema** para o processamento de áudio.
- O script requer **alta capacidade de processamento**, memória e conexão com a internet.
- O modelo pode **utilizar a GPU automaticamente** se disponível.
- A API da OpenAI pode ter **limitações de uso** dependendo do plano.
- Durante a execução, **dois arquivos de áudio** serão gerados no diretório:
  - `audio.mp4` (extraído do vídeo)
  - `audio.mp3` (convertido para maior nitidez)

## Como Forçar o Uso da CPU

Se desejar rodar apenas na CPU, **mesmo que a GPU esteja disponível**, utilize o comando abaixo antes de executar o script:

```sh
set CUDA_VISIBLE_DEVICES=
```

Ou execute em um ambiente sem GPU, como uma máquina virtual.

## Próximas Versões

- Adição de uma **interface gráfica**.
- Melhorias na **interface de terminal**.
- Possibilidade de **resumir o texto transcrito** automaticamente.

## Avisos

Durante o carregamento do modelo, alguns avisos podem ser exibidos no terminal. Isso **não afeta o funcionamento do script** e não foram desativados por questão de conveniência.

