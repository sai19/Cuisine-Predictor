from __future__ import division
from collections import Counter
import pandas as pd
#read the train file 
data_total = pd.read_json("/media/sai/New Volume1/Practice/cuisine_predictor/train/train.json");
data = data_total.head(int(0.8*len(data_total)));
check = data['ingredients'];
#read all the cuisine types in the data
cuisine_types = data['cuisine'].unique()
#create a dictionary that contains the ingredients of each cuisine	
ingr_dict_indiv = {};
ingr_dict_group = {};
for cuisine in cuisine_types:
	# filter the data such that resulting data contains only 
	# the current cuisines
	cuisine_data = data[data['cuisine']==cuisine];
	ingr = cuisine_data['ingredients'];
	# get all the ingredients that the cuisine uses
	cuisine_ingr = [];
	cuisine_ingr_group = [];
	for a in ingr:
		if a not in cuisine_ingr_group:
			cuisine_ingr_group.append(a);
		for item in a:
			if item not in cuisine_ingr:
				cuisine_ingr.append(item);				
	ingr_dict_indiv[cuisine] = cuisine_ingr;
	ingr_dict_group[cuisine] = cuisine_ingr_group;

a  = data_total.tail(int(0.1*len(data_total)))
correct =0;
incorrect = 0;
count =0;
for index,row in a.iterrows():
	probable_cuisines_indiv = [];
	probable_cuisines_group = [];	
	match_index = 0;
	count = count+1;
	print count;		
	for key,ingredient in ingr_dict_group.items():
		for item in ingredient:
			inter = set(row['ingredients'])&set(item);
			if(len(inter)>match_index):
				match_index = len(inter);
				match = key;	
	#print match_index,match,row['cuisine'];
	print "\n"
	if(match==row['cuisine']):
		correct = correct+1;		
	else:
		incorrect = incorrect +1;
	#print "\n"	
	'''	
	for item in row['ingredients']:
		for key,ingredient_list in ingr_dict_indiv.items():
			if item in ingredient_list:
				probable_cuisines_indiv.append(key);
	most_freq = Counter(probable_cuisines_indiv);
		#for key,count in most_freq:
		
	print max(most_freq),row['cuisine']+": ",most_freq[row['cuisine']],
	print "\n"	
	
	if(len(probable_cuisines_group)!=0):
		if (max(set(probable_cuisines_group), key=probable_cuisines_group.count) == row['cuisine']):
			correct = correct +1;
		else:
			incorrect = incorrect + 1;	
	else:	
		if (max(set(probable_cuisines_indiv), key=probable_cuisines_indiv.count) == row['cuisine']):
			correct = correct +1;
		else:
			incorrect = incorrect + 1;
'''
print correct/(correct+incorrect);				

