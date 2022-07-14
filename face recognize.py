import cv2
from aip import AipFace
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
import threading
import numpy as np
import requests


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def frame2base64(frame):
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data  # 转码成功 返回base64编码


def process(image, ls):
    """ 调用人脸检测 """
    """ 如果有可选参数 """

    # 换成自己的appid
    APP_ID = '24390752'
    API_KEY = 'HIgBO2SdxXpY5udX0R19ytUF'
    SECRET_KEY = 'gIgz0FpPQRqRG45E2k00C0IbGrTMKFmK '
    groupIdList = "group1"  # 我的用户组，具体看创建什么
    imageType = 'BASE64'
    base64 = frame2base64(image)
    # base64 = str(base64)
    base64 = str(base64, 'UTF-8')
    options = {}
    options["face_field"] = "age,gender,emotion"
    options["max_face_num"] = 10
    options["face_type"] = "LIVE"
    options["match_threshold"] = 0
    # options["liveness_control"] = "NORMAL"
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    face_data = client.detect(base64, imageType, options)
    # print(face_data)
    if face_data['error_msg'] == 'SUCCESS':
        i = face_data['result']['face_list'][0]
        if i['face_probability'] > 0.8:
            # groupIdList = 'group_1'
            """ 如果有可选参数 """
            options = {}
            options["max_face_num"] = 10
            options["match_threshold"] = 0
            options["quality_control"] = "LOW"
            options["liveness_control"] = "LOW"
            options["max_user_num"] = 7
            # json1 = client.multiSearch(base64, imageType, groupIdList, options)
            json1 = client.multiSearch(base64, imageType, groupIdList, options)
            # print(json1)
            face_num = face_data['result']['face_num']
            for i in range(face_num):
                x = max(int(face_data['result']['face_list'][i]['location']['left']), 0)
                y = max(int(face_data['result']['face_list'][i]['location']['top']), 0)
                width = int(face_data['result']['face_list'][i]['location']['width'])
                height = int(face_data['result']['face_list'][i]['location']['height'])
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
                if json1['error_msg'] == 'SUCCESS':
                    if json1['result']['face_list'][0]['user_list'][i]['score'] > 70:
                        # print(json1['result']['face_list'][0]['user_list'][i]['user_id'])
                        face_data['name'] = json1['result']['face_list'][0]['user_list'][i]['user_id']
                        print(face_data)
                        res = requests.post(url, data=face_data)
                        print(res.text)
                        image = cv2ImgAddText(image, json1['result']['face_list'][0]['user_list'][i]['user_id'],
                                              max(x - 20, 0), max(y - 20, 0), (255, 255, 255), 20)
                    else:
                        cv2.putText(image,
                                    f"{str(face_data['result']['face_list'][i]['age'])} {face_data['result']['face_list'][i]['gender']['type']}",
                                    (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                    ls.append(image)


def main():
    video_capture = cv2.VideoCapture(1)

    while True:
        ls = []
        ret, frame = video_capture.read()
        t = threading.Thread(target=process, args=(frame, ls))
        t.start()
        t.join()
        frame = ls[0] if ls else frame
        cv2.imshow('wx', frame)
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            cv2.destroyAllWindows()
            video_capture.release()
            break


url = "http://www.rt-thread.com/service/echo"

if __name__ == "__main__":
    main()
