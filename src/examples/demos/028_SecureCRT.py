# $language = "python"
# $interface = "1.0"
import time


def Main():
    crt.Screen.Synchronous = True
    while(True):
        crt.Screen.Send("echo 'skintheme:json:{\"skin\":0,\"theme\":1}' >> /pps/foryou/ivi/status" + chr(13))
        time.sleep(10)
        theme1 = "echo 'skintheme:json:{\"skin\":0,\"theme\":"
        theme1_end = "}' >> /pps/foryou/ivi/status"
        for i in range(17):
            crt.Screen.Send(theme1 + str(i) + theme1_end + chr(13))
            time.sleep(0.5)

Main()
