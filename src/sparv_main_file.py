# Modules
import argparse, json
import sparv_annotation
import sparv_identification

#This is the starting file for Sparv annotation

parser = argparse.ArgumentParser(description='Program takes an input and output text file together with output formats')
parser.add_argument('--input', '-i', type=str, required=True)
parser.add_argument('--output', '-o', type=str, required=True)
args = parser.parse_args()

if __name__ == '__main__':
        
    # Read input file, only text file
    with open(args.input) as inputfile:
        data = inputfile.read()
    
    annotated_data = sparv_annotation.annotate(data) #returns a list of sentences
    output_data = sparv_identification.identify(data, annotated_data)
    
    # Save the output to the path in args.output
    if args.output:
        with open(args.output, 'w') as outputfile:

            json.dump(output_data, outputfile)
            #outputfile = open(args.output, 'w')
            #outputfile.write(output_data)            
            
