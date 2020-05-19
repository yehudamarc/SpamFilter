import smtpd
import asyncore

# Machine Learning code - analize the probability of email to by
# spam by using Baye's Classifire

# Training phase: Learning from data base

trainData = [] # @TODO: get database for training
SPAM = True
#runs once on training data
def train():
    total = 0
    numSpam = 0
    for email in trainData:
        if email.label == SPAM:
            numSpam += 1
        total += 1
        processEmail(email.body, email.label)
    pA = numSpam/total
    pNotA = (total - numSpam)/total

#counts the words in a specific email
def processEmail(body, label):
    for word in body:
        if label == SPAM:
            trainPositive[word] = trainPositive.get(word, 0) + 1
            positiveTotal += 1
        else:
            trainNegative[word] = trainNegative.get(word, 0) + 1
            negativeTotal += 1

# Functions for analyzing given email:

#gives the conditional probability p(B | A_x)
def conditionalEmail(body, spam):
    result = 1.0
    for word in body:
        result *= conditionalWord(word, spam) # con
    return conditionalEmail

#gives the conditional probability p(B_i | A_x)
def conditionalWord(word, spam):
    if spam:
       return trainPositive[word]/positiveTotal
    return trainNegative[word]/negativeTotal

#classifies a new email as spam or not spam
def classify(email):
	return False
    #isSpam = pA * conditionalEmail(email, True) # P (A | B)
    #notSpam = pNotA * conditionalEmail(email, False) # P(¬A | B)
    #return isSpam > notSpam


class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        
        data_as_string = str(data)
        message_text = data_as_string.split('Subject:')[1]

        if classify(message_text):
        	print ('Mail is spam! exiting...')
        	return
        else:
        	print ('Mail is okay, keep proccesing...')
        	print ('Receiving message from:', peer)
        	print ('Message addressed from:', mailfrom)
        	print ('Message addressed to  :', rcpttos)
        	print ('Message length        :', len(data))
        	print ('Message               :', message_text)
        	#subject = message_text.split('\n\n')[0]
        	#body = message_text.split('\n\n')[1]
        	#print ('Subject               :', subject)
        	#print ('Body                  :', body)

     
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
