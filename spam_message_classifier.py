import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import pickle
df=pd.read_csv("spam.csv")

x=df["EmailText"]
y=df["Label"]

x_train, y_train=x[0:4457],y[0:4457]
x_test,y_test=x[4457:],y[4457:]

cv=CountVectorizer()
features=cv.fit_transform(x_train)
tuned_parameters={'kernel':['linear','rbf'],'gamma':[1e-3,1e-4],'C':[1,10,100,1000]}
model= GridSearchCV(svm.SVC(),tuned_parameters)
model.fit(features,y_train)

pickle.dump(model,open('final_trained_model','wb'))
features_test=cv.transform(x_test)

print("Training complete and Accuracy of the model is ",model.score(features_test,y_test))
