import imp
import threading
from time import sleep
import pyaudio
import wave


class RecordThread(threading.Thread):

    def __init__(self, audiofile='record.wav'):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.audiofile = audiofile
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

    def run(self):
        audio = pyaudio.PyAudio()
        wavfile = wave.open(self.audiofile, 'wb')
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format,
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        while self.bRecord:
            wavfile.writeframes(wavstream.read(self.chunk))
        wavstream.stop_stream()
        wavstream.close()
        audio.terminate()

    def stoprecord(self):
        self.bRecord = False


if __name__ == "__main__":
    print("record test ...")
    audio_recored = RecordThread("record.wav")
    audio_recored.start()
    sleep(10)
    audio_recored.stoprecord()
    print("done!")
