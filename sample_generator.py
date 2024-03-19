import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Video Capture Object to capture the video through webcam

cam.set(3, 640)  # Video Frame Width
cam.set(4, 480)  # Video Frame Height

detector = cv2.CascadeClassifier("Classifier/haarcascade_frontalface_default.xml")

id = input("Enter a Numeric user ID  here:  ")
# Integer ID for every new face (0, 1, 2...)

print("Taking Samples, look at Camera... ")
count = 0

while True:
    ret, img = cam.read()
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(converted_image, 1.3, 5)

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        cv2.imwrite(
            "Samples/face." + str(id) + "." + str(count) + ".jpg",
            converted_image[y : y + h, x : x + w],
        )
        cv2.imshow("image", img)

    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        break
    elif count > 100:
        break

print("Completed Taking Samples!")
cam.release()
cv2.destroyAllWindows()
