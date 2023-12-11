import logging
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from videoai.videoAi import VideoAI
from textai.textAI import TextAI
from audioai.audioAI import AudioAI

API_TOKEN = '6689449158:AAHfmHeuYvi3VOL_v0FWRQR6df5bnw4vXvs'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Create an InlineKeyboardMarkup with three buttons
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton("Text", callback_data='text'),
        types.InlineKeyboardButton("Audio", callback_data='audio'),
        types.InlineKeyboardButton("Video/Photo", callback_data='video'),
    ]
    keyboard.add(*buttons)

    # Send the welcome message with the InlineKeyboardMarkup
    await message.answer(
        "Welcome to Emotion Detection Bot. This bot detects emotion from text, audio, and video. "
        "Use one of the buttons below:",
        reply_markup=keyboard
    )

# Handler for InlineKeyboardButton callbacks
@dp.callback_query_handler(lambda c: c.data in {'text', 'audio', 'video'})
async def process_callback(callback_query: types.CallbackQuery):
    action = callback_query.data

    # Ask the user to send a specific type of message based on the chosen action
    if action == 'text':
        await bot.send_message(callback_query.from_user.id, "Please send me a text message.")
    elif action == 'audio':
        await bot.send_message(callback_query.from_user.id, "Please send me a voice message.")
    elif action == 'video':
        await bot.send_message(callback_query.from_user.id, "Please send me a photo, a video, or video message.")

# Handler for text messages
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    await bot.send_message(message.chat.id, 'Analyzing your text. Please wait...')
    text = message.text
    text_model = TextAI()
    emotional_state = text_model.predict(text)
    await message.reply(f"Emotion detected from the provided text. Your emotional state is {emotional_state}")

# Handler for audio messages
@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_audio(message: types.Message):
    await bot.send_message(message.chat.id, 'Analyzing your voice. Please wait...')
    # Get the voice file ID
    voice_file_id = message.voice.file_id

    # Get the voice file path
    voice_file_path = 'audioai/audio_files/file.ogg'

    # Download the voice file
    voice_file = await bot.download_file_by_id(voice_file_id)

    # Save the voice file locally
    with open(voice_file_path, 'wb') as f:
        f.write(voice_file.read())

    # await message.reply("Voice message saved. Emotion detected from the provided voice message.")
    audio_model = AudioAI()
    emotion = audio_model.predict(voice_file_path)

    await message.reply(f"Emotion detected from the provided voice message. Your emotion is {emotion.upper()}")

# Handler for video messages

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    # Get the video file ID
    await bot.send_message(message.chat.id, 'Analyzing your video. Please wait...')
    video_file_id = message.video.file_id

    # Get the video file path
    video_file_path = 'videoai/video_files/file.mp4'

    # Download the video file
    video_file = await bot.download_file_by_id(video_file_id)

    # Save the video file locally
    with open(video_file_path, 'wb') as f:
        f.write(video_file.read())


    video_model = VideoAI()
    video_model.predict(video_file_path)
    output = "videoai/video_files/output.mp4"
    await bot.send_video(chat_id=message.chat.id, video=types.InputFile(output), caption="Emotion detected from the provided video.")
    await bot.send_message(message.chat.id, "if the video is not playing, try to save it on your device, then open from gallery.")


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video(message: types.Message):
    # Get the video file ID
    await bot.send_message(message.chat.id, 'Analyzing your video. Please wait...')
    video_file_id = message.video_note.file_id

    # Get the video file path
    video_file_path = 'videoai/video_files/file.mp4'

    # Download the video file
    video_file = await bot.download_file_by_id(video_file_id)

    # Save the video file locally
    with open(video_file_path, 'wb') as f:
        f.write(video_file.read())


    video_model = VideoAI()
    video_model.predict(video_file_path)
    output = "videoai/video_files/output.mp4"
    await bot.send_video_note(chat_id=message.chat.id, video_note=types.InputFile(output))
    await bot.send_message(message.chat.id, "if the video is not playing, try to save it on your device, then open from gallery.")

# Handler for photo messages
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    await bot.send_message(message.chat.id, 'Analyzing your photo. Please wait...')
    # Get the photo file ID
    photo_file_id = message.photo[-1].file_id

    # Get the photo file path
    photo_file_path = "videoai/video_files/file.jpg"

    # Download the photo file
    photo_file = await bot.download_file_by_id(photo_file_id)

    # Save the photo file locally
    with open(photo_file_path, 'wb') as f:
        f.write(photo_file.read())

    photo_model = VideoAI()
    photo_model.predict(photo_file_path)
    output = "videoai/video_files/output.mp4"
    await bot.send_photo(message.chat.id, photo=types.InputFile(output), caption="Emotion detected from the provided photo.")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
