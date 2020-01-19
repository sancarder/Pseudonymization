#DIARY

##December 16
Topic for project finalized in agreement with Dana and Elena.
Forked pseudonymization repo into my GitHub.

##January 05
Made up a project plan for how to go on.
Read up on how to use Sparv. 
Test run and went through Samir's code to familiarize me with expected output.
Did a lot of test prints to follow what the code does. Some code in the repo seems to be not used. 
Have possibily detected a few errors in the code. Will check it more properly and make a list of improvements suggestions. 

##January 06
Have decided to first work with POS tags and take NER in a later step, for better evaluation. 
Have made two new python files, one main file for Sparv annotation and one script for the actual annotation code. 
Have worked on understanding Sparv API and used urllib to fetch the data.
Next step is to extract the POS information. I have decided to attach the POS tag to each word separated with double slash //. The double slash is to avoid splitting on real slashes in a text. 
I will write the output like this, and then adapt the functions in the pseudonymization code to use the tags. 

I have now extracted the POS information with the help of the Element Tree method and attached each tag to its word, saved the sentences and written the output to a file. This file is now ready
to be used as input to the pseudonymization steps. 

I have now implemented the POS tags for personal names (only this so far). 
I have done a function that checks a word's pos and returns true if it's the pos PM. 
This is used in all first name checks and the surname checks, and the words that are false are not added to the name lists. This works well so far (few examples tested only). 
Problem detected: Words in the end of a sentence is together with a dot, and the dot prevents the word from being recognized/matches in a sentence. What do to about this, and where? 
Next steps: Implement this also for cities and countries. More categories? 

##January 07
Have sent email to Samir with some questions about input and evaluation, and also about some of the code. Now it's more clear to me how the evaluation could be done. I will run the texts as plain input, then construct an output that is easy to analyze. For each text, I will compare it to the manual evaluation I have gotten access to and compare the number of correct identifications for names, cities and countries. I will also combine statistics for the whole set. 
I have implemented the POS checking for cities and countries. It proved a little trickier to understand this part of the original code. I also detected some questions marks in the code that I will collect and report to Samir and Elena, which may be used for improving further versions. It was also a little trickier to run test examples on cities and countries, but evaluation will show if this improves the pseudonymization at all. Next step: Finish up for cities and countries and possible also street names and professions. 

##January 08
Tried the POS intervention on Swedish cities and street names, but this turns out to be dangerous. Cities are deemed as nouns or verbs (Kisa, Vara, Trosa) in the Sparv annotation. The same is true for 
street names. Single street names will probably be deemd as nouns, and will be found from the list anyway. 
Setting this as a condition will 
prevent the pseudonymizer to find them - as it is now, it will find them. In this case, I think it will be best to not implement Sparv annotation. I also realized that MWE:s are not good to use annotation with. It's difficult to catch the accordingly, and also, the Sparv annotation does not take most of them into consideration as one unit (Papaua Nya Guinesa, Gamla Anneforsvägen). When it comes tp personal names, this doesn't seem to happen (mwes). But for countries, when it's "New York", it will find "York" and annotate that because it loops over a set that is unordered. 

I'm thinking about how to do the evaluation. I want to be able to conpare the table for each genre in the article. This is based on number of tags. The manual numbers and the numbers from the 
running without POS tagging is already there. I think the best way is to do a script separately, which takes as input the anonymized text - or texts, either all at once, or genre by genre or all at once
and then count the tags. This way, I will get the same table. I will do this, and run the original script first, to confirm that I get the right numbers. First, I must extract the original texts from the source of the json files. 

##January 9
I have now done an evaluation script. There's a main file, looping through files in a folder. For each folder, it gets the plain text from the source, POS annotates, anonymizes and evaluates. Finally, it concludes the result per genre. It seems to work pretty well. I have now only tested with 10 files, limiting the number of words to 10 for each file, so that the annotation won't slow it down. Next step is to make sure the printing of the output is accurate (that it collects it accordingly) and readable, and then run it on all full files. Also write the output to a file so that can be reviewed later. Make sure that the text types are collected/listed in the right way (you have to handle cases where an essay has more than one category). Do not collect after "filename" but after the five categories. 

Then run the script without POS tagging, and then make a script to get the same counts per label for the manual encoded essays. Save all those runs in a file so you can compare. 

Run started 21.41 (all essays, all text, POS, no topic switcher). Finished 00.31. 
Run started 01.04 (all essays, all text, no POS, no topic switcher). Finished 01.17. 

Further work: Trye with NER setting in Sparv, and try to extract the result from this. Seems like the words that the NER tagger finds are tagged as a <ne> with additional information. This could be
caught in the annotation step and used in the identification step as a further check? Or will it really enhance results, is't it the same? Perhaps for street names? 

Also, add a topic switcher. Where? In the main file, so that it can condition whether or not you run the rest of the steps (annotation, identification). You already have the file evaluation.py.
It doesn't really evaluate, it just extracts the genre and labels from each file and returns them. Rename it. But it can't be used in the beginning since it needs the pseudonymized data. 
Perhaps take the code for just extracting the topic and do it in the main file instead? And only have the labels extracted in the last step? And use the genre already extracted as input to this method.

Now you have the results from the "just POS tagging". Save them. Then, do a run without the POS tagging and save those results. Then, one with topic switcher WITH POS and one with topic switcher
WITHOUT POS. This is now implemented, and the results are bascially the same as before, just with zeros for the two excepted categories (so a different total). 

OBS! Implement sanity checks/error checks on argparse in main! 

##Jan 10
I have concluded the results for four runs (with/without POS, with/without topic switch). The results are not identical to that in the table in the article. Might have to do with different
pre-processing of texts? Or some kind of conclusion when making the table? Check with Elena. But anyway, the trend of the result can be used anyway. POS tagging lowers the score. 
Next step: make a script that extracts the target labels for the essays. This is the "key"/right answers. Then make a print out of this comparable to your results, and add it to the table for comparison. 

##Jan 13
I have talked to Elena about the confusion around the labels and numbers. The explanation is that it's a work in progress and the script has evolved since this data was compiled, and the manual
annotator used labels that weren't available for automatic tagging, and vice versa. My results show a trend anyway, based on this data and this version of the script. I have now added in even 
the manual results from the article table as references in my table. Next step is to do a quick run to see what words are labeled, to get an overview and a feeling for if it's correct or not 
(precision/recall). Then I will write the report, and further on get the code presentable for submitting to the Swell project to use if they wish. 
