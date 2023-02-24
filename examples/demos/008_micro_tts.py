'''
After you've set your subscription key, run this application from your working
directory with this command: python TTSSample.py
'''
from xml.etree import ElementTree

import requests
import time

'''
If you prefer, you can hardcode your subscription key as a string and remove
the provided conditional statement. However, we do recommend using environment
variables to secure your subscription keys. The environment variable is
set to SPEECH_SERVICE_KEY in our sample.
For example:
subscription_key = "Your-Key-Goes-Here"
'''


# if 'SPEECH_SERVICE_KEY' in os.environ:
#     subscription_key = os.environ['SPEECH_SERVICE_KEY']
# else:
#     print('Environment variable for your subscription key is not set.')
#     exit()


class TextToSpeech(object):

    def __init__(self, subscription_key, text="打开空调"):
        self.subscription_key = subscription_key
        self.tts = text
        # self.tts = input("What would you like to convert to speech: ")
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''

    def get_token(self):
        fetch_token_url = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken"  # 终结点
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
        print("access_token = " + self.access_token)

    def save_audio(self):
        # ShortName = 'zh-CN-XiaoxiaoNeural'  # 每月 5000个 字符免费
        ShortName = 'zh-CN-YunyangNeural'  # 每月 5000个 字符免费
        # ShortName = 'zh-CN-Yaoyao-Apollo' # 每月 500 万个字符免费

        base_url = 'https://southeastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', ShortName)  # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        # voice.text = self.tts
        # add by wdc
        prosody = ElementTree.SubElement(voice, 'prosody')
        # rate="20%" pitch="0%"
        prosody.set("rate", "0%")
        prosody.set("pitch", "0%")
        # end add by wdc
        prosody.text = self.tts
        body = ElementTree.tostring(xml_body)
        print(body)

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(
                response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")


if __name__ == "__main__":
    subscription_key = '25a46949ecab415a81a0b0632763437d'
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.save_audio()
