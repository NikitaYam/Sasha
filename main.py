import face_recognition
known_image = face_recognition.load_image_file("andrey.jpg")
unknown_image = face_recognition.load_image_file("papa.jpg")

known_encoding = face_recognition.face_encodings(known_image)
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces(known_encoding, unknown_encoding)[0]
if results:
    print('Одно лицо!!!')
else:
    print('Совсем не похожи...')
