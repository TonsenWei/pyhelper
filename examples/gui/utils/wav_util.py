# -*- coding: utf-8 -*-
import pyaudio
import wave
import time


class WavPlayer:
    keep_play = False
    is_stop = True

    def play(self, filepath, timeout=0):
        self.keep_play = True
        self.is_stop = False
        chunk = 1024  # 每次读取帧数
        f = wave.open(filepath, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        # output_device_index = 14,
                        output=True,
                        )
        data = f.readframes(chunk)
        while data and self.keep_play is True:
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.is_stop = True

    def stop(self):
        self.keep_play = False


if __name__ == "__main__":
    wavplayer = WavPlayer()
    wavplayer.play(r"D:\Projects\gitee\pylearning\files\wav_report\xiaoaitongxue.wav")
