# 🎀 Persian Voice Bot | فارسی‌خوان

🎧 **Turn Persian text into audio!**

## 🌸 About the Project

Persian Voice Bot (فارسی‌خوان) is a Python-based bot on Bale that converts Persian text into downloadable audio files.

I created this project to make listening to Persian text easier and more accessible. I'm continuously improving it by adding new features and learning from user feedback. 💗

## 🎧 What Does It Do?

Persian Voice Bot allows users to send a Persian paragraph and receive an audio file of the text.

Instead of reading a long paragraph, users can simply listen to it! ✨

## ✨ Features

- 🎙️ **Persian Text-to-Speech:** Converts Persian text into speech.
- 🎵 **MP3 Audio:** Sends the generated speech as a downloadable audio file.
- 🎀 **Emoji Filtering:** Removes emojis before generating speech so they aren't read aloud.
- 🗣️ **Custom Pronunciation Corrections:** Allows users to teach the bot their preferred pronunciation of specific words.
- 🧠 **Saved Corrections:** Stores pronunciation corrections in a JSON file for future use.
- 📢 **Channel Integration:** Keeps users informed about updates and new features.
- 💗 **User-Friendly Interaction:** Provides a simple way to turn Persian paragraphs into audio.

## 🛠️ Technologies Used

- 🐍 **Python** — Main programming language.
- 🤖 **Bale Bot API** — Handles bot messages and user interactions.
- 🔊 **Piper TTS** — Generates Persian speech using a local voice model.
- 🌐 **aiohttp** — Handles asynchronous HTTP requests.
- 🎵 **lameenc** — Converts generated audio into MP3 format.
- 🎀 **emoji** — Detects and removes emojis from text.
- 📄 **JSON** — Stores custom pronunciation corrections.

## 🚀 How to Use It

1. Open Persian Voice Bot on Bale.
2. Join the project channel and confirm your membership.
3. Send a Persian paragraph to the bot.
4. Wait while your text is converted into speech.
5. Receive your audio file and enjoy listening! 🎧

### 💬 Available Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/teach` | Teach the bot a pronunciation correction |
| `/correct` | Start the pronunciation correction process |
| `/cancel` | Cancel the current operation |

### ⚙️ Run It Yourself

1. Clone the repo and install the dependencies:

```bash
git clone https://github.com/amitisy67/Persian-Voice-Bot.git
cd Persian-Voice-Bot
pip install -r requirements.txt
```

2. Download the Persian Piper voice model and put it in a folder named `Mana-Persian-Piper` next to `main.py`. You need both files (they are large, so they are not stored in this repo):
   - `fa_IR-mana-medium.onnx`
   - `fa_IR-mana-medium.onnx.json`

3. Set your Bale bot token as an environment variable (never write a real token in the code):

```bash
# Linux / macOS
export BALE_BOT_TOKEN="your-token-here"

# Windows (PowerShell)
$env:BALE_BOT_TOKEN="your-token-here"
```

4. Start the bot:

```bash
python main.py
```

### 🔗 Try It Out!

- 🤖 **Bot:** https://ble.ir/farsireaderbot
- 📢 **Channel:** https://ble.ir/farsireader

---

💗 *Built with Python, powered by Piper TTS, and made with a little bit of 🎀.*
