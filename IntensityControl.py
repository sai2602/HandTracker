from HandTracking import HandTracker
import time
import cv2 as cv
import serial

SERIAL_PORT_INIT = 0

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    my_tracker = HandTracker(detect_confidence=0.7, track_confidence=0.7)
    hand_range = [20, 150]

    serial_session = serial.Serial('COM3', 9600)
    if not serial_session.is_open:
        serial_session.open()
    serial_session.write(str(SERIAL_PORT_INIT).encode())

    prev_time = 0
    curr_time = 0

    while True:

        success, img = cap.read()
        img = my_tracker.find_hands(img, draw_landmarks=False)
        co_ords_list = my_tracker.find_position(img)

        distance, updated_volume = my_tracker.volume_regulator(img, co_ords_list,
                                                               hand_range=hand_range)

        if distance != -1:
            serial_session.write(str(distance).encode())

        curr_time = time.time()
        fps = 1/(curr_time - prev_time)
        prev_time = curr_time

        cv.putText(img, f'FPS: {(int(fps))}', (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        cv.imshow("hand", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyWindow("hand")
            break
