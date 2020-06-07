import spam_message_classifier as smc
message='hello how are you'
message=[message,]
message=smc.cv.transform(message)
y=smc.model.predict(message)
print('hello how are you ',"is a",y[0])
