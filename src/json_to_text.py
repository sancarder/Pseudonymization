# Modules
import json

def extract_data(data, limit):
    
    words = []
    
    for id in data['source']:
        word = (id['text'])
        
        #If a limitation is specified by the user, extract this number of word
        if limit != None:
            if len(words) < limit:
                words.append(word)
        else:        
            words.append(word)
        
    text = ''.join(words)
    text = text.replace(' ,', ',')
    text = text.replace(' .', '.')

    return text


if __name__ == '__main__':
            
    extracted_data = extract_data(data, limit=None)
          
