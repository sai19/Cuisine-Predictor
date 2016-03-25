from __future__ import division
from collections import Counter
from sklearn.preprocessing import LabelEncoder;
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def normalize_word(word):
	word = word.replace("(","");
	word = word.replace(")","");
	word = word.replace("'","")
	word = word.lower();
	return(word);
#read the train file 
data_total = pd.read_json("/media/sai/New Volume1/Practice/cuisine_predictor/train/train.json");
data = data_total.head(int(0.9*len(data_total)));
	check = data['ingredients'];
#read all the cuisine types in the data
cuisine_types = data['cuisine'].unique()
#create a dictionary that contains the ingredients of each cuisine	
ingr_dict_indiv = {};
ingr_dict_group = {};
ingr_dict_unique = {};
ingr_all = [];
train_data = data_total.head(int(0.9*len(data_total)));
le = LabelEncoder();
cv = CountVectorizer();
train_X = train_data['ingredients'];
train_X = [' '.join(v) for v in train_X]
train_Y = train_data['cuisine'];
train_X = cv.fit_transform(train_X).toarray();
train_Y = le.fit_transform(train_Y);
rf_classifier = RandomForestClassifier()
rf_classifier.fit(train_X, train_Y)
for item in check:
	for a in item:
		a = a.split(" ");
		for word in a:
			word = normalize_word(word);
			ingr_all.append(word);
most_common = Counter(ingr_all).most_common(100);
most_common = [key for key,freq in most_common];
for cuisine in cuisine_types:
	# filter the data such that resulting data contains only 
	# the current cuisines
	cuisine_data = data[data['cuisine']==cuisine];
	ingr = cuisine_data['ingredients'];
	# get all the ingredients that the cuisine uses
	cuisine_ingr = [];
	cuisine_ingr_group = [];
	for content in ingr:
		if content not in cuisine_ingr_group:
			cuisine_ingr_group.append(content);
		for item in content:
			item = item.split(" ");
			for word in item:
				word = normalize_word(word);
				if word not in (most_common):
					cuisine_ingr.append(word);					
	ingr_dict_indiv[cuisine] = cuisine_ingr;
	ingr_dict_group[cuisine] = cuisine_ingr_group;

for key,ingredients in ingr_dict_indiv.items():
	a = set([]);
	for other,ingr_other in ingr_dict_indiv.items():
		if(key!=other):
			a = a | (set(ingredients)&set(ingr_other));
	ingr_dict_unique[key]= set(ingredients) - a;	
a  = data_total.tail(int(0.1*len(data_total)))
correct =0;
incorrect = 0;
count =0;

for index,row in a.iterrows():
	count = count+1;
	print count,	
	match_index = 0;
	ingredient = [];
	test = [];
	test = [' '.join(row['ingredients'])];
	found  = False;
	for line in row['ingredients']:
		line_split = line.split(" ");
		ingredient = ingredient +line_split;
	probable_match = [];
	unique_match = [];
	match = "not found"
	for key,ingredient_list in ingr_dict_group.items():
		if row['ingredients'] in ingredient_list:
			match = key;
			found = True;
			break;	
	
	if(found==False):	
		for key,ingredient_list in ingr_dict_indiv.items():		
			for word in ingredient:			
				word = normalize_word(word);	
				if word in ingr_dict_unique[key]:
					unique_match.append(key);	
		unique_best = Counter(unique_match);
		if(len(unique_match)!=0):
			match = max(unique_best, key=unique_best.get);
			found = True;		
		#else:		
			#test = cv.transform(test).toarray();
			#Y = rf_classifier.predict(test);
			#match = le.inverse_transform(Y); 			
	if(found==True):	
		if(match==row['cuisine']):
			correct = correct+1;
			print 1,
		else:
			incorrect = incorrect +1;
			print 0,
		print "\n";
print correct/(correct+incorrect);						
