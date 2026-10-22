import asyncio
import tempfile
import traceback
import wave
from pathlib import Path
import aiohttp
import bale
import lameenc
from piper import PiperVoice
import emoji

TOKEN = "...."

client = bale.Bot(TOKEN)

CHANNEL_ID = "@farsireader"
CHANNEL_URL = "https://ble.ir/farsireader"


def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")
def subscription_keyboard():
    keyboard = bale.InlineKeyboardMarkup()

    keyboard.add(
        bale.InlineKeyboardButton(
            "📢 کانال فارسی‌خوان",
            url=CHANNEL_URL,
        ),
        row=1,
    )

    keyboard.add(
        bale.InlineKeyboardButton(
            "عضو شدم ✅",
            callback_data="check_channel",
        ),
        row=2,
    )

    return keyboard


async def send_channel_prompt(message):
    await message.reply(
        "سلام! به فارسی‌خوان خوش اومدی. 🎀🎧\n\n"
        "اینجا می‌تونی متن‌های فارسی رو به فایل صوتی تبدیل کنی.\n\n"
        "برای باخبر شدن از قابلیت‌های جدید، به‌روزرسانی‌ها "
        "و امکاناتی که به‌مرور به فارسی‌خوان اضافه می‌شن، "
        "می‌تونی کانال ما رو هم دنبال کنی. 🌸\n\n"
        "برای شروع، اول عضویتت در کانال رو تأیید کن. 💗",
        components=subscription_keyboard(),
    )

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Mana-Persian-Piper" / "fa_IR-mana-medium.onnx"

import json

PRONUNCIATIONS_FILE = BASE_DIR / "pronunciations.json"


def load_pronunciations():
    if not PRONUNCIATIONS_FILE.exists():
        return {"pronunciations": {}}

    try:
        with open(PRONUNCIATIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not read pronunciations.json")
        return {"pronunciations": {}}


def save_pronunciation(original, pronunciation):
    data = load_pronunciations()

    data["pronunciations"][original] = pronunciation

    with open(PRONUNCIATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def apply_pronunciations(text):
    data = load_pronunciations()

    for original, pronunciation in data["pronunciations"].items():
        text = text.replace(original, pronunciation)

    return text



tts = PiperVoice.load(str(MODEL_PATH))
print("Persian Piper model loaded successfully!")

waiting_users = set()
teaching_users = {}

def text_to_mp3(text: str, temp_dir: str) -> Path:
    wav_path = Path(temp_dir) / "persian_audio.wav"
    mp3_path = Path(temp_dir) / "persian_speech.mp3"

    with wave.open(str(wav_path), "wb") as wav_file:
        tts.synthesize_wav(text, wav_file)

    with wave.open(str(wav_path), "rb") as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        sample_width = wav_file.getsampwidth()
        pcm_data = wav_file.readframes(wav_file.getnframes())

    if sample_width != 2:
        raise ValueError(f"Expected 16-bit audio, got {sample_width * 8}-bit")

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(channels)
    encoder.set_quality(2)

    mp3_path.write_bytes(encoder.encode(pcm_data) + encoder.flush())
    return mp3_path


@client.listen("on_ready")
async def on_ready():
    print("Persian Voice Bot is running! 🎀")

async def send_voice(chat_id: int, audio_bytes: bytes, caption: str):
    url = f"https://tapi.bale.ai/bot{TOKEN}/sendVoice"

    form = aiohttp.FormData()
    form.add_field("chat_id", str(chat_id))
    form.add_field("caption", caption)
    form.add_field(
        "voice",
        audio_bytes,
        filename="persian_speech.mp3",
        content_type="audio/mpeg",
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form) as resp:
            body = await resp.text()
            if resp.status != 200:
                raise RuntimeError(f"sendVoice failed: {resp.status} {body}")
@client.listen("on_message")
async def on_message(message: bale.Message):
    if not message.author or not message.content:
        return

    user_id = message.author.id
    text = message.content.strip()
    
    if text in ("/teach", "/correct"):
        teaching_users[user_id] = {"step": "original"}
        waiting_users.discard(user_id)

        await message.reply(
            "بیاید تلفظ‌های منو درست کنید 🎀\n\n"
            "اگه کلمه‌ای که تو ویس شنیدین به نظرتون اشکال تلفظی داشتم شما می‌تونین اینجا به من درستش یاد بدید \nکلمه ای اشتباه تلفظی داره رو وارد کنید"
            "برای لغو /cancel\n\n"
        )
        return

    if user_id in teaching_users:
        if text == "/cancel":
            teaching_users.pop(user_id, None)
            await message.reply("یاد دادن لغو شد 🌸")
            return

        if text.startswith("/"):
            await message.reply(
                "Please send the requested text or /cancel."
            )
            return

        state = teaching_users[user_id]

        if state["step"] == "original":
            state["original"] = text
            state["step"] = "pronunciation"

            await message.reply(
                "لطفا تلفظ درستش رو برام بفرستید "
                "که بتونم اصلاحش کنم"
            )
            return

        original = state["original"]
        pronunciation = text

        if original == pronunciation:
            await message.reply(
                "تلفظ مشابه تلفظ اصلی بود "
                "Please try /teach again."
            )
            teaching_users.pop(user_id, None)
            return

        save_pronunciation(original, pronunciation)
        teaching_users.pop(user_id, None)

        await message.reply(
            "با تشکر از شما به خاطراصلاح تلفظ 🎀 "
            "توی حافظه‌ ثبت شد."
        )
        return

    
    if text == "/start":
        waiting_users.discard(user_id)
        await send_channel_prompt(message)
        return


    if text == "/cancel":
        waiting_users.discard(user_id)
        await message.reply("عملیات لغو شد. 🌸 برای شروع دوباره /start را بزنید.")
        return

    if user_id not in waiting_users:
        return

    if text.startswith("/"):
        await message.reply("لطفاً یک پاراگراف فارسی بفرستید یا /cancel را بزنید.")
        return

    waiting_users.discard(user_id)
    await message.reply("متنتان دریافت شد! دارم صدا را می‌سازم... 🎧")


    try:
        corrected_text = apply_pronunciations(text)
        clean_text = remove_emojis(text)
        corrected_text = apply_pronunciations(clean_text)
        with tempfile.TemporaryDirectory() as temp_dir:
            mp3_path = await asyncio.to_thread(
                text_to_mp3, corrected_text, temp_dir
            )
            audio_bytes = mp3_path.read_bytes()

            await client.send_audio(
                chat_id=message.chat.id,
                audio=bale.InputFile(
                    audio_bytes,
                    file_name="persian_speech.mp3",
                ),
                caption="صدای متن شما آماده است! 🎀",
            )

        print(f"Audio file sent to user {user_id}")

    except Exception as error:
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")
        traceback.print_exc()
        await message.reply(
            "متأسفانه مشکلی پیش آمد. لطفاً دوباره امتحان کنید. 🌸"
        )


@client.listen("on_callback")
async def on_callback(callback: bale.CallbackQuery):
    if callback.data != "check_channel":
        return

    if not callback.from_user or not callback.message:
        return

    user_id = callback.from_user.id

    try:
        member = await client.get_chat_member(
            CHANNEL_ID,
            user_id,
        )

    except Exception as error:
        print(f"Membership check failed: {error}")

        await callback.message.reply(
            "فعلاً نتونستم عضویتت رو بررسی کنم. 🌸\n"
            "لطفاً کمی بعد دوباره امتحان کن."
        )
        return

    if member and member.status in {
        "member",
        "administrator",
        "creator",
    }:
        waiting_users.add(user_id)

        await callback.message.reply(
            "سلام! 🎀 به ربات تبدیل متن فارسی به صدا خوش آمدید.\n\n"
            "لطفاً پاراگراف فارسی خود را ارسال کنید تا آن را "
            "به فایل صوتی MP3 تبدیل کنم. 🎧"
        )

    else:
        await callback.message.reply(
            "هنوز عضویتت در کانال تأیید نشده. 🌸\n\n"
            "اگه عضو شدی، دوباره روی «عضو شدم ✅» بزن.",
            components=subscription_keyboard(),
        )

client.run()