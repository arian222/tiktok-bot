# ALECS TikTok Bot

Un bot automatizat pentru TikTok cu interfață grafică, creat de ALECS.

## Caracteristici

- Interfață grafică modernă și intuitivă
- Suport pentru Views, Hearts și Followers
- Gestionare automată a CAPTCHA
- Delay-uri configurabile
- Număr de acțiuni configurabil
- Logging detaliat
- Salvare automată de screenshot-uri în caz de erori

## Cerințe

```bash
Python 3.8+
Google Chrome
```

## Instalare

1. Clonați repository-ul:
```bash
git clone https://github.com/yourusername/tiktok-bot.git
cd tiktok-bot
```

2. Instalați dependențele:
```bash
pip install selenium==4.9.1
pip install selenium-stealth==1.0.6
pip install webdriver-manager==3.8.6
pip install customtkinter
pip install Pillow
```

## Utilizare

1. Rulați scriptul:
```bash
python TIKTOKFULL.py
```

2. Introduceți URL-ul videoclipului TikTok
3. Selectați tipul de acțiune (Views/Hearts/Followers)
4. Setați intervalul de delay (în secunde)
5. Opțional: specificați numărul de acțiuni
6. Apăsați "Start Bot"

## Configurare

- Delay minim implicit: 30 secunde
- Delay maxim implicit: 60 secunde
- Număr de încercări pentru fiecare acțiune: 3
- Logging salvat în: tiktok_bot.log

## Note

- Nu închideți fereastra Chrome manual
- Rezolvați CAPTCHA manual când apare
- Pentru oprire sigură, folosiți butonul "Stop Bot"
- Screenshot-urile de eroare sunt salvate în directorul curent

## Autor

ALECS © 2024

## Licență

Acest proiect este licențiat sub MIT License. #   t i k t o k - b o t  
 #   t i k t o k - b o t  
 