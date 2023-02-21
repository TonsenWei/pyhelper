import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices)
print("voices length = " + str(len(voices)))
# texts = '''今天我，寒夜里看雪飘过​怀着冷却了的心窝漂远方​风雨里追赶，雾里分不清影踪​天空海阔你与我​可会变（谁没在变）​多少次，迎着冷眼与嘲笑​从没有放弃过心中的理想​一刹那恍惚， 若有所失的感觉​不知不觉已变淡​心里爱（谁明白我）​原谅我这一生不羁放纵爱自由​也会怕有一天会跌倒​背弃了理想 ，谁人都可以​哪会怕有一天只你共我'''
# 0：汉语女声；1：英语男声；2：英语女声；3：日语女声；4：韩语女声；5：英语女声；6：粤语女声；7：台语女声
texts = "你好世界"
voices = engine.setProperty('voice', voices[0].id)
engine.say(texts)
"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()