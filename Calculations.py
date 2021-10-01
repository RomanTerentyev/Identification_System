import os
import json
import cv2
import face_recognition

def recognition(data, accuracy_threshold=0.6, db_path='database'):
    result = {'Ошибка идентификации': None,
             'Уверенность системы в схожести фотографий': None,
             'Количество лиц в кадре': None,
             'Имя сотрудника': None,
             'Должность': None,
             'Идентификатор должности': None,
             'Порог точности': accuracy_threshold,
             'Идентификатор файла': None}
    
    error_list = ['Идентификационный номер отсутствует в БД',
                 'Нет лиц в кадре',
                 'Больше одного лица в кадре',
                 'Другой человек в кадре']
    
    _id = data['id']
    with open(f'{db_path}/database.json', encoding='utf-8') as f: database = json.load(f)
    
    try: result.update(database[str(_id)])
    except KeyError: return error_handler(data['image'], result, error_list[0])

    test_image = face_recognition.load_image_file(data['image'])
    test_encodings = face_recognition.face_encodings(test_image)
    result['Количество лиц в кадре'] = len(test_encodings)
    
    if len(test_encodings) == 0: return error_handler(data['image'], result, error_list[1])
    
    elif len(test_encodings) > 1: return error_handler(data['image'], result, error_list[2])
    
    else: 
        true_image = face_recognition.load_image_file(f'{db_path}/{_id}.jpg')
        true_encodings = face_recognition.face_encodings(true_image)        
        face_distance = face_recognition.face_distance(true_encodings, test_encodings[0])[0]
        result['Уверенность системы в схожести фотографий'] = face_distance
        
        if face_distance > accuracy_threshold: return error_handler(data['image'], result, error_list[3])
        else: return error_handler(data['image'], result, None)
    
def error_handler(img, result, error):
    if error:
        img_path = 'unsuccessful_identifications'
        result['Ошибка идентификации'] = error
    else: img_path = 'successful_identifications'        
        
    img = cv2.imread(img)
    n_files = len(os.listdir(path=img_path))
    filename = f'{img_path}/{n_files+1}.jpg'
    cv2.imwrite(filename,img)
    result['Идентификатор файла'] = filename
    return result