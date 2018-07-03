'''
TCSS 435 - PA 3. Trigram Language Model

@author: Jieun Lee (jieun212@uw.edu)
@version: June 01, 2017

** Instruction:
    - The output text files are saved in the same folder of this project.
    - It will not display new story on the console. Please see the generated output text file.
    - Only the process of running this program will be displayed on the console.
      (please wait until you see 'Done! Please see the output text files' on the console)
'''

import random

def main():
    
     
    # Open and read input text file, convert all to lower cases, and create word list
    doyle_txt = open("doyle-27.txt", 'r').read().lower().split()
    doyle_case_txt = open("doyle-case-27.txt", 'r').read().lower().split()
    alice_txt = open("alice-27.txt", 'r').read().lower().split()
    london_call_txt = open("london-call-27.txt", 'r').read().lower().split()
    melville_billy_txt = open("melville-billy-27.txt", 'r').read().lower().split()
    twain_adventures_txt = open("twain-adventures-27.txt", 'r').read().lower().split()
    
    print ("Read all the input text files successfully")
 
    # ---- For 2 books -----
     
    # Open a file to write a new story
    output_2books = open("2books.txt", 'w')
     
    # Combines 2 books
    words2 = doyle_txt + doyle_case_txt
    
    print ("Creating tri-gram model for 2 books ...")
    # Train a  tri-gram language model with given word list
    word_dict2 = trainTrigramLanguageModel(words2)
     
    print ("Generating a new story of 2 books ... ")
    
    # Choose a word from word_dict(hash table) at random to generate a new story of 1000 words
    generateStroy(output_2books, word_dict2, 1000)
     
    # Close opened output file
    output_2books.close()
     
    print ("A new story of 2 books is generated successfully!")
     
     
     
     
    # ----- For 6 books -----
     
    # Open a file to write a new story
    output_6books = open("6books.txt", 'w')
      
    # Combines 6 books
    words6 = alice_txt + doyle_txt + doyle_case_txt + london_call_txt + melville_billy_txt + twain_adventures_txt
     
    print ("Creating tri-gram model for 6 books ...")
    # Train a  tri-gram language model with given word list
    word_dict6 = trainTrigramLanguageModel(words6)
     
    print ("Generating a new story of 6 books ... ")
    # Choose a word from word_dict(hash table) at random to generate a new story of 1000 words
    generateStroy(output_6books, word_dict6, 1000)
     
    # Close opened output file
    output_6books.close()
    print ("A new story of 6 books is generated successfully!")
      
      
    print ("Done! Please see the output text files")
              
            
            
# Generates a new story and write the story on the given output file   
def generateStroy(outputFile, word_dict, lenOfWord):
    
    # Choose 1st word from word_dict at random
    key1 = random.choice(list(word_dict.keys()))
    count = 1
    
    #print (key1.word)
    outputFile.write(str(key1.word))
    
    # get words until total number of words are the given lenOfWord
    while True:

        # Extends next word at random 
        key2 = random.choice(list(key1.nextDict.keys()))
        #print(key2.word)
        outputFile.write(' ' + str(key2.word))
        
        # increases the number of words for the new story
        count += 1
        
        if (count >= lenOfWord):
            break
        
        # Get the last key which has high probability
    
        maxProbability = 0
        key3 = None
        for k in key2.nextDict:
            if (key3 == None):
                key3 = k
            currentP = calculateProbability(key2.nextDict[k], key1.nextDict[key2])
            #print('\t', currentP, k.word)
            if (currentP > maxProbability):
                maxProbability = currentP
                key3 = k
                #print(maxProbability, key3.word)
        
        #print(key3.word)
        outputFile.write(' ' + str(key3.word))
        # print(key2.word, key3.word, '[' , key1.nextDict[key2],'/', key2.nextDict[key3], '=',calculateProbability(key2.nextDict[key3], key1.nextDict[key2]), ']')
    
        # increases the number of words for the new story
        count += 1
        
        # get the 1st word from word_dict
        for key in word_dict:
            hasWord = False
            if (key.word == key3.word):
                hasWord = True
                key1 = key
                break
        
        # If there is no word that starts with the previous last word,
        # get the first word at random from word_dict
        if (not hasWord):
            key1 = random.choice(list(word_dict.keys()))

     
        

# Construct tri-gram language model with given the list of words
def trainTrigramLanguageModel(words):
        
    word_dict = dict() 
    
    for i in range (0, len(words) - 2):
        
        # check if there exists 2nd word for 1st word
        w1_has_key = False
        for key1 in word_dict:
            if (words[i] == key1.word):
                w1_has_key = True
                w1_key = key1
                break
            
        if (w1_has_key):  # if the key exists in the word_dict
            
            # increase value of w1[key]
            word_dict[w1_key] += 1
            
            # check if there exists 2nd word for 1st word
            w2_has_key = False
            for key2 in w1_key.nextDict:
                if (words[i + 1] == key2.word):
                    w2_has_key = True
                    w2_key = key2 
                    break
            
            if (w2_has_key):  # if the key exists in the  w2_dict
                
                # increase value of w2[key]
                w1_key.nextDict[w2_key] += 1
                
                # check if there exists 3rd word for 1st and 2nd word
                w3_has_key = False
                for key3 in w2_key.nextDict:
                    if (words[i + 2] == key3.word):
                        w3_has_key = True
                        w3_key = key3 
                        break
                
                if (w3_has_key):  # if the key exists in the  w3_dict
                    
                    # increase value of w3[key]
                    w2_key.nextDict[w3_key] += 1

                else:
                    
                    # Add new key with its value with 1 for w3_dict
                    w3_key = Node(words[i + 2])
                    w2_key.nextDict[w3_key] = 1
   
            else:
                # Add new key with value 1 for w2_dict & w3_dict\
                w2_key = Node(words[i + 1])
                w3_key = Node(words[i + 2])
                
                w2_key.nextDict[w3_key] = 1
                w1_key.nextDict[w2_key] = 1
                

        else:
            # Add new key with value 1 for w1_dict & w2_dict & w3_dict
            w1_key = Node(words[i])
            w2_key = Node(words[i + 1])
            w3_key = Node(words[i + 2])
            w2_key.nextDict[w3_key] = 1
            w1_key.nextDict[w2_key] = 1
            word_dict[w1_key] = 1
    
    return word_dict      


        
# Calculates probability of the word is used
# P (word | given1, given2)
def calculateProbability(w3, w2):
    return round((w3 / w2), 5)

# Tests with 2 short text file to generate 10 length of word of the new story.
def testProgram():
    doyle_txt = open("test.txt", 'r').read().lower().split()
    doyle_case_txt = open("test2.txt", 'r').read().lower().split()
       
    output_test = open("testOut.txt", 'w')
       
    words = doyle_txt + doyle_case_txt
    word_dict = trainTrigramLanguageModel(words)
       
    printThreeWordsWithValue(word_dict)
       
    generateStroy(output_test, word_dict, 10)
       
    output_test.close() 
    
# Tests for calculating probability
def testCalculateProbability(word_dict):
    for key1 in word_dict:
        if (key1.word == 'it'):
            for key2 in key1.nextDict:
                if (key2.word == 'finger'):
                    for key3 in key2.nextDict:
                        if (key3.word == 'on'):
                            print(key1.nextDict[key2], key2.nextDict[key3], calculateProbability(key2.nextDict[key3], key1.nextDict[key2]))
    

# Prints all 3 consecutive words with its values and the probability
def printThreeWordsWithValue(word_dict):
    print ("---- (Word Dictionary (Hash Table)) -------------------")
    for key1 in word_dict:
        for key2 in key1.nextDict:
            for key3 in key2.nextDict:
                print(key1.word, word_dict[key1], key2.word, key1.nextDict[key2], key3.word, key2.nextDict[key3], '\t\t P(w3/w2) = ', calculateProbability(key2.nextDict[key3], key1.nextDict[key2]))
    print ("-------------------------------------------------------")
    

# Node class: Each node has its word and the its own child dictionary
class Node:
    def __init__(self, word):
        self.word = word
        self.nextDict = dict()
    
    def __str__(self):
        return self.word
        

if __name__ == '__main__':
    main()
