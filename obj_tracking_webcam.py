import cv2
import sys
import urllib.request
import numpy as np

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


class point:#needed to determine direction of the object

    def __init__(self):
        self.x = 0
        self.y = 0


# Constant integers for directions
RIGHT = 1
LEFT = -1
ZERO = 0

#calculate the direction
def directionOfPoint(A, B, P):
    global RIGHT, LEFT, ZERO

    # Subtracting co-ordinates of
    # point A from B and P, to
    # make A as origin
    B.x -= A.x
    B.y -= A.y
    P.x -= A.x
    P.y -= A.y

    # Determining cross Product
    cross_product = B.x * P.y - B.y * P.x

    # Return RIGHT if cross product is positive
    if (cross_product > 0):
        return RIGHT

    # Return LEFT if cross product is negative
    if (cross_product < 0):
        return LEFT

    # Return ZERO if cross product is zero
    return ZERO


if __name__ == '__main__':

    # Set up tracker.
    # Instead of CSRT, you can also use

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]# select kcf tracking

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    url = 'http://192.168.1.12/cam-mid.jpg'

    # video = cv2.VideoCapture(0) # for using CAM

    # Exit if video not opened.
    # if not video.isOpened():
    #     print("Could not open video")
    #     sys.exit()
    #
    # # Read first frame.
    # ok, frame = video.read()
                                            # if not ok:
                                            #     print('Cannot read video file')
                                            #     sys.exit()

    setroi = 0

    while True:
        # Read a new frame
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)
        #   break
        if setroi == 0:# we want to set initial bounding box so we run this once only
            # Define an initial bounding box
            bbox = (287, 23, 86, 320)

            # Uncomment the line below to select a different bounding box
            bbox = cv2.selectROI(frame, False)

            # Initialize tracker with first frame and bounding box
            ok = tracker.init(frame, bbox)
            setroi=1
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # showing coordinates on frame
        #rectangle_center = (int(p1[0] + p2[0]) / 2,int(p1[0] + p2[0]) / 2)
        #print(rectangle_center)
        A = point()
        B = point()
        P = point()
        #defining arbitrary divide
        A.x = 400
        A.y = 600  # A(-30, 10)
        B.x = 400
        B.y = 0  # B(29, -15)
        #center of object to be tracked
        P.x = int(p1[0] + p2[0]) / 2
        P.y = int(p1[0] + p2[0]) / 2

        direction = directionOfPoint(A, B, P)

        if (direction == 1):
            print("Right Direction")
        elif (direction == -1):
            print("Left Direction")
        else:
            print("Point is on the Line")
        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):  # if press SPACE bar
            break
cv2.destroyAllWindows()