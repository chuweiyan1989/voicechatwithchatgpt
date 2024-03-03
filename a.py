import os
# from openai import OpenAI
from openai import OpenAI
import speech_recognition as sr
import logging
import pyttsx3

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client =OpenAI()



wav_num=2
while True:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    logging.info('录音中...')

    with mic as source:
    #降噪
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        with open(f"00{wav_num}.wav", "wb") as f:
        #将麦克风录到的声音保存为wav文件
            f.write(audio.get_wav_data(convert_rate=16000))
            logging.info('录音结束，识别中...')    

            test=sr.AudioFile(f"00{wav_num}.wav")
            with test as source:
                audio = recognizer.record(source)
                type(audio)
                text = recognizer.recognize_sphinx(audio, language='en-US')
                print("你说的是：", text)

            # with sr.Microphone() as source:
            #     print("请说话...")
            #     audio = recognizer.listen(source)
            #     text = recognizer.recognize_google(audio, 'en-US')
            #     print("你说的是：", text)

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="gpt-3.5-turbo",
            )

            # 获取模型的回复文本
            message_content =  response.choices[0].message.content
            print(message_content)
            pyttsx3.speak(message_content)	#文字转语音
            #print(print(response.choices[0].message.content))  # 更具体的的打印
            break
