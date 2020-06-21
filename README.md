# IT251 DSa Project on Suffix Trees

## Description
Suffix Tree is constructed in linear time using Ukkonen's algorithm. This tree is used to carry out 3 different applications on a dataset of 312 short stories from Aesop's Fables.

These applications are:
1. Finding all occurences of a string in the stories
2. Find the first occurence of a string. If not found, find the first occurence of the longest substring of of string
3. Find and rank all stories for a given string according to certain rules
   Rules:
   1. If the whole substring is found in a story, score = 150
	 2. If all words in the string are found, (need not be consecutive), score = 75
	 3. If a substring of string is found: 
	     - if len(substring) >= 0.6*len(Query_string), score = 40
	     - Else discard the substring
	 4. If some words in the query are found, for each matched word in the query, 
	     - if len(word) > 5  score += 10
	     - if len(word) > 2  score += 5
	     - if len(word) < 2  score += 1 
	 5. If a word with len(word) > 2 has occured multiple times, score += n * 3, n being the number of times it has occured  
	
## Running the Code
1. Open the folder containing code
2. Open terminal, type python main.py and run
