# Modules
import json
import glob
import os
import argparse

import json_to_text
import sparv_annotation
import sparv_identification
import identification

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


def count_occurrences_per_label(target_text, genre): 
    
    # Looks at the anonymized text, count the occurrences, records the labels and outputs the result (number of occurrences for each label for that document)
        
    labels = {}
    
    # data is a list. It consists of lists (sentences). Those lists consists of dicts (string:label). 
    for sentence in target_text:
        for word in sentence:
            labellist = word['label']
            if labellist != []:
                label = labellist[0]
                if label in labels:
                    labels[label] += 1
                else:
                    labels[label] = 1

    return labels


def add_wordlists_to_genre(genre, wordlist):
    
    # Adds the labeled words found in the file's genre
    # Used for quick analysis of which words are detected
            
    if genre not in wordlists_per_genre:
        wordlists_per_genre[genre] = wordlist
            
    else:
        wordlists_per_genre[genre] += wordlist
                

def add_labels_to_genre(genre, labels):
         
    # Adds the labels found for the file's genre
    # Used for statistics
                 
    if genre not in labels_per_genre:
        labels_per_genre[genre] = labels

    else:
        genre_labels = labels_per_genre[genre]
        
        for label in labels:

            if label in genre_labels:
                labels_per_genre[genre][label] += labels[label]

            else:
                labels_per_genre[genre][label] = labels[label]    
                
                
def print_statistics():
    
    # Prints statistics to the terminal
    
    print('\n')        
    print("Statistics:")
    print('\n')        
    
    
    for genre in labels_per_genre:
        # Print each genre and its labels with number of occurrences
        print(genre)
        for l in labels_per_genre[genre]:
            print(l, '\t', labels_per_genre[genre][l])    
        print('\n')

    for g in wordlists_per_genre:
        # Prints the words detected for each genre and their labels
        print(g, wordlists_per_genre[g])
        print('\n')
        
        
def write_statistics(output):
    
    # Writes statistics to the given output file
    
    with open(output, 'w') as resultfile:
    
        resultfile.write("Statistics:" + '\n')
        resultfile.write('\n')        

        for genre in labels_per_genre:            
            # Writes each genre and its labels with number of occurrences
            resultfile.write(genre+'\n')
            for l in labels_per_genre[genre]:
                resultfile.write(l + '\t' + str(labels_per_genre[genre][l]) +'\n')    
            resultfile.write('\n')

        for g in wordlists_per_genre:
            # Writes the words detected for each genre and their labels
            resultfile.write(g+'\n')
            outer_list = wordlists_per_genre[g]
                          
            for w in outer_list:
                resultfile.write(w+'\n')
            resultfile.write('\n')
        

parser = argparse.ArgumentParser(description='Program takes a module as input')
parser.add_argument('--input', '-i', type=str, required=True)
parser.add_argument('--output', '-o', type=str, required=True)
parser.add_argument('--postagging', '-pos', type=str, required=True) #Use of pos tagging, can be on or off
parser.add_argument('--limit', '-limit', type=int, default=None)
parser.add_argument('--exception', '-exc', type=str, required=True, default=None) #Use of excepting certain genres, can be on or off
args = parser.parse_args()
#Example run: python main_evaluation.py -i few_essays -pos on -limit 10 -exc off


if __name__ == '__main__':
 
    current_directory = os.getcwd()    
    counter = 1
    
    for f in glob.glob(current_directory+'/'+args.input+'/*.json'):
        print(counter, f)
    
        #Getting genre
        fname, suffix = f.split('.')
        genrecode = fname[-3:]
        genre = genres[genrecode]
                
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
                
                add_wordlists_to_genre(genre, labeled_words)
                

            elif args.postagging.lower() == 'off':
                #Anonymize data without POS annotation
                output_data = identification.identify(plain_source_text)
            else:
                print("Pos arguments must be 'on' or 'off'")
            
            #Count occurrences per label 
            labels = count_occurrences_per_label(output_data, genre)
                                                                                
            #If there are more than one genre assigned to an essay, add the labels for all genres
            if ',' in genre:
                sev_genres = genre.split(', ')
                for g in sev_genres:
                    add_labels_to_genre(g, labels)
            else:
                add_labels_to_genre(genre, labels)
                
        else:
            print("Genre excepted for pseudonymization")

        counter+=1

    #print_statistics()
    write_statistics(args.output)

