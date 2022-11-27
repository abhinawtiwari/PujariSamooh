import pickle

filename = 'finalized_model.sav'

loaded_model = pickle.load(open(filename, 'rb'))
[predicted_val] = loaded_model.predict([[2,91.04624672,13.92933001,26.18824997,0,0,4,1,217]])
print(int(predicted_val))