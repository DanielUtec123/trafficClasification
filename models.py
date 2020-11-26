
from sklearn import  svm
import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.naive_bayes import GaussianNB


encoders = []
le = preprocessing.LabelEncoder()

def leer_dataset(nom_archivo):
    return pd.read_csv(nom_archivo)

training_data = leer_dataset("/home/daniel/Documents/Utec/7to ciclo/Redes y Comunicaciones/Proyecto/scripts/data/training_dataset.csv")

y = training_data.pop('label').values
#X = le.fit_transform(training_data[0].values)

for column in training_data:
    encoder = preprocessing.LabelEncoder()
    training_data[column] = encoder.fit_transform(training_data[column].values)
    encoders.append(encoder)

print(training_data)

X = training_data.to_numpy()

print(X)

consulta = ['192.168.0.112'	,37264,	'64.233.186.108',587,6	,18,26,3464	,5779] # 2

def encodeConsulta(consulta):
    result = []
    for i in range(len(consulta)):
        encoder = encoders[i]
        value = consulta[i]
        if value in encoder.classes_:
            value = encoder.transform([value])
            result.append(value[0])
        else:
            value = -1
            result.append(-1)
        
    return result

consulta = ['192.168.0.112'	,37264,	'64.233.186.108',587,6	,18,26,3464	,5779] # 2
consulta2 = ['192.168.0.112'	,51280,	'64.233.186.101',	80,	1000,	22,	18,	1818,	17064] # 1
consulta3 = ['10.0.0.1',37498,'10.0.0.2',80,6,5,5,473,3072] # 1

consulta = encodeConsulta(consulta)
consulta2 = encodeConsulta(consulta2)
consulta3 = encodeConsulta(consulta3)

print(consulta)
print(consulta2)
print(consulta3)


clf = svm.SVC()
clf.fit(X, y)
p = clf.predict([consulta])
print(p)

model = GaussianNB()
model.fit(X,y)
p = model.predict([consulta])
p2 = model.predict([consulta2])
p3 = model.predict([consulta3])

print(p)
print(p2)
print(p3)