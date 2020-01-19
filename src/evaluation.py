# Modules
import argparse, json

#evaluate - looks at the anonymized text, count the tags, records the types and outputs the result (number of tags for each tag for that document)

def evaluate(text, genre): #before filename
    
    labels = {}

    #print("Evaluating...")
    
    #fname, suffix = filename.split('.')
    #genre = fname[-3:]

    #data is a list. It consists of lists (sentences). Those lists consists of dicts (string:label). 
    for sentence in text:
        for word in sentence:
            labellist = word['label']
            if labellist != []:
                label = labellist[0]
                if label in labels:
                    labels[label] += 1
                else:
                    labels[label] = 1

    return labels
    #return genre, labels

'''
parser = argparse.ArgumentParser(description='Program takes an json file as input')
parser.add_argument('--input', '-i', type=str, required=True)
args = parser.parse_args()
'''

if __name__ == '__main__':
        
    '''
    with open(args.input) as inputfile:
        data = json.load(inputfile)
    '''
    #genre, labels = evaluate(data, args.input)
    genre, labels = evaluate(data, genre)
    
    
    '''
    print("Genre: " + genres[genre])
    print("Labels: ")
    for label in labels:
        print(label, labels[label])
    '''
