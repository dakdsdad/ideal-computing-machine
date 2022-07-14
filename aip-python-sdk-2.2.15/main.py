
from aip import AipFace
import base64
import cv2
import numpy as np
from PIL import Image ,ImageDraw, ImageFont

global string


# 这里直接用cv2.putText（）也行，但是不能显示中文，如果输入中文就
# 会在图片上显示？？？
def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def show_result():
    img = cv2.imread(img_path)

    if list2['error_msg'] == 'SUCCESS':
        face_num = list2['result']['face_num']
        for i in range(face_num):

            x1 = int(list2['result']['face_list'][i]['location']['left'])
            y1 = int(list2['result']['face_list'][i]['location']['top'])
            x2 = x1 + int(list2['result']['face_list'][i]['location']['width'])
            y2 = y1 + int(list2['result']['face_list'][i]['location']['height'])

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            if list2['result']['face_list'][i]['user_list'] != []:
                print(list2['result']['face_list'][i]['user_list'][0]['score'])
                if list2['result']['face_list'][i]['user_list'][0]['score'] > 70:

                    print('员工', list2['result']['face_list'][i]['user_list'][0]['user_id'])
                    # cv2.putText(img, '员工', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    img = cv2ImgAddText(img, "员工", x1 - 20, y1 - 20, (255, 255, 255), 30)
                else:
                    print("访客")
                    # cv2.putText(img, '访客', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    img = cv2ImgAddText(img, "访客", x1 - 20, y1 - 20, (0, 0, 255), 20)
            else:
                img = cv2ImgAddText(img, "访客", x1 - 20, y1 - 20, (0, 0, 255), 20)
                print("访客")
        cv2.imshow('wx', img)
    elif res1['error_msg'] == 'SUCCESS':
        face_num = res1['result']['face_num']

        for i in range(face_num):
            x1 = int(res1['result']['face_list'][i]['location']['left'])
            y1 = int(res1['result']['face_list'][i]['location']['top'])
            x2 = x1 + int(res1['result']['face_list'][i]['location']['width'])
            y2 = y1 + int(res1['result']['face_list'][i]['location']['height'])

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            img = cv2ImgAddText(img, "访客", x1 - 20, y1 - 20, (0, 255, 0), 30)
            cv2.imshow('wx', img)
    else:
        user_result = {'is_user': is_user}
        print(user_result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    # """ 你的 APPID AK SK """

    APP_ID = '24390752'
    API_KEY = 'HIgBO2SdxXpY5udX0R19ytUF'
    SECRET_KEY = 'gIgz0FpPQRqRG45E2k00C0IbGrTMKFmK '
    imageType = "BASE64"
    groupIdList = "group1"  # 我的用户组，具体看创建什么

    client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    img_path = r'D:\python\test\1.jpg'
    # 这个api要求必须是Base64格式的，所以我们要把图片改为base64
    with open(img_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)  # base64编码
        string = str(base64_data, "utf-8")
        # print(string)

    image = string
    list1 = client.search(image, imageType, groupIdList)  # 单人

    options = {}
    options["max_face_num"] = 10
    options["match_threshold"] = 70
    options["quality_control"] = "NONE"
    options["liveness_control"] = "NONE"
    options["max_user_num"] =7

    is_user = False

    list2 = client.multiSearch(image, imageType, groupIdList, options)

    res1 = client.detect(image, imageType, options)
    print(res1)







