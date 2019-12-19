import os
import time
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess


#FaceAPI

#APIkey
API_KEY = "bf5c18ab3d38470ab0ec42279a943101"
file = "capture.jpg"

def RaadJson(datas):
  emotion = []
  emo = ["anger","contempt","disgust","fear","happiness","sadness","surprise"]
  #anger, contempt, disgust, fear, happiness, sadness and surprise.
  for data in datas:
    #
    f = data["faceAttributes"]
    d = f["emotion"]
    for name in emo:
      emotion.append(d[name])
  return emotion


def Recognize(emotion):
  data = np.array(emotion)
  emo = np.array(["怒り","悔しい","嫌","恐怖","幸せ","悲しい","驚く"])
  print(data)
  num = np.argmax(data)
  pred = "この写真は「" +emo[num] + "」という感情です"
  print(pred)
  #cmd_2 = num
  #cmd_1 = "./node.js"
  #cmd = cmd_1+" "+str(num)
  try:
      if(sum(data) != 0):
          #main.jsのファイルを読み込む
          subprocess.call(f"node main.js {str(num)}", shell=True)
  except ValueError:
      print("google home error")
headers = {
# Request headers
'Content-Type': 'application/octet-stream',
'Ocp-Apim-Subscription-Key': API_KEY,
}

params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion'
})


#画像認識＆ファイル出力
#5秒おきに出力する
T=5

def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    # 処理前の時刻
    t1 = time.time()
    N=0
    while True:
        # 処理後の時刻
        t2 = time.time()
        # 経過時間を表示
        elapsed_time = t2-t1
        # T秒後
        elapsed_time = elapsed_time/T
        key = cv2.waitKey(delay) & 0xFF
        if(elapsed_time > N+1):
            N=N+1
            print("経過時間：{}",N)
            cv2.imwrite('{}.{}'.format(base_path,ext), frame)

            #画像認識
            try:
                conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
                conn.request("POST", "/face/v1.0/detect?%s" % params, open(file,"rb"), headers)
                response = conn.getresponse()
                data = response.read()
                data = json.loads(data)
                emotion = RaadJson(data)
                print(emotion)
                pic = cv2.imread(file)
                pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
                plt.imshow(pic)
                Recognize(emotion)
                conn.close()
            except ValueError and IndexError:
                print("表情を読み取れませんでした")
                #cmd_2 = -1
                #cmd_1 = "./node.js"
                #cmd = cmd_1+" "+"{}",cmd_2
                #subprocess.call(cmd, shell=True)

        elif key == ord('q'):
            break
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF


    cv2.destroyAllWindow(window_name)


save_frame_camera_key(0, './', 'capture')
