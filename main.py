import cv2
from cvzone.PoseModule import PoseDetector
import socket

# Parameters
width, height = 1280, 720

# IP WebCam
cap = cv2.VideoCapture(0)

# 일반 WebCam 을 사용할 경우
#cap = cv2.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)

# 손을 감지
detector = PoseDetector(staticMode=False,
                        modelComplexity=1,
                        smoothLandmarks=True,
                        enableSegmentation=False,
                        smoothSegmentation=True,
                        detectionCon=0.5,
                        trackCon=0.5)

# 네트워크
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)


while True:
# 웹켐에서 프레임 가져오기
    success, img = cap.read()

    # Hands
    img = detector.findPose(img)

    lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

    # Check if any body landmarks are detected
    if lmList:
        # Get the center of the bounding box around the body
        center = bboxInfo["center"]

        # Draw a circle at the center of the bounding box
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        # Calculate the distance between landmarks 11 and 15 and draw it on the image
        length, img, info = detector.findDistance(lmList[11][0:2],
                                                  lmList[15][0:2],
                                                  img=img,
                                                  color=(255, 0, 0),
                                                  scale=10)

        # Calculate the angle between landmarks 11, 13, and 15 and draw it on the image
        angle, img = detector.findAngle(lmList[11][0:2],
                                        lmList[13][0:2],
                                        lmList[15][0:2],
                                        img=img,
                                        color=(0, 0, 255),
                                        scale=10)

        # Check if the angle is close to 50 degrees with an offset of 10
        isCloseAngle50 = detector.angleCheck(myAngle=angle,
                                             targetAngle=50,
                                             offset=10)

        # Print the result of the angle check
        print(len(lmList))

    # Display the frame in a window
    cv2.imshow("Image", img)

    # Wait for 1 millisecond between each frame
    cv2.waitKey(1)



    # data = []
    #
    # # 21개의 랜드마크 값들을 UDP 프로토콜을 사용하여 Unity에 보냄.
    # # Landmark values - (x,y,z) * 21
    # if hands:
    # # Get the first hand detected
    #     hand = hands[0]
    # # Get the landmark list
    #     lmList = hand['lmList']
    #     print(lmList)
    #     for lm in lmList:
    #         data.extend([lm[0], height - lm[1], lm[2]])
    #         print(data)
    #         sock.sendto(str.encode(str(data)), serverAddressPort)
    #
    #
    # img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    # cv2.imshow("Image", img)
    # if cv2.waitKey(1) == ord("q"): # q 누를 시 웹켐 종료
    #     break