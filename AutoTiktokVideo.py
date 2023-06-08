import moviepy
import speech_recognition as sr

recognizer = sr.Recognizer()

from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.editor import AudioFileClip, CompositeAudioClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

video_name = input("Video file name (video must be inside auto video folder): ")
duration = int(input("Enter clip duration: "))
reps = int(input("Enter the number of clips you want: "))
add_text = input("Add text?(y/n): ")

if (add_text == 'y'):

    input_text = input("Enter text: ")
    font = input("Enter font(ex:Arial): ")
    font_color = input('Enter color(ex:white): ')
    size = int(input('Enter size: '))
    x = int(input("Enter X position: "))
    y = int(input("Enter Y position: "))
add_subs = input("Add subtitles?(y/n): ")

if (add_subs == 'y'):

    sub_font = input("Enter font(ex:Arial): ")
    sub_color = input('Enter color(ex:white): ')
    sub_size = int(input('Enter size: '))
    sub_x = int(input("Enter X position: "))
    sub_y = int(input("Enter Y position: "))
    word_count = int(input("How many words per line: "))
    text_duration = int(input("How many seconds the subtitles will be shown: "))

merge_audio = input("Merge audio with music?(y/n): ")

if (merge_audio == 'y'):
    m_audio = input("Audio file name (must be inside auto video folder): ")

resize = input("Resize the video(y/n): ")

if (resize == 'y'):
    resize_height = input("Enter height(recommended 1920): ")
    resize_width = input("Enter width(recommended 1080): ")

crop = input("Crop video(y/n): ")

crop_size = [1, 1]

if (crop == 'y'):
    crop_size[0] = int(input("Enter height(recommended 1920): "))
    crop_size[1] = int(input("Enter width(recommended 1080): "))

input_video = VideoFileClip(video_name)
video_duration = input_video.duration

clip_number = int(video_duration // duration)

if (clip_number > reps):
    clip_number = reps

print(str(clip_number), "clips will be created")

for i in range(clip_number):

    start_time = i * duration
    end_time = (i + 1) * duration
    chunk = input_video.subclip(start_time, end_time)
    chunk.audio.write_audiofile("audio.wav")

    if (add_text == 'y'):
        texts = TextClip(input_text, fontsize=size, color=font_color, font=font)
        texts = texts.set_position((x, y))
        
    if (add_subs == 'y'):

        with sr.AudioFile("audio.wav") as source:
            audio = recognizer.record(source)

        audio_text = recognizer.recognize_google(audio)
        words = audio_text.split()
        start_time = 0
        end_time = text_duration

        for ii in range(0, len(words), word_count):
            group = words[ii:ii+word_count]
            text = TextClip(' '.join(group), fontsize=sub_size, color=sub_color, font=sub_font)
            text = text.set_position((sub_x, sub_y))
            text = text.set_start(start_time).set_end(end_time)
        
            chunk = CompositeVideoClip([chunk, text])
            start_time += text_duration
            end_time += text_duration  

    if (add_text == 'y'):
        chunk = CompositeVideoClip([chunk, texts])
    
    if (merge_audio == 'y'):

        audio1 = AudioFileClip("audio.wav")
        audio2 = AudioFileClip(m_audio)

        audio2 = audio2.set_duration(audio1.duration)
        merged_audio = CompositeAudioClip([audio1, audio2])
        chunk = chunk.set_audio(merged_audio)

    if (resize == 'y'):
        new_resolution = (resize_width, resize_height)
        chunk = chunk.resize(new_resolution)

    if (crop == 'y'):
        chunk = chunk.crop(x1=(chunk.size[0] / 2) - (crop_size[1] / 2), y1=(chunk.size[1] / 2) - (crop_size[0] / 2), x2=(chunk.size[0] / 2) + (crop_size[1] / 2), y2=(chunk.size[1] / 2) + (crop_size[0] / 2))

    chunk.duration = duration
    chunk.write_videofile(f"chunk_{i+1}.mp4")