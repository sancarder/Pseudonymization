# Pseudonymization

This repository is based on the fork from https://github.com/SamirYousuf/Pseudonymization

Pseudonymization guidelines from SweLL project are here: https://spraakbanken.github.io/swell-project/Anonymization_guidelines 

Updated implementation is done in the following files: 

* main_evaluation - this code is run to be able to evaluate the code where you can switch on and off both pos tagging and topic selection. It runs on a folder with many files and gives statistics about them
* sparv_main_file - this code is meant to be run in the same way as the original main file, one text essay at a time (in text format - if we want this to work with json files we would have to add some code), it includes topic switching option
* sparv_identification - the identification part with part of speech tag checking implemented
* sparv_annotation - here's where the annotation is made with calls to the Sparv service
* json_to_text - a script that extracts the text from the json files (used only for evaluation at the moment)

## Example runs
python main_evaluation.py -i essay_folder -o output.txt -exc on -pos on -limit None
python sparv_main_file.py -i essay.txt -exc off -o output.txt
