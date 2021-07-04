from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from joblib import dump,load
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn import svm

data = pd.read_excel("dataSet.xlsx")
target = data["target"]
arrays = data[["spam_rate", "normal_rate"]]
Standard = StandardScaler()
arrays = Standard.fit_transform(arrays)
x_train, x_test, y_train, y_test = train_test_split(arrays, target, test_size=0.25, random_state=9)
x_train = Standard.fit_transform(x_train)
x_test = Standard.fit_transform(x_test)

# model = GaussianNB()
# model.fit(x_train, y_train)
# ss = model.predict(x_test)
# print(model.score(x_train,y_train))
# print(accuracy_score(y_test,ss))

# a = 0
# b = 0
# gama = 0
# for i in range(10, 101):
#     model = svm.SVC(C=0.8, kernel='rbf', gamma=i, decision_function_shape='ovr')
#     model.fit(x_train, y_train)
#     res = model.predict(x_test)
#     train_score = model.score(x_train, y_train)
#     test_score = accuracy_score(y_test, res)
#     if test_score >= b:
#         a = train_score
#         b = test_score
#         gama = i
#
# print(a, '\t', b, '\t', gama)

model = svm.LinearSVC(C=0.8,max_iter=1000)
model.fit(x_train, y_train)
# dump(model,"svm_model2")
# model = load("svm_model")
res = model.predict(x_test)
train_score = model.score(x_train, y_train)
test_score = accuracy_score(y_test, res)
print(train_score,test_score)

# model = KNeighborsClassifier()
# neibors = {"n_neighbors": [1, 3, 5]}
# train = GridSearchCV(model,param_grid=neibors,cv=5)
# train.fit(x_train,y_train)
# print(model.score(x_test,y_test))
# print(model.score(x_train,y_train))
