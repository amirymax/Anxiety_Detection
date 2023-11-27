import pickle

class FromText:
    def __init__(self) -> None:
        with open('from_text/text_emotion_detection_model.pkl', 'rb') as model_file:
            self.model = pickle.load(model_file)
    
    def predict(self, text: str) -> str:
        state = {0: 'Negative',
                 2: 'Neutral',
                 4:'Positive'}
        n = self.model.predict([text])[0]
        return state[n]

model = FromText()

print(model.predict(input()))
