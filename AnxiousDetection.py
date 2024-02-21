from aiogram import Bot, Dispatcher, types
from aiogram import executor
from videoai.videoAi import VideoAI
from textai.textAI import TextAI
from audioai.audioAI import AudioAI


API_TOKEN = '6689449158:AAHfmHeuYvi3VOL_v0FWRQR6df5bnw4vXvs'

# logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
emotions = {'Text': None, 'Audio': None, 'Video': None}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Send the welcome message
    await message.answer(
        """Привет! Я помогу вам определить уровень тревожности на основе ваших эмоций.\n\n
Для этого опишите свое состояние текстом, отправьте голосовое сообщение, видео, и я вам помогу. Жду вашего обращения!"
        """
    )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    await bot.send_message(message.chat.id, 'Анализ текста. Пожалуйста, подождите...')
    text = message.text
    text_model = TextAI()
    emotional_state = text_model.predict(text)
    emotions['Text'] = emotional_state
    msg = ''
    if emotions['Audio'] == None:
        msg += ' Аудио'
    if emotions['Video'] == None:
        msg += ' Видео'
    
    if msg:
        await bot.send_message(message.chat.id, 'Состояние по тексту получено. Теперь отправьте' + msg)
    else:
        anx = 0
        negative_states = []
        for i, j in emotions.items():
            if j in 'Negative Fear Angry Surprise Sad':
                anx += 1
                negative_states.append(i)
            emotions[i] = None
        if anx == 2:
            await bot.send_message(message.chat.id, '''
По результатам, у вас может быть небольшая тревожность. 
                                
Сейчас важно обратить внимание на свое самочувствие и принять несколько мер 
для улучшения эмоционального состояния. 
Возможно, стоит выделить время на занятия, которые приносят вам удовольствие и расслабление, такие как медитация, йога, прогулки на свежем воздухе или чтение. 
Также важно обратить внимание на свой образ жизни: регулярное питание, достаточный сон и здоровый образ жизни могут помочь справиться с негативными эмоциями и уменьшить тревожность. 

Если тревожность сохраняется или усиливается, обратитесь за поддержкой к профессионалу, такому как психолог или терапевт, который поможет вам разобраться в ваших чувствах и найти эффективные стратегии решения проблемы.
                ''')
        if anx == 3:
            await bot.send_message(message.chat.id, '''
По результатам всех анализов, у вас обнаруживается негативное состояние.
                                   
Большая вероятность, что у вас тревожность. 
Если это так, то вам следует немедленно обратить внимание на свое эмоциональное состояние. 
Важно сначала признать свои чувства и дать себе разрешение на то, чтобы чувствовать их. 
Затем попробуйте применить стратегии самоуспокоения, такие как глубокое дыхание, медитация или практика мускульного расслабления. 

Один из способов справиться с тревожностью может быть и поиск поддержки у близких людей или профессионального психолога. 
Важно найти способы разгрузиться и обсудить свои чувства, а также обратить внимание на свой образ жизни: регулярные физические упражнения, здоровое питание и достаточный сон могут помочь справиться с негативными эмоциями и тревожностью. 
Не стесняйтесь обратиться за помощью, если ощущаете, что не можете справиться с этим самостоятельно. 
                                   
Заботьтесь о себе!"
''')
@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_text(message: types.Message):
    await bot.send_message(message.chat.id, 'Анализ голоса. Пожалуйста, подождите...')
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
    emotional_state = audio_model.predict(voice_file_path)

    emotions['Audio'] = emotional_state
    msg = ''
    if emotions['Text'] == None:
        msg += ' Текст'
    if emotions['Video'] == None:
        msg += ' Видео'
    
    if msg:
        await bot.send_message(message.chat.id, 'Состояние по голосу получено. Теперь отправьте' + msg)
    else:
        anx = 0
        negative_states = []
        for i, j in emotions.items():
            if j in 'Negative Fear Angry Surprise Sad':
                anx += 1
                negative_states.append(i)
            emotions[i] = None
        if anx == 2:
            await bot.send_message(message.chat.id, '''
По результатам, у вас может быть небольшая тревожность. 
                                
Сейчас важно обратить внимание на свое самочувствие и принять несколько мер 
для улучшения эмоционального состояния. 
Возможно, стоит выделить время на занятия, которые приносят вам удовольствие и расслабление, такие как медитация, йога, прогулки на свежем воздухе или чтение. 
Также важно обратить внимание на свой образ жизни: регулярное питание, достаточный сон и здоровый образ жизни могут помочь справиться с негативными эмоциями и уменьшить тревожность. 

Если тревожность сохраняется или усиливается, обратитесь за поддержкой к профессионалу, такому как психолог или терапевт, который поможет вам разобраться в ваших чувствах и найти эффективные стратегии решения проблемы.
''')
        if anx == 3:
            await bot.send_message(message.chat.id, '''
По результатам всех анализов, у вас обнаруживается негативное состояние.
                                   
Большая вероятность, что у вас тревожность. 
Если это так, то вам следует немедленно обратить внимание на свое эмоциональное состояние. 
Важно сначала признать свои чувства и дать себе разрешение на то, чтобы чувствовать их. 
Затем попробуйте применить стратегии самоуспокоения, такие как глубокое дыхание, медитация или практика мускульного расслабления. 

Один из способов справиться с тревожностью может быть и поиск поддержки у близких людей или профессионального психолога. 
Важно найти способы разгрузиться и обсудить свои чувства, а также обратить внимание на свой образ жизни: регулярные физические упражнения, здоровое питание и достаточный сон могут помочь справиться с негативными эмоциями и тревожностью. 
Не стесняйтесь обратиться за помощью, если ощущаете, что не можете справиться с этим самостоятельно. 
                                   
Заботьтесь о себе!"
''')

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    # Get the video file ID
    await bot.send_message(message.chat.id, 'Анализ видео. Пожалуйста, подождите...')
    video_file_id = message.video.file_id

    # Get the video file path
    video_file_path = 'videoai/video_files/file.mp4'

    # Download the video file
    video_file = await bot.download_file_by_id(video_file_id)

    # Save the video file locally
    with open(video_file_path, 'wb') as f:
        f.write(video_file.read())


    video_model = VideoAI()
    predictions = []
    video_model.predict(video_file_path, predictions)
    negative =  0
    for i in predictions:
        if i == 'neutral':
            continue
        elif i in 'fear angry surprise sad':
            negative += 1
        else:
            negative -= 1
    if negative:
        emotions['Video'] = 'Negative'

    msg = ''
    if emotions['Text'] == None:
        msg += ' Текст'
    if emotions['Audio'] == None:
        msg += ' Аудио'
    
    if msg:
        await bot.send_message(message.chat.id, 'Состояние по видео получено. Теперь отправьте' + msg)
    else:
        anx = 0
        negative_states = []
        for i, j in emotions.items():
            if j in 'Negative fear angry surprise sad':
                anx += 1
                negative_states.append(i)
            emotions[i] = None
        if anx == 2:
            await bot.send_message(message.chat.id, '''
По результатам, у вас может быть небольшая тревожность. 
                                
Сейчас важно обратить внимание на свое самочувствие и принять несколько мер 
для улучшения эмоционального состояния. 
Возможно, стоит выделить время на занятия, которые приносят вам удовольствие и расслабление, такие как медитация, йога, прогулки на свежем воздухе или чтение. 
Также важно обратить внимание на свой образ жизни: регулярное питание, достаточный сон и здоровый образ жизни могут помочь справиться с негативными эмоциями и уменьшить тревожность. 

Если тревожность сохраняется или усиливается, обратитесь за поддержкой к профессионалу, такому как психолог или терапевт, который поможет вам разобраться в ваших чувствах и найти эффективные стратегии решения проблемы.
''')
        if anx == 3:
            await bot.send_message(message.chat.id, '''
По результатам всех анализов, у вас обнаруживается негативное состояние.
                                   
Большая вероятность, что у вас тревожность. 
Если это так, то вам следует немедленно обратить внимание на свое эмоциональное состояние. 
Важно сначала признать свои чувства и дать себе разрешение на то, чтобы чувствовать их. 
Затем попробуйте применить стратегии самоуспокоения, такие как глубокое дыхание, медитация или практика мускульного расслабления. 

Один из способов справиться с тревожностью может быть и поиск поддержки у близких людей или профессионального психолога. 
Важно найти способы разгрузиться и обсудить свои чувства, а также обратить внимание на свой образ жизни: регулярные физические упражнения, здоровое питание и достаточный сон могут помочь справиться с негативными эмоциями и тревожностью. 
Не стесняйтесь обратиться за помощью, если ощущаете, что не можете справиться с этим самостоятельно. 
                                   
Заботьтесь о себе!"
''')
        emotions.clear()
@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video(message: types.Message):
    # Get the video file ID
    await bot.send_message(message.chat.id, 'Анализ видео. Пожалуйста, подождите...')
    video_file_id = message.video_note.file_id

    # Get the video file path
    video_file_path = 'videoai/video_files/file.mp4'

    # Download the video file
    video_file = await bot.download_file_by_id(video_file_id)

    # Save the video file locally
    with open(video_file_path, 'wb') as f:
        f.write(video_file.read())


    video_model = VideoAI()
    predictions = []
    video_model.predict(video_file_path, predictions)
    negative =  0
    for i in predictions:
        if i == 'neutral':
            continue
        elif i in 'fear angry surprise sad':
            negative += 1
        else:
            negative -= 1
    if negative:
        emotions['Video'] = 'Negative'

    msg = ''
    if emotions['Text'] == None:
        msg += ' Текст'
    if emotions['Audio'] == None:
        msg += ' Аудио'
    
    if msg:
        await bot.send_message(message.chat.id, 'Состояние по видео получено. Теперь отправьте' + msg)
    else:
        anx = 0
        negative_states = []
        for i, j in emotions.items():
            if j in 'Negative fear angry surprise sad':
                anx += 1
                negative_states.append(i)
            emotions[i] = None
        if anx == 2:
            await bot.send_message(message.chat.id, '''
По результатам, у вас может быть небольшая тревожность. 
                                
Сейчас важно обратить внимание на свое самочувствие и принять несколько мер 
для улучшения эмоционального состояния. 
Возможно, стоит выделить время на занятия, которые приносят вам удовольствие и расслабление, такие как медитация, йога, прогулки на свежем воздухе или чтение. 
Также важно обратить внимание на свой образ жизни: регулярное питание, достаточный сон и здоровый образ жизни могут помочь справиться с негативными эмоциями и уменьшить тревожность. 

Если тревожность сохраняется или усиливается, обратитесь за поддержкой к профессионалу, такому как психолог или терапевт, который поможет вам разобраться в ваших чувствах и найти эффективные стратегии решения проблемы.
''')
        if anx == 3:
            await bot.send_message(message.chat.id, '''
По результатам всех анализов, у вас обнаруживается негативное состояние.
                                   
Большая вероятность, что у вас тревожность. 
Если это так, то вам следует немедленно обратить внимание на свое эмоциональное состояние. 
Важно сначала признать свои чувства и дать себе разрешение на то, чтобы чувствовать их. 
Затем попробуйте применить стратегии самоуспокоения, такие как глубокое дыхание, медитация или практика мускульного расслабления. 

Один из способов справиться с тревожностью может быть и поиск поддержки у близких людей или профессионального психолога. 
Важно найти способы разгрузиться и обсудить свои чувства, а также обратить внимание на свой образ жизни: регулярные физические упражнения, здоровое питание и достаточный сон могут помочь справиться с негативными эмоциями и тревожностью. 
Не стесняйтесь обратиться за помощью, если ощущаете, что не можете справиться с этим самостоятельно. 
                                   
Заботьтесь о себе!"
''')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
