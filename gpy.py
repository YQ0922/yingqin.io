import random
import cv2
import mediapipe as mp
import numpy as np
import time

capture = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:
    previousTime = 0
    currentTime = 0
    imgW = 800
    imgH = 600
    boxW = 100
    img_counter = 0
    listX = []
    listY = []
    startFingerX = 0
    startFingerY = 0
    finalFingerX = 0
    finalFingerY = 0

    # x 軸位置，從 50 ~ 800-50 之間挑一個數字
    boxX = random.randint(boxW, imgW - imgH)

    # y 軸位置，從 50 ~ 600-50 之間挑一個數字
    boxY = random.randint(boxW, imgW - imgH)

    print(f"box: {boxX}, {boxY}")

    boxTouch = False
    boxPinch = False
    linePoints = []  # 新增線條的座標點列表

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            print("Cannot receive frame")
            break

        frame = cv2.resize(frame, (imgW, imgH))
        frame = frame[:, ::-1]  # 影像左右翻轉

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 取得目前影像的尺寸
        imgSize = image.shape
        w = imgSize[1]
        h = imgSize[0]

        # 如果有偵測到手部的節點
        if boxTouch and boxPinch:
            listX.append(indexFingerX)
            listY.append(indexFingerY)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

                # 取得食指指尖的座標位置
                indexFingerX = hand_landmarks.landmark[8].x * imgW
                indexFingerY = hand_landmarks.landmark[8].y * imgH
                # 取得大拇指的座標位置
                indexThumbX = hand_landmarks.landmark[4].x * imgW
                indexThumbY = hand_landmarks.landmark[4].y * imgH

                # 判斷指尖是否在方形
                if ((indexFingerX > boxX) and (indexFingerX < (boxX + boxW)) and (indexFingerY > boxY) and (indexFingerY < (boxY + boxW))):
                    boxTouch = True
                    boxX = int(indexFingerX) - 50
                    boxY = int(indexFingerY) - 50

                    # 判斷是否有捏住的動作
                    if ((indexFingerX - indexThumbX) ** 2 + (indexFingerY - indexThumbY) ** 2) < 1000:
                        boxPinch = True
                        linePoints.append((int(indexFingerX), int(indexFingerY)))
                    else:
                        boxPinch = False
                else:
                    boxTouch = False

        if boxTouch:
            # 繪製方框
            cv2.rectangle(image, (boxX, boxY), (boxX + boxW, boxY + boxW), (0, 0, 255), 1)
            if len(linePoints) > 1:
                cv2.polylines(
                    image, np.array([linePoints]), False, (0, 0, 255), thickness=2
                )
                startFingerX, startFingerY = linePoints[0]
                finalFingerX, finalFingerY = linePoints[-1]
                print(f"this is start：{startFingerX}, {startFingerY} ")
                print(f"this is final：{finalFingerX}, {finalFingerY} ")
        else:
            cv2.rectangle(image, (boxX, boxY), (boxX + boxW, boxY + boxW), (0, 255, 0), 1)

        # 計算fps
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(image, str(int(fps)) + " FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("course", image)

        k = cv2.waitKey(1)
        if k == ord("q"):
            print(cv2.waitKey(1))
            print(ord("q"))
            print(ord("a"))
            break

        if k % 256 == 32:
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))
            img_counter += 1


# 釋放資源
capture.release()
cv2.destroyAllWindows()
