# Modules
import json
import glob
import os
import argparse

import json_to_text
import sparv_annotation
import sparv_identification
import identification
import evaluation

#This is the starting file for evaluation

exceptions = ['Evaluative', 'Investigative']

genres = {
"AT3":"Narrative",
"AT4":"Argumentative",
"BT1":"Investigative",
"CT1":"Narrative, Instructions",
"CT2":"Argumentative",
"ET2":"Evaluative",
"ET3":"Evaluative",
"ET4":"Evaluative",
"ET5":"Evaluative",
"FT1":"Argumentative",
"GT3":"Narrative",
"GT4":"Narrative"
}

labels_per_genre = {}
words_per_genre = {}
wordlists_per_genre = {}

def add_wordlists_to_genre(genre, wordlist):
    
    if genre not in wordlists_per_genre:
        
        words = []
        
        for w in wordlist:
            if w not in words:
                wordlist.append(w)
        
        wordlists_per_genre[genre] = words

    else:
        
        for w in wordlist:
            if w not in wordlists_per_genre[genre]:
                wordlists_per_genre[genre].append(w)
    

def add_words_to_genre(genre, words):
    
    #words_per_genre = {'Narrative':{'surname':'[Andersson], 'country:'[Africa, 'Sweden']'}, 'Argumentative':{'city':'[Panama'], 'firstname':['Anna', 'Mohammed']}}
    
    words_per_label = {}
    
    for line in words:
        print(line)
        l, word = line.split(': ')
        label = l.split()[1]
        
        print(label, word)
        
        if label not in words_per_label:
            print([word])
            print(type([word]))
            words_per_label[label] = [word]
            print(words_per_label[label])
        else:
            print(words_per_label[label])
            words_per_label[label].append(word)
            print(words_per_label[label])
            
        if genre not in words_per_genre:
            words_per_genre[genre] = words_per_label
        else:
            words_per_genre[genre][label] = word
            
    
    #Split on colon to get a dict of label:word


def add_labels_to_genre(genre):
            
    #What is labels here?! Is it the labels in the main method? Why don't I have to send it as an argument?
    #Do a test, print and see if the labels in here are the same as the one from the idenficaction run! 
            
    if genre not in labels_per_genre:
        #print("Adding new genre:")
        labels_per_genre[genre] = labels
        #print(labels_per_genre)
    else:
        #print("Genre exists - adding new labels")
        genre_labels = labels_per_genre[genre]
        for label in labels:
            if label in genre_labels:
                labels_per_genre[genre][label] += labels[label]
            else:
                labels_per_genre[genre][label] = labels[label]    
                
                
def print_statistics():
    print('\n')        
    print("Statistics:")
    print('\n')        
    for genre in labels_per_genre:
        print(genre)
        for l in labels_per_genre[genre]:
            print(l, '\t', labels_per_genre[genre][l])    
        print('\n')

    for g in wordlists_per_genre:
        print(g, wordlists_per_genre[g])
        
    '''    
    for genre in words_per_genre:
        print(genre)
        for lex in words_per_label[genre]:
            for label in lex:
                print(label)
                print(lex[label])
                print('\n')
        print('\n')
    '''

parser = argparse.ArgumentParser(description='Program takes a module as input')
parser.add_argument('--input', '-i', type=str, required=True)
parser.add_argument('--postagging', '-pos', type=str, required=True) #Use of pos tagging, can be on or off
parser.add_argument('--limit', '-limit', type=int, default=None)
parser.add_argument('--exception', '-exc', type=str, required=True, default=None) #Use of excepting certain genres, can be on or off
args = parser.parse_args()
#Example run: python main_evaluation.py -i few_essays -pos on -limit 10 -exc off


if __name__ == '__main__':
 
    current_directory = os.getcwd()
    #print(current_directory)
    
    for f in glob.glob(current_directory+'/'+args.input+'/*.json'):
        print(f)
    
        #Getting genre
        fname, suffix = f.split('.')
        genrecode = fname[-3:]
        genre = genres[genrecode]
        
        #print(genre)
        
        #Check if the genre should be excepted from pseudonymization
        if args.exception.lower() == 'off' or (args.exception.lower() == 'on' and genre not in exceptions):
    
            with open(f) as json_data:
                #Load json input
                data = json.load(json_data)

            #Extract plain text from json source
            plain_source_text = json_to_text.extract_data(data, args.limit) #returns a string

            if args.postagging.lower() == 'on':
                #Annotate plain source text with POS tags
                annotated_data = sparv_annotation.annotate(plain_source_text) #returns a list of sentences
                        
                #Anonymize the POS annotated data
                output_data, labeled_words = sparv_identification.identify(plain_source_text, annotated_data)

                print(genre)
                print(labeled_words)
                print('\n')
                add_wordlists_to_genre(genre, labeled_words)

            elif args.postagging.lower() == 'off':
                #Anonymize data without POS annotation
                output_data = identification.identify(plain_source_text)
            else:
                print("Pos arguments must be 'on' or 'off'")
            
            #Evaluate 
            #genrecode, labels = evaluation.evaluate(output_data, f) #then you could send genre as argument here instead of repeating it in that code
            labels = evaluation.evaluate(output_data, genre)
                    
            #Getting genre
            #genre = genres[genrecode] #and this can be removed
            
            '''
            print(genre)
            print(labels)
            '''
            
            #If there are more than one genre assigned to an essay, add the labels for all genres
            #This might be optional? 
            if ',' in genre:
                #print("Several genres")
                sev_genres = genre.split(', ')
                for g in sev_genres:
                    add_labels_to_genre(g)
                    #add_words_to_genre(g, labeled_words)                    
            else:
                #print("A single genre")
                add_labels_to_genre(genre)
                #add_words_to_genre(genre, labeled_words)

        else:
            print("Genre excepted for pseudonymization")

    print_statistics()

