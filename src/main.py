from suffix_tree import SuffixTree
import re          
import dataset

fables = []         #SuffixTree Objects, one object per Story 
string = ''
title = ''
flag = 0

with open("AesopTales.txt", "r") as f:
	for i in f.readlines():
		line = i.strip()
		if len(line) == 0:
			flag = flag-1
			continue
		elif flag == 0 and len(line) != 0:   #title
			fables.append(SuffixTree(string , title, True))
			string = ''
			title = line
			flag = 2
			continue
		elif flag == 1 and len(line) != 0:   #content
			flag = 2
			string += line + ' '
		elif flag == 2:
			string += line + ' '

fables.append(SuffixTree(string , title, True))
del fables[0]
n = len(fables)      #312 stories
print("Number of stories Read : ", n)

#Finds all occurences of a query string in the story in the file
def all_matches(query_string):
	flag = 0
	for i in range (0, len(fables)):
		index = fables[i].find_all_occurences(query_string)
		for j in index:
			if j != -1 :
				flag += 1
				print('Title : ' + fables[i].get_title() + '\t\t Position : ' + str(j)) # returns  the indices at which the query string has occured

				print_sentence(j, i)
	if flag == 0 :
		print('No Match Found!!!')
	

#Finds the 1st Occurence of a query string. If doesnt exist, find the 1st occurence of the longest substring of query string
# Gives the Longest substring and the index of its 1st occurence if found
def first_substring_match(query_string, i):
	flag1 = 0
	start = 0
	end = len(query_string)-1
	for j in range (0, len(query_string)) :
		start = 0
		end = len(query_string)-j-1
		for k in range(len(query_string)-j-1, len(query_string)):
			substr = query_string[start:end+1]
			index = fables[i].find_substring(substr)
			if index != -1:
				flag1 += 1
				ret_list = [substr, index]
				return ret_list
			else:
				start = start+1
				end = end+1
	
	return ['', -1]

		
#Finds and ranks all the documents for a query string by defining some rules
def rank_docs(query_string):
	#rules in comments
	query_words = re.sub(r'[^a-zA-Z ]', '', query_string).split()
	scores = {}               # {Title : score}
	for i in range (0, len(fables)):
		if fables[i].find_substring(query_string) != -1 :
			# If the whole substring is found in the story, score is 150
			scores[fables[i].get_title()] = 150 	
		else :
			scores[fables[i].get_title()] = 0
			n = len(query_words)
			matches = []
			for word in query_words : 
				index = fables[i].find_substring(word)
				if index != -1 :
					matches.append(word)
			if len(matches) == n :
					# If all words in the query string are found, but need not be together, score is 75
				scores[fables[i].get_title()] += 75
			else :

				ret_list = first_substring_match(query_string, i)
				if len(ret_list[0]) > 0.6 * len(query_string) : 
					# If a substring of given string is found and len(substring) >= 0.6*len(Query_string) score = 40
					scores[fables[i].get_title()] += 40
					for word in matches :
						if(len(word) > 3):
						    #If a word with len(word) > 2 has occured multiple times, score += n * 3, n being the number of times it has occured  
							scores[fables[i].get_title()] += 3 * (len(fables[i].find_all_occurences(word))-1)
				else :	
						# If some words in the query are found, score gets added as: (for each matched word), 

					for word in matches :
						if len(word) > 5 :
							#if len(word) > 5  score += 10
							scores[fables[i].get_title()] += 5 * (len(fables[i].find_all_occurences(word))-1)
							scores[fables[i].get_title()] += 10
						elif len(word) > 2 :
					        #if len(word) > 2  score += 5
							scores[fables[i].get_title()] += 3 * (len(fables[i].find_all_occurences(word))-1)
							scores[fables[i].get_title()] += 5
						else :
					        #if len(word) < 2  score += 1 
							scores[fables[i].get_title()] += 1
				
	relevant_stories = sorted(scores.items(), key=lambda x:x[1]) 	#documents are sorted according to their scores and titles are printed   
	n = len(relevant_stories)
	for i in range (0, 10) :         # printing top 10 score stories
		print("(Title , score) : " , relevant_stories[n-i-1])

def print_sentence(index, i):
	if index == -1 :
		return
	start = 0
	end = 0
	if index-20 > 0 :
		start = index-20
	if index+15 < len(dataset.data[i][2]) :
		end = index+20
	else:
		end = len(dataset.data[i][2])-1
	print("Sentence : ", dataset.data[i][2][start:end])
	print("\n")

# Main 
ch = 'y'
while ch == "y" or ch == "Y" :
	print("1. Find All occurences of a Query string \n2. Find the First occurence of a substring of given Query string \n3. Rank documents for the given Query string \nChoose from above")
	choice = int(input().strip())
	
	if choice == 1 :
		print('Give a query string : ')
		query_string = input().strip()
		all_matches(query_string)
			
	
	elif choice == 2 :
		print('Give a query string : ')
		query_string = input().strip()
		for i in range (0,n):
			ret_list = first_substring_match(query_string, i)
			if ret_list[1] != -1:
				print('Title : {0:>18}\t\tPosition : {1:>4}\t\tSubstring : {2:>4}'.format(fables[i].get_title(), str(ret_list[1]), ret_list[0]) )
				print_sentence(ret_list[1], i)
	
	elif choice == 3 :
		print('Give a query string : ')
		query_string = input().strip()
		rank_docs(query_string)
			
	print('Continue? (y/n)')
	ch = input().strip()

