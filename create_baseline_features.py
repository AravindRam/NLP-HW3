from collections import namedtuple
import csv
import sys
import glob
import os
import re

def get_utterances_from_file(dialog_csv_file):
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    with open(os.getcwd()+"/"+dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

DialogUtterance = namedtuple("DialogUtterance", ("act_tag", "speaker", "pos", "text"))

PosTag = namedtuple("PosTag", ("token", "pos"))

def _dict_to_dialog_utterance(du_dict):

    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            continue	#Skipping the iteration if no there are no TOKEN/POS pairs present in an utterance

    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)

#Main Fuction

utterances = get_utterances_from_filename(sys.argv[1])	#Retrieve utterances for each .csv filename passed
line_no =1
speaker_list=[]
output_string=""
for utterance in utterances:				#Iterate through each utterance in the file
	output_string=""
	token_string=""
	pos_string=""
	if(utterance[0]!=""):				#Check if dialog_tag is present or else insert UNKNOWN tag
		dialog_tag = utterance[0]
	else:
		dialog_tag = "UNKNOWN"
	speaker = utterance[1]				
	if(line_no == 1 or line_no == 2):
		speaker_list.append(speaker)
	else:
		speaker_list.pop(0)
		speaker_list.append(speaker)

	token_pos_list = utterance[2]		#If utterance does not have token/pos pairs then the list will be empty.
	for token_pos in token_pos_list:	#It will not enter the loop and so it will skip and proceed to the next utterance
		token = token_pos[0]
		pos = token_pos[1]
		token_string+="\tTOKEN_"+token
		pos_string+="\tPOS_"+pos

	output_string+=dialog_tag
	if(line_no == 1):			#Check if it is the first line of the csv file, if so insert a feature f[0] as 1 
		output_string+="\tf[0]=1"			
	if(len(speaker_list)==2 and speaker_list[0] != speaker_list[1]):
		output_string+="\tf[1]=0"	#Check if the speakers have changed in consecutive utterances, if so insert f[1] as 0
	output_string+=token_string		#Add the list of unigram TOKENs present in the utterance
	output_string+=pos_string		#Add the list of unigram POS tags corresponding to the list of tokens before.
	line_no+=1
	sys.stdout.write(output_string+"\n")
sys.stdout.write("\n")				#Insert a newline between 2 conversations(different .csv files)

