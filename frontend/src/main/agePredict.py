import face_recognition
import cv2
import numpy as np
import pandas as pd
import os
import uuid

try:
    cap = cv2.VideoCapture(0) 
    # 0: 웹캠, 1: 카메라
    flag = False
except:
    print("camera loading error")
    
def agePredict():
    #age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
    age_list = ['normal', 'normal', 'normal', 'normal', 'normal', 'normal', 'senior', 'senior']

    age_net = cv2.dnn.readNetFromCaffe(
              'D://python/age_gender_estimation-master/models/deploy_age.prototxt', 
              'D://python/age_gender_estimation-master/models/age_net.caffemodel')
    
    img1 = face_recognition.load_image_file("D:/python/data/img1.jpg")
    img1_face_encoding = face_recognition.face_encodings(img1)[0]
    img2 = face_recognition.load_image_file("D:/python/data/img2.png")
    img2_face_encoding = face_recognition.face_encodings(img2)[0]
    img3 = face_recognition.load_image_file("D:/python/data/img3.jpg")
    img3_face_encoding = face_recognition.face_encodings(img3)[0]
    img4 = face_recognition.load_image_file("D:/python/data/img4.jpg")
    img4_face_encoding = face_recognition.face_encodings(img4)[0]
    img5 = face_recognition.load_image_file("D:/python/data/img5.jpg")
    img5_face_encoding = face_recognition.face_encodings(img5)[0]
    img6 = face_recognition.load_image_file("D:/python/data/img6.jpg")
    img6_face_encoding = face_recognition.face_encodings(img6)[0]
    img7 = face_recognition.load_image_file("D:/python/data/img7.jpg")
    img7_face_encoding = face_recognition.face_encodings(img7)[0]
    img8 = face_recognition.load_image_file("D:/python/data/img8.jpg")
    img8_face_encoding = face_recognition.face_encodings(img8)[0]
    img9 = face_recognition.load_image_file("D:/python/data/img9.jpg")
    img9_face_encoding = face_recognition.face_encodings(img9)[0]
    img10 = face_recognition.load_image_file("D:/python/data/img10.jpg")
    img10_face_encoding = face_recognition.face_encodings(img10)[0]

    known_face_encodings = [
        img1_face_encoding,
        img2_face_encoding,
        img3_face_encoding,
        img4_face_encoding,
        img5_face_encoding,
        img6_face_encoding,
        img7_face_encoding,
        img8_face_encoding,
        img9_face_encoding,
        img10_face_encoding,
    ]

    known_face_names = [
        "RhoSeungChan",
        "ParkByeongHyun",
        "KimJinKyum",
        "halabum",
        "kimhayul",
        "parkjinyoung",
        "Kimmakrae",
        "Kimokji",
        "Parkyoungkwang",
        "Kimjinyoung",
    ]
    
    dirname = 'D:/python/data/resource/'
    files = os.listdir(dirname)
    
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            known_face_names.append(name)
            pathname = os.path.join(dirname, filename)
            img = face_recognition.load_image_file(pathname)
            face_encoding = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(face_encoding)
            
    face_locations = []
    face_encodings = []
    face_name = ['name',]
    face_age = ['age',]
    post_data = []
    count = 1
    name = ""
     
    while count <= 15:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        if face_encodings:
            count = count + 1
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.4)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_name.append(name)

        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

        for (top, right, bottom, left) in face_locations:
            face_img = frame[top:bottom, left:right]
            blob = cv2.dnn.blobFromImage(face_img, scalefactor=1, size=(227, 227),
                    mean=(78.4263377603, 87.7689143744, 114.895847746),
                    swapRB=False, crop=False)

            # 나이 예측
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]
            face_age.append(age)

        cv2.imshow('Video', frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
     

    for face_name, age in zip(face_name, face_age):
        post_data.append((face_name, age))
    dataframe = pd.DataFrame(post_data)
    print(dataframe)
         
    client_name = dataframe[0].value_counts().index[0]
    client_age = dataframe[1].value_counts().index[0]
            
    return client_name,client_age


client_name, client_age = agePredict()
print(f"Client Name: {client_name}, Client Age: {client_age}")

current_directory = os.getcwd()

file_path = os.path.join(current_directory,'frontend' ,'src', 'main' ,'templates','client_info.txt')

# txt 파일 저장
with open(file_path, 'w') as file:
    file.write(f"{client_age}")