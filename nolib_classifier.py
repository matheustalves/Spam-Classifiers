import csv

dataset = []
size = 2000
count_ham = 0
count_spam = 0

with open('data.csv', 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in reader:
        if line_count == size + 1:
            break
        if line_count != 0:
            dataset.append([row[2].lower().split(), row[3]])
            if row[3] == '0':
                count_ham += 1
            else:
                count_spam += 1
        line_count += 1


vocabulary = set()
for row in dataset[:int(0.8*(len(dataset)))]:
    vocabulary = vocabulary.union(set(row[0]))
vocabulary = list(vocabulary)

cWord_spam = {}
cWord_ham = {}
cWord_total = {}

for word in vocabulary:
    cWord_spam[word] = 0
    cWord_ham[word] = 0
    for row in dataset[:int(0.8*(len(dataset)))]:
        if row[1] == '0':
            cWord_ham[word] += row[0].count(word)
        else:
            cWord_spam[word] += row[0].count(word)
    
    cWord_total[word] = cWord_ham[word] + cWord_spam[word]

totalWords_ham = sum(cWord_ham.values())
totalWords_spam = sum(cWord_spam.values())
totalWords = sum(cWord_total.values())

prob_ham = count_ham / (0.8*size)
prob_spam = 1 - prob_ham

probWord_ham = {}
probWord_spam = {}
probWord = {}

for word in vocabulary:
    probWord_ham[word] = cWord_ham[word]/totalWords_ham
    probWord_spam[word] = cWord_spam[word]/totalWords_spam
    probWord[word] = cWord_total[word]/totalWords


x_test = dataset[int(0.8*(len(dataset))):]
probs_test = []

for row in x_test:
    email = row[0]
    tempProb_ham = prob_ham
    tempProb_spam = prob_spam
    for word in email:
        if word in vocabulary:
            tempProb_ham *= probWord_ham[word]/probWord[word]
            tempProb_spam *= probWord_spam[word]/probWord[word]

    if tempProb_ham > tempProb_spam:
        probs_test.append('0')
    else:
        probs_test.append('1')

hits = 0
for i in range(len(x_test)):
    # print(f"predict: {probs_test[i]} /// expected: {x_test[i][1]}")
    if probs_test[i] == x_test[i][1]:
        hits += 1

print(f"Accuracy: {hits*100/len(x_test)}%")