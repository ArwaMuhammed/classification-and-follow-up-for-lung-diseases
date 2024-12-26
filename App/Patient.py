class Patient:
     progressions = []
     def __init__(self, name, ID, diagnosis=None, progressions=None):
          self.name = name
          self.ID = str(ID)
          self.diagnosis=diagnosis
          self.progressions=progressions if progressions is not None else []

     def add_diagnosis(self, diagnosis):
          self.diagnosis = diagnosis

     def add_progression(self, progression):    
          self.progressions.append(progression)

