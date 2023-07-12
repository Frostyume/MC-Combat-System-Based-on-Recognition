import pyaudio
import wave
from aip import AipSpeech
from xpinyin import Pinyin
from pynput.keyboard import Key, Listener

APP_ID = '28600992'
API_KEY = "fXMPWqnvVxAOG4yzIrxvdkob"
SECRET_KEY = "qzPK97vaykOR3fBiGHOG9WwW6GHXzsDA"

CHUNK = 2000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAVE_OUTPUT_FILENAME = "back.wav"


def record(rs):  # 录音，rs代表录音的秒数
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stream.start_stream()
    print("* 开始录音......")

    frames = []
    for i in range(0, int(RATE / CHUNK * rs)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def getSpeak():  # 将识别到的语音转成拼音文本
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    py = Pinyin()

    with open('back.wav', 'rb') as fp:
        wave = fp.read()

    print("* 正在识别......", len(wave))
    result = client.asr(wave, 'wav', 16000, {'dev_pid': 1537})
    print(result)
    if result["err_no"] == 0:
        res = str(result['result'][0])
        pinyin = py.get_pinyin(res, "")
        print(pinyin)
        return pinyin
    else:
        print("没有识别到语音\n", result["err_no"])


def attack(text):  # 根据语音内容释放技能
    if 'huoqiu' in text:  # 只需录音期间说的话中包含关键字即可，技能关键字可自行更改，此处仅作参考，下同
        print("火球")  # 暂以print测试效果
        # 发送释放技能指令给NPC
        # NPC判断是否冷却好，并发回判断结果
        # 根据判断结果，决定是否进行释放技能
    if 'hongzha' in text:
        print("轰炸")
        # 发送释放技能指令给NPC
        # NPC判断是否冷却好，并发回判断结果
        # 根据判断结果，决定是否进行释放技能
    if 'leiji' in text:
        print("雷击")
        # 发送释放技能指令给NPC
        # NPC判断是否冷却好，并发回判断结果
        # 根据判断结果，决定是否进行释放技能
    if 'jingu' in text or 'jinggu' in text:
        print("禁锢")
        # 发送释放技能指令给NPC
        # NPC判断是否冷却好，并发回判断结果
        # 根据判断结果，决定是否进行释放技能
    if 'binzhui' in text or 'bingzhui' in text:
        print("冰锥")
        # 发送释放技能指令给NPC
        # NPC判断是否冷却好，并发回判断结果
        # 根据判断结果，决定是否进行释放技能


def start(key):  # 开始函数，当按下tab键时开始录音并识别，根据识别结果决定是进行普通攻击还是释放大招
    if key == Key.tab:
        record(2)  # 暂定录音时间2s，可按需更改
        text = getSpeak()
        attack(text)


while True:
    with Listener(on_press=start) as listener:
        listener.join()

