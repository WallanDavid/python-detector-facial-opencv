# 🤖 Aplicação de Reconhecimento Facial com OpenCV e Dlib

Esta aplicação em Python utiliza as bibliotecas **OpenCV**, **dlib** e **Pillow** para realizar reconhecimento facial em tempo real via webcam. Além da detecção facial, ela oferece funcionalidades como captura de fotos, gravação de vídeos e ajustes de imagem (iluminação, contraste, suavização e modo noturno).

## 📦 Requisitos

- Python 3.x
- opencv-python
- dlib
- pillow

### Instalação das dependências

pip install opencv-python dlib pillow

> Obs: A instalação do `dlib` pode exigir build tools no Windows ou `cmake`/`boost` no Linux.

## ▶️ Como Executar

1. Clone o repositório:
git clone https://github.com/WallanDavid/python-detector-facial-opencv.git

2. Acesse a pasta:
cd python-detector-facial-opencv

3. Execute o script:
python face.py

## 🧠 Funcionalidades

- 📸 **Capturar Foto:** Salva uma imagem da câmera em formato PNG
- 🎥 **Iniciar/Parar Gravação:** Grava um vídeo em tempo real da webcam
- 📷 **Captura Múltipla:** Permite registrar várias fotos em sequência
- 💡 **Ajuste de Iluminação:** Três níveis de luminosidade para o feed da câmera
- 🌗 **Ajuste de Contraste:** Modifique o contraste da imagem ao vivo
- 🌫️ **Filtro de Suavização:** Aplica um blur leve para suavizar imperfeições
- 🌙 **Modo Noturno:** Adapta a imagem para baixa luminosidade

## 🛠️ Sugestões de Melhorias Futuras

- Detecção de múltiplos rostos simultaneamente
- Identificação facial com base em dataset
- Exportação de logs ou fotos para banco de dados
- Integração com reconhecimento de emoções
- Interface gráfica com PyQt ou Tkinter

## 🤝 Contribuições

Contribuições são bem-vindas!  
Você pode abrir uma issue ou enviar um pull request com sugestões, melhorias ou correções.

## 📜 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

## 📫 Contato

**Desenvolvedor:** Wallan David Peixoto  
**Email:** bobwallan2@gmail.com  
**LinkedIn:** https://www.linkedin.com/in/wallanpeixoto
