import smtpd
import asyncore
import getData

# Machine Learning code - analize the probability of email to by
# spam by using Baye's Classifire

# Training phase: Learning from data base

trainData = getData.getData()
SPAM = True
trainPositive = {}
trainNegative = {}
positiveTotal = 0
negativeTotal = 0
pA = 0
pNotA = 0

#runs once on training data
def train():
    global pA
    global pNotA
    total = 0
    numSpam = 0
    for email in trainData:
        if email[0] == SPAM:
            numSpam += 1
        total += 1
        processEmail(email[1], email[0])
    pA = numSpam/total
    pNotA = (total - numSpam)/total

#counts the words in a specific email
def processEmail(body, label):
    global positiveTotal
    global negativeTotal
    body = body.split()
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
    body = body.split()
    for word in body:
        result *= conditionalWord(word, spam) # con
    return result

#gives the conditional probability p(B_i | A_x)
def conditionalWord(word, spam):
    if spam:
        print('spam ', trainPositive.get(word,0))
        if trainPositive.get(word,0) == 0:
            return 1
        else:
            return trainPositive[word]/positiveTotal
    if trainNegative.get(word,0) == 0:
        return 1
    else:
        print('ham ', trainNegative.get(word,0))
        return trainNegative[word]/negativeTotal

#classifies a new email as spam or not spam
def classify(email):
    isSpam = pA * conditionalEmail(email, True) # P (A | B)
    notSpam = pNotA * conditionalEmail(email, False) # P(¬A | B)
    return isSpam > notSpam


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

        return

train()
print('Test prints:')
print ('positiveTotal: ', positiveTotal)
print ('negativeTotal: ', negativeTotal)
print ('Length of trainPositive: ', len(trainPositive))
print ('Length of trainNegative: ', len(trainNegative))
print ('Length of trainData: ', len(trainData))

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
