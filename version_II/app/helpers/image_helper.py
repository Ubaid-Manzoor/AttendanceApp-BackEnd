import face_recognition
import os

print("==============================")
print(os.getcwd())
print("==============================")


def generate_image_encoding():
    face_picture = face_recognition.load_image_file("app/tabishGroup.jpeg")
    face_locations = face_recognition.face_locations(face_picture,model='hog')
    return face_recognition.face_encodings(face_picture, face_locations)
