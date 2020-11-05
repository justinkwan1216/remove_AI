import cv2
imagePath = "1.jpg"
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)
print("Found {0} faces!".format(len(faces)))
img_array=[]
# Draw a rectangle around the faces
for (x, y, w, h) in faces:

    img_array.append(image[y:y+h, x:x+w])
    #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found"+str(1), img_array[0])
cv2.imshow("Faces found"+str(2), img_array[1])

cv2.waitKey(0)
