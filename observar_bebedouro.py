import cv2 as cv
import numpy as np

FPS = 20

cap = cv.VideoCapture('./bebeu-short.mp4')
ret, initial_frame = cap.read()

background = cv.imread('./background.jpg')
roi = background[145:180, 347:380]
cv.imshow('teste', roi)
cont_frames = 0
cont_segundos = 0

# controle de visita
visita_iniciada = False
cont_visita = 0


while True:
    ret, frame = cap.read()

    if ret is True:
        cropped_frame = frame[145:180, 347:380]
        cont_frames += 1
        if cont_frames == FPS:
            cont_segundos += 1
            cont_frames = 0

        diff = cv.absdiff(cropped_frame, roi)
        gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(
            dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            if cv.contourArea(contour) < 700:
                continue

            # contar tempo
            if cont_frames == 0:
                cont_visita += 1

            # desenhar retângulo
            (x, y, w, h) = cv.boundingRect(contour)
            color = (0, 255, 0) if cont_frames == 0 else (255, 0, 0)
            cv.rectangle(frame, (385, 170), (345, 130), color, 2)

        cv.imshow('suino', frame)

        if cv.waitKey(49) == 27:
            break
    else:
        break

print(str(cont_visita) + 'segundos')
cv.destroyAllWindows
cap.release()
