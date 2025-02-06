# ALECS TikTok Bot

Un bot automatizat pentru TikTok cu interfață grafică, creat de ALECS.

## Ghid de Instalare Pas cu Pas

### 1. Pregătire Sistem
- Instalați [Python](https://www.python.org/downloads/) (versiunea 3.8 sau mai nouă)
- Instalați [Google Chrome](https://www.google.com/chrome/)
- Asigurați-vă că aveți Git instalat sau descărcați de la [git-scm.com](https://git-scm.com/downloads)

### 2. Descărcarea Proiectului
Aveți două opțiuni:

#### Opțiunea 1: Folosind Git
```bash
# Deschideți Command Prompt sau PowerShell și rulați:
git clone https://github.com/alecs/tiktok-bot.git
cd tiktok-bot
```

#### Opțiunea 2: Descărcare Directă
- Mergeți la [pagina proiectului](https://github.com/alecs/tiktok-bot)
- Click pe butonul verde "Code"
- Selectați "Download ZIP"
- Extrageți arhiva descărcată

### 3. Instalare Dependențe
```bash
# Deschideți Command Prompt sau PowerShell în folderul proiectului și rulați:
pip install -r requirements.txt
```

### 4. Rulare Bot
```bash
python TIKTOKFULL.py
```

## Utilizare

1. După pornirea aplicației, veți vedea interfața grafică
2. Introduceți URL-ul videoclipului TikTok în câmpul dedicat
3. Selectați tipul de acțiune dorit:
   - Views: pentru vizualizări
   - Hearts: pentru like-uri
   - Followers: pentru urmăritori
4. Ajustați timpii de delay (implicit 30-60 secunde)
5. Opțional: specificați numărul de acțiuni dorite
6. Apăsați "Start Bot"

## Configurare

- Delay minim implicit: 30 secunde
- Delay maxim implicit: 60 secunde
- Număr de încercări pentru fiecare acțiune: 3
- Logging salvat în: tiktok_bot.log

## Rezolvare Probleme Comune

1. **Eroare la instalarea dependențelor**
   ```bash
   # Încercați să actualizați pip:
   python -m pip install --upgrade pip
   # Apoi reinstalați dependențele:
   pip install -r requirements.txt
   ```

2. **Chrome nu pornește**
   - Asigurați-vă că aveți Google Chrome instalat
   - Verificați că nu rulați alt bot în același timp

3. **Erori CAPTCHA**
   - Rezolvați manual primul CAPTCHA când apare
   - Nu închideți fereastra Chrome în timpul rulării

4. **Eroare "element not interactable"**
   - Măriți timpul de delay
   - Verificați că URL-ul TikTok este valid

## Note Importante

- Nu închideți manual fereastra Chrome
- Rezolvați CAPTCHA manual când apare
- Pentru oprire sigură, folosiți butonul "Stop Bot"
- Screenshot-urile de eroare sunt salvate automat

## Actualizări

Pentru a obține ultima versiune:
```bash
git pull origin main
```

## Autor

ALECS © 2024

## Suport

Pentru probleme sau întrebări:
- Deschideți un issue pe GitHub
- Verificați secțiunea [Issues](https://github.com/alecs/tiktok-bot/issues) pentru soluții existente

## Licență
Salut! Poți să-mi trimiți bani pe Revolut cu acest link: revolut.me/alecss12
https://wa.me/40732159658?text=Salut!%20Cum%20te%20pot%20ajuta
Acest proiect este licențiat sub MIT License.
