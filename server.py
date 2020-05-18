import smtpd
import asyncore

# Machine Learning code - analize the probability of email to by
# spam by using Baye's Classifire

# Training phase: Learning from data base

trainData = [] # @TODO: get database for training
SPAM = True
#runs once on training data
def train:
    total = 0
    numSpam = 0
    for email in trainData:
        if email.label == SPAM:
            numSpam += 1
        total += 1
        processEmail(email.body, email.label)
    pA = numSpam/(float)total
    pNotA = (total — numSpam)/(float)total

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
       return trainPositive[word]/(float)positiveTotal
    return trainNegative[word]/(float)negativeTotal

#classifies a new email as spam or not spam
def classify(email):
    isSpam = pA * conditionalEmail(email, True) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False) # P(¬A | B)
    return isSpam > notSpam


class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print ('Receiving message from:', peer)
        print ('Message addressed from:', mailfrom)
        print ('Message addressed to  :', rcpttos)
        print ('Message length        :', len(data))
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
