from Patient import *
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications.densenet import preprocess_input

class System:
    ID = 2453
    patients = []
    @classmethod
    def add_patient (cls, name, diagnosis=None, progressions=None):
        cls.ID += 1
        patient = Patient (name, cls.ID, diagnosis, progressions)
        cls.patients.append(patient)
        
        return cls.ID
    @classmethod
    def search_patient (cls, ID):
        for patient in cls.patients:
            if patient.ID == ID:
                return patient
        return None    
    
    @classmethod
    def connect_to_model (cls, img_path):
        model = load_model('saved_model.keras')
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        predictions = model.predict(img_array)
        predictions = predictions[0]
        labels = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 'Emphysema',
                  'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule', 'Pleural_Thickening',
                  'Pneumonia', 'Pneumothorax']
        prediction_dict = dict(zip(labels, predictions))
        return prediction_dict