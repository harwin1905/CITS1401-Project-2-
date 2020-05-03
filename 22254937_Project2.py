#Student Name: Harwinddranath Muralitheran
#Student_ID: 22254937
#CITS1401 - Project 2

import os
import math

#This function checks file1 input and makes sure the file exists. If the file exists, the program reads the file
#and sanitizes the text in the file, replacing punctuations with full stops, indicating sentences.
def file1_exists(textfile1):
    
    if not os.path.isfile(textfile1):
        print('File 1 not found.')
        return None
    else:
        print('Profile of text: ',textfile1)
        
        with open(textfile1, 'r') as file1:
            sanitized = file1.read().replace('!','.').replace('?','.').replace('\n',' ').replace('--',' ').lower().strip()
            result = [x for x in sanitized.split('.') if x]#remove blank lines
            
            return result

#This function checks that the file for argument 2 exists in the directory and if it does not,
#sets the argument to a string called 'listing'.
#The text in file2 is sanitized to replace the punctuation marks with full stops. 
def file2_exists(arg2):
    
    if not os.path.isfile(arg2):
        arg2 = 'Listing'
        return None
    else:
        print('vs')
        
        print('Profile of text: ',arg2)
        
        with open(arg2, 'r') as file2:
            sanitized2 = file2.read().replace('!','.').replace('?','.').replace('\n',' ').replace('--',' ').lower().strip()
            result = [x for x in sanitized2.split('.') if x]#remove blank lines
            
            return result

#If the file exists, the file is opened as file3, which is used in later functions.
def punc_countt(filename):
    
    if not os.path.isfile(filename):
        print('File 1 not found.')
        return None
    else:
        with open(filename,'r') as file3:
            result = file3.read()
        
        return result

#This function counts the number of occurences for each word in the input text files. For any remaining
#punctuation marks, they are replaced and the words are counted.
#The number of occurences for the conjunctions in the text are added to a separate dictionary named 'Profile'.

def countwords(wordlist,profile):
    
    seen = set()
    
    result = {}
    
    nested_list = [x for x in wordlist if x]
    
    puncx = '!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~'
    
    for sentence in nested_list:
        for char in puncx:
            sentence = sentence.replace(char,'')
        for word in sentence.split(' '):
            if word not in seen:
                seen.add(word)
                result[word]=0
        for word in sentence.split(' '):
            result[word]+=1
    
    conjunctions = ['also','although','and','as','because','before','but','for','if','nor',
                    'of','or','since','that','though','until','when','whenever',
                    'whereas','which','while','yet']
    
    for word in conjunctions:
        if word in result.keys():
            profile[word] = result[word]
        else:
            profile[word] = 0.0000
    
    return result,seen


#This function removes any special characters from the sanitized text file. 
def sanitise(stringx):
    
    punc2 = '!"#$%&()*+/:<=>?@[\\]^_`{|}~'
    
    sanitised_string = stringx.lower()
    
    while '  ' in sanitised_string:
        sanitised_string = sanitised_string.replace('  ',' ')
    for chars in punc2:
        sanitised_string = sanitised_string.replace(chars,'')
    
    return sanitised_string    


#This function serves to count the occurences of the important punctuations (',', "'", '-' and ';'.
#The count of each punctuation character is added to the existing 'profile' dictionary.
def count_punctuations(sentences,profile):
    
    sentences = sentences.replace('--',' ').replace('!','.').replace('?','.').replace('\n',' ')
    
    important_punc = "',-;"
    
    punc_counts = {}
    
    sentences = sanitise(sentences)
    
    count = 0
    
    for sentence in sentences.split('.'):
        for word in sentence.split(' '):
            if word.strip("'").count("'") == 1:
                count+=1
    
    for char in sentences:
        if char in important_punc:
            punc_counts[char]=0
    
    for char in sentences:
        if char in important_punc:
            punc_counts[char]+=1
    punc_counts["'"] = count    
    
    for key,val in punc_counts.items():
        profile.update(punc_counts)

#This function counts the number of words in each sentence in the text file and adds the count to the  'profile'
#dictionary.
def words_per_sentence(sentences,profile):    
    
    sentences = sentences.replace('--',' ').replace('!','.').replace('?','.').replace('\n',' ')#.replace('\n\n','\n')
    
    sentence_length = []
    
    sentences = sanitise(sentences)
    
    for sentence in sentences.split('.'):
        if sentence.strip() != '':#Skip over empty lines
            words = sentence.strip().split(' ')
            for word in sentence.strip().split(' '):
                if ',' in word.strip(',') and word.replace(',','').isdigit():
                    #If there is any digit which has a comma in between like '80,000' convert the comma into a fullstop...
                    words = [word.replace(',','.') if ',' in word.strip(',') and word.replace(',','').isdigit() else word.strip(',') for word in words]
                    #Then perform the split function on that fulstop to convert it into two words
                    words = [sub_item for item in words for sub_item in item.split(".")]
            
            words = list(filter(None, [x.strip("'") for x in words if x]))# remove unnecessary single quotes ('')  around words            
            
            length = len(words)
            
            sentence_length.append(length)
    
    average_words_per_sentence = ((sum(sentence_length)))/(len(sentence_length))
    
    profile['words_per_sentence'] = average_words_per_sentence
    
    return profile


#This function counts the number of sentences in each paragraph for the respective text file and adds the count
#to the 'profile' dictionary.
def sentences_per_para(sentences,profile):
    
    sentences_para = sentences#clone to avoid removing \n
    
    sentences = sentences.replace('--',' ').replace('!','.').replace('?','.').replace('\n',' ')
    
    sentences = sanitise(sentences)
    
    no_of_para = sentences_para.strip().split('\n\n')#2 new-line characters represent break between paragraphs.
    
    sentences = sentences.strip().split('.')
    
    sentences = [x for x in sentences if x]#to remove blank lines
    
    sentences_paragraph = len(sentences)/len(no_of_para)
    
    profile['sentences_per_para'] = sentences_paragraph
    
    profile['no_of_sentences'] = len(sentences)
    
    return profile

#This function prints the 'profile' dictionary in separate lines for each key.
#The dictionary contains the counts for the conjucntions, punctuations, number of words per sentence and the
#number of sentences per paragraph. 
def print_profile(profile):
   
    for elements in sorted(profile):
        print("{:<30}  :  {:.4f}".format(repr(elements),profile[elements]))
    
    print()#print blank line after each file

#This function normalises the values for each count in the 'profile' dictionary if the third argument,
# 'Normalize' is set to TRUE. 
def normalise_dict(dict):
    
    exceptions = ['no_of_sentences','sentences_per_para','words_per_sentence']
    
    for items in dict.items():
        if items[0] not in exceptions:
            dict[items[0]] = round((items[1]/dict['no_of_sentences']),4)
    
    return dict


#This function calculates the distance between the profiles of the two texts specified. 
def calculation(p1,p2):
    
    result = [(p1[key]-p2[key])**2 for key in p1.keys()]
    
    resultsum = sum(result)
    
    resultsqrt = math.sqrt(resultsum)
    
    return round(resultsqrt,4)

#This function initialises the above functions. 
def final_calc(filelist,filename,secondFile,Normalize):
    
    if filelist == None:
        return None
    else:
        profile = {}
        punc = punc_countt(filename)
        count_punctuations(punc,profile)
        result,seen = countwords(filelist,profile)
        profile = words_per_sentence(punc,profile)
        profile = sentences_per_para(punc,profile)
        if Normalize:
            profile = normalise_dict(profile)
        del profile['no_of_sentences']
        if secondFile:
            print_profile(profile)
        else:
            return profile

#This function calls other functions to execute the program, as mentioned in the project specification.
def main(textfile1, arg2, Normalize=False):
    
    file1 = file1_exists(textfile1)
    
    file2 = file2_exists(arg2)
    
    if file2 == None:
        profile1 = final_calc(file1,textfile1,True,Normalize)
    else:
        profile1 = final_calc(file1,textfile1,False,Normalize)
        profile2 = final_calc(file2,arg2,False,Normalize)
        print('The distance between the two texts is:',calculation(profile1, profile2))

