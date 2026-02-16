import cv2
import os

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

# samples folder agar nahi hai to bana do
os.makedirs(SAMPLES_DIR, exist_ok=True)

# ---------------- CAMERA SETUP ----------------
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

# ---------------- FACE DETECTOR ----------------
detector = cv2.CascadeClassifier(CASCADE_PATH)

# check cascade load hua ya nahi
if detector.empty():
    print("❌ ERROR: haarcascade_frontalface_default.xml load nahi hui")
    exit()

# ---------------- USER INPUT ----------------
face_id = input("Enter a Numeric user ID here: ")

print("📸 Taking samples, look at camera .......")
count = 0

# ---------------- MAIN LOOP ----------------
while True:
    ret, img = cam.read()
    if not ret:
        print("❌ Camera access nahi ho raha")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1

        face_img = gray[y:y+h, x:x+w]
        file_path = os.path.join(SAMPLES_DIR, f"face.{face_id}.{count}.jpg")
        cv2.imwrite(file_path, face_img)

        cv2.imshow("image", img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # ESC
        break
    elif count >= 100:
        break

# ---------------- CLEANUP ----------------
print("✅ Samples taken, closing program...")
cam.release()
cv2.destroyAllWindows()
