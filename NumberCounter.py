from HandTracking import HandTracker, Hands, Fingers
import time
import cv2 as cv


def get_hand_info(hand_number):
    hand = "Unknown"

    if not hand_number:
        hand = "Left"
    else:
        hand = "Right"

    return hand


def get_finger_info(finger_id):
    finger = ""
    if finger_id == Fingers.Thumb.value:
        finger = "Thumb"
    elif finger_id == Fingers.Index.value:
        finger = "Index"
    elif finger_id == Fingers.Middle.value:
        finger = "Middle"
    elif finger_id == Fingers.Ring.value:
        finger = "Ring"
    elif finger_id == Fingers.Little.value:
        finger = "Little"
    else:
        finger = "Unknown"

    return finger


if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    my_tracker = HandTracker(detect_confidence=0.7, track_confidence=0.7)

    prev_time = 0
    curr_time = 0

    left_info = []
    right_info = []
    current_number = -1

    while True:

        success, img = cap.read()
        img = my_tracker.find_hands(img, draw_landmarks=False)
        co_ords_list = my_tracker.find_position(img)

        number, fingers_info = my_tracker.detect_fingers_up(img, co_ords_list)

        if current_number != number:
            current_number = number
            print("Number: " + str(number))

        print_info = True
        if fingers_info[Hands.Left.value] == left_info and fingers_info[Hands.Right.value] == right_info:
            print_info = False

        if print_info:
            for hand_id, each_hand_info in enumerate(fingers_info):
                if hand_id:
                    right_info = each_hand_info
                else:
                    left_info = each_hand_info

                log_print = get_hand_info(hand_id) + ": "
                for each_finger_info in each_hand_info:
                    log_print += get_finger_info(each_finger_info) + ", "

                log_print = log_print[:-2]
                log_print += "\n"
                print(log_print)

        curr_time = time.time()
        fps = 1/(curr_time - prev_time)
        prev_time = curr_time

        cv.putText(img, f'FPS: {(int(fps))}', (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        cv.imshow("hand", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyWindow("hand")
            break
