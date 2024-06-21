import os
import telebot
from pytube import YouTube
from moviepy.editor import AudioFileClip

# Fetch the bot token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Function to download video
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_file = stream.download()
        return video_file
    except Exception as e:
        print(e)
        return None

# Function to convert video to mp3
def convert_video_to_mp3(video_file):
    try:
        base, ext = os.path.splitext(video_file)
        mp3_file = base + '.mp3'

        audio_clip = AudioFileClip(video_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        return mp3_file
    except Exception as e:
        print(e)
        return None

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"សូមស្វាគមន៍🙏🏻 {message.from_user.full_name} មកកាន់ YTKhmerBlood🇰🇭🩸 កម្មវិធីទាញយក YouTube ។ សូមផ្ញើតំណ Link វីដេអូ YouTube មកកាន់ខ្ញុំ ហើយខ្ញុំនឹងទាញយកវាសម្រាប់អ្នក។")

# Handler for receiving messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        bot.reply_to(message, "កំពុងដំណើរការសំណើរបស់អ្នក⚙️។ ⏱សូមរង់ចាំ...!")

        video_file = download_youtube_video(url)
        if video_file:
            bot.send_video(message.chat.id, open(video_file, 'rb'), caption="ទាញយកដោយ YTKhmerBlood🇰🇭🩸                                                                                                 Developer  @Kheng_Chetra")
            bot.send_message(message.chat.id,"កុំពុងបំលែងវីដេអូទៅជា MP3🎵។​ ⏱សូមរង់ចាំ...!")

            mp3_file = convert_video_to_mp3(video_file)
            if mp3_file:
                bot.send_audio(message.chat.id, open(mp3_file, 'rb'), caption="MP3🎵")
                os.remove(mp3_file)
                bot.send_message(message.chat.id,"🙏🏻សូមអគុណ!/🙏🏻Thank You!")
            os.remove(video_file)
        else:
            bot.reply_to(message, "បរាជ័យក្នុងការទាញយកវីដេអូ❌។")
    else:
        bot.reply_to(message, "សូមផ្ញើតំណ​ Link YouTube ឲ្យបានត្រឹមត្រូវ✅។")

# Start the bot
bot.polling()
