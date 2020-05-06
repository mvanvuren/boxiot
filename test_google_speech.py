# from google_speech import Speech

# text = "jab, right hand, rolling under left hook, lean away from right hand, left hook, right hand"
# lang = "en-uk"
# speech = Speech(text, lang)
# speech.play()

# # you can also apply audio effects while playing (using SoX)
# # see http://sox.sourceforge.net/sox.html#EFFECTS for full effect documentation
# # sox_effects = ("speed", "0.9")
# # speech.play(sox_effects)

# # save the speech to an MP3 file (no effect is applied)
# speech.save("40.mp3")

from gtts import gTTS
import os
import hashlib

text = 'jab. right hand. rolling under left hook. lean away from right hand. left hook. right hand.'

md5 = hashlib.md5(text.encode())
filename = "{}.mp3".format(md5.hexdigest())
if not os.path.isfile(filename):
    tts = gTTS(text)
    tts.save(filename)

print('exit')
