# Modules
import nltk
import argparse, json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

'''        
methods: GET, POST
parameters:
text (required)
settings, default: settings returned from https://ws.spraakbanken.gu.se/ws/sparv/v2/schema
language, default: sv
mode, default: plain, options: plain, xml, file
incremental, default: False
examples:
https://ws.spraakbanken.gu.se/ws/sparv/v2/?text=En+exempelmening+till+nättjänsten
curl -X POST --data-binary text="En exempelmening till nättjänsten" https://ws.spraakbanken.gu.se/ws/sparv/v2/

Example result:

b'<result>\n<build hash=\'3903951c5614955bfa900c81dd91f69a5c4524c1\'/>\n<corpus link=\'https://ws.spraakbanken.gu.se/ws/sparv/v2/download?hash=3903951c5614955bfa900c81dd91f69a5c4524c1\'>\n<text lix="20.69" ovix="40.65" nk="0.80">\n<paragraph>\n<sentence id="8f74-8c25">\n<w pos="PN" msd="PN.UTR.SIN.DEF.SUB" lemma="|jag|" lex="|jag..pn.1|" sense="|jag..1:-1.000|" complemgram="|" compwf="|" ref="01" dephead="02" deprel="SS">Jag</w>\n<w pos="VB" msd="VB.PRS.AKT" lemma="|sakna|" lex="|sakna..vb.1|sakna..vb.2|" sense="|sakna..1:0.761|sakna..2:0.239|" complemgram="|" compwf="|" ref="02" dephead="05" deprel="MS">saknar</w>\n<w pos="PS" msd="PS.UTR.SIN.DEF" lemma="|jag|" lex="|jag..pn.1|" sense="|jag..1:-1.000|" complemgram="|" compwf="|" ref="03" dephead="05" deprel="DT">min</w>\n<w pos="NN" msd="NN.UTR.SIN.IND.NOM" lemma="|mamma|" lex="|mamma..nn.1|" sense="|mamma..1:-1.000|" complemgram="|" compwf="|" ref="04" dephead="05" deprel="CJ">mamma</w>\n<w pos="KN" msd="KN" lemma="|och|" lex="|och..kn.1|" sense="|och..1:-1.000|" complemgram="|" compwf="|" ref="05" dephead="07" deprel="DT">och</w>\n<w pos="NN" msd="NN.UTR.SIN.IND.NOM" lemma="|pappa|" lex="|pappa..nn.1|" sense="|pappa..1:-1.000|" complemgram="|" compwf="|" ref="06" dephead="07" deprel="CJ">pappa</w>\n<w pos="KN" msd="KN" lemma="|men|" lex="|men..kn.1|" sense="|men..1:-1.000|" complemgram="|" compwf="|" ref="07" dephead="" deprel="ROOT">men</w>\n<w pos="PN" msd="PN.UTR.SIN.DEF.SUB" lemma="|jag|" lex="|jag..pn.1|" sense="|jag..1:-1.000|" complemgram="|" compwf="|" ref="08" dephead="09" deprel="SS">jag</w>\n<w pos="VB" msd="VB.PRS.AKT" lemma="|bo|" lex="|bo..vb.1|" sense="|bo..1:-1.000|" complemgram="|" compwf="|" ref="09" dephead="07" deprel="MS">bor</w>\n<w pos="AB" msd="AB" lemma="|h\xc3\xa4r|" lex="|h\xc3\xa4r..ab.1|" sense="|h\xc3\xa4r..1:-1.000|" complemgram="|" compwf="|" ref="10" dephead="09" deprel="HD">h\xc3\xa4r</w>\n<w pos="PP" msd="PP" lemma="|med|" lex="|med..pp.1|" sense="|med..1:-1.000|med..2:-1.000|" complemgram="|" compwf="|" ref="11" dephead="09" deprel="OA">med</w>\n<w pos="PS" msd="PS.UTR.SIN.DEF" lemma="|jag|" lex="|jag..pn.1|" sense="|jag..1:-1.000|" complemgram="|" compwf="|" ref="12" dephead="13" deprel="DT">min</w>\n<w pos="NN" msd="NN.UTR.SIN.IND.NOM" lemma="|pojkv\xc3\xa4n|" lex="|pojkv\xc3\xa4n..nn.1|" sense="|pojkv\xc3\xa4n..1:-1.000|" complemgram="|pojke..nn.1+v\xc3\xa4n..nn.1:4.339e-10|pojk..nn.1+v\xc3\xa4n..nn.1:4.339e-10|" compwf="|pojk+v\xc3\xa4n|" ref="13" dephead="11" deprel="PA">pojkv\xc3\xa4n</w>\n<w pos="MAD" msd="MAD" lemma="|" lex="|" sense="|" complemgram="|" compwf="|" ref="14" dephead="07" deprel="IP">.</w>\n</sentence>\n</paragraph>\n</text>\n</corpus>\n</result>\n'
(base) Sandras-MBP:sparv sandra$ 

'''

def getData(sentence):
    
    #print("getting data from url")
    
    url = 'https://ws.spraakbanken.gu.se/ws/sparv/v2/'
    values = {'text':sentence}

    d = urllib.parse.urlencode(values)
    d = d.encode('utf-8')
    req = urllib.request.Request(url, d)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    #print(respData)
    return respData
    
    
def parseXML(data):
    
    #print("parsing XML")

    words_with_pos = []
    root = ET.fromstring(data)
        
    for w in root.iter('w'):
        attributes = w.attrib
        pos = attributes['pos']
        words_with_pos.append(w.text+'//'+pos)
        
    new_sentence = ' '.join(words_with_pos)
    
    #print(new_sentence)
    return new_sentence
        
        
# Main function annotate the data with POS tags from Sparv
def annotate(data):
        
    #print("Annotating...")
    
    new_sentences = []
    
    data = nltk.sent_tokenize(data)
    #print(data)
    
    for line in data:
        annotated = getData(line)
        parsed_sentence = parseXML(annotated)
        new_sentences.append(parsed_sentence)
                
    #new_text = ' '.join(new_sentences)
    
    #print(new_text)
    return new_sentences #returning list so that you don't have to tokenize it again in the next step
    
if __name__ == '__main__':
    
    output_data = annotate(data)
    
