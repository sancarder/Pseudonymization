# Modules
import argparse, json
import sparv_annotation
import sparv_identification

#This is the starting file for Sparv annotation

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

parser = argparse.ArgumentParser(description='Program takes an input and output text file together with output formats')
parser.add_argument('--input', '-i', type=str, required=True)
parser.add_argument('--output', '-o', type=str, required=True)
parser.add_argument('--exception', '-exc', type=str, required=True, default=None) #Use of excepting certain genres, can be on or off
args = parser.parse_args()
#Example run: python sparv_main_file.py -i essay.txt -exc off -o output.txt

if __name__ == '__main__':
        
    # Getting genre
    # This approach needs the file name to contain the genre information
    # Perhaps we need to find another way of getting it for other files
    filename, suffix = args.input.split('.')
    genrecode = filename[-3:]
    genre = genres[genrecode]
        
    print(genre)
        
    #Check if the genre should be excepted from pseudonymization
    if args.exception.lower() == 'off' or (args.exception.lower() == 'on' and genre not in exceptions):
        
        # Read input file, only text file
        with open(args.input) as inputfile:
            data = inputfile.read()
        
        # If json format should be accepted, we need to add code here
        # Then, we need to dump the json file and call json_to_text to extract the plain text
        # In main_evaluation there is code for this that we can reuse
        
        annotated_data = sparv_annotation.annotate(data) #returns a list of sentences
        output_data = sparv_identification.identify(data, annotated_data)
        
        # Save the output to the path in args.output
        if args.output:
            with open(args.output, 'w') as outputfile:

                json.dump(output_data, outputfile)
                #outputfile = open(args.output, 'w')
                #outputfile.write(output_data)            
                
    else:
        print("Genre excepted for pseudonymization")

            
