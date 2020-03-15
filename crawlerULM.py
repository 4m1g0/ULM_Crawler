import sys
from urllib.request import *
from bs4 import BeautifulSoup


def main(argv):
    questionsFile = open('questions.txt', 'w')
    page = 0
    
    while(True):
        page = page + 1
        print("PAGE: " + str(page))
        req = Request(
            'https://*****.es/base.php?marco=test3.php&nutex=' + str(page) + '&tip=COM', 
            data=None, 
            headers={
                'User-Agent': 'chrome',
                'Cookie': 'contador=1; conttot=2'
            }
        )
        
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        
        tableCol = soup.find('td', class_= 'central')
        question = tableCol.findAll(text=True)[3].strip()
        
        rightAnswer = 0
        for i in range(1,5):
            span = soup.find('span', {"id" : "s_001"+str(i)})
            if not span:
                break
            
            if span['class'][0] == 'a':
                rightAnswer = i

        answerList = []
        for i in range(1,5):
            label = soup.find('label', {"for" : "r_001"+str(i)})
            if not label:
                break
            
            answer = label.text.strip()
            answerList.append(answer)

        explanation = soup.find('div', class_= 'popup-contenedor')
        
        
        
        if rightAnswer == 0:
            print("error. Could not find the right answer.")
        
        if rightAnswer > len(answerList):
            print("error. The right answer is not in the list.")
            
        print(question + ', ')
        print(str(rightAnswer) + ', ')
        for i in range(0,4):
            if i < len(answerList):
                print(answerList[i] + ', ')
            else:
                print(' , ')
        #if explanation:
        #    print(explanation)
        
        questionsFile.write('"' + question + '", ')
        questionsFile.write(str(rightAnswer) + ', ')
        for i in range(0,4):
            if i < len(answerList):
                questionsFile.write('"' + answerList[i] + '", ')
            else:
                questionsFile.write(' , ')
        if explanation:
            questionsFile.write('"' + str(explanation).replace('\n', '').replace('"','') + '"')

        questionsFile.write('\r\n')


if __name__ == "__main__":
   main(sys.argv[1:])
