#Date: 4.3.18
#Purpose: This program will take the blast table from commandline blast and pull out the
#query sequence within the contigs. Will only work for best blast hit to avoid multiple
#dictionary misques 

btable_input = input("\nWhat is the Blast Table file?   ")
fasta_input = input("\nWhat is the Fasta file?   ")
out_input = input("\nWhat is the out file?   ")

#Open Blast Table File and fasta file 
f = open(btable_input,'r')
btable_infile = f.readlines()
f.close() 

g = open(fasta_input,'r')
fasta_infile = g.readlines()
g.close()

#Make a dictionary for each Blast Table Row with the
#key being the query sequence id, and the term being the coordinates
#of start and finish as integers 

#makes each element in a row a separate part of the list
btable_rows = []

for x in btable_infile:
	y= x.strip().split('\t')	#remove white spaces/next lines and separates 
					#as a list by tabs 
	btable_rows.append(y) 

#Make a Dictionary with the key as query search id and the term being [qstart,qend]
#This is what will be used to pull out the proper string 

btable_dictionary = dict() 
key = ""

count = 0

for x in btable_rows:
	count = count + 1
	new_ID = x[0] + "!" + str(count) 
	key = new_ID 
	row_6 = int(x[6])
	row_7 = int(x[7])
	y = []
	#plus strand	
	if row_6 < row_7:
		y.append(row_6) #qstart
		y.append(row_7) #qend
	#minus strand	
	if row_6 > row_7:
		y.append(row_7) #qstart
		y.append(row_6) #qend
	btable_dictionary[key] = y

#make a dictionary from the fasta file, with the key being the fasta header 
#and the term being the sequence as a string 

fasta_dictionary = dict()
key = ""

for x in fasta_infile:
	y = x.strip('\n')
	if y.startswith('>'):
		key = y
		fasta_dictionary[key] = ""
	else:
		fasta_dictionary[key] += y
		
#choose the largest contig length using the fasta_dictionary as the key 

#import defaultdict
from collections import defaultdict

btable_dictionary_by_contig = defaultdict(list) 

#change the name of the contigs, and add to list with coordinates as pos 2
by_contig = []

for x in fasta_dictionary:
	contig_name = x.strip('>')
	for y in btable_dictionary:
		split_y = y.split('!')
		if contig_name == split_y[0]:
			z = []
			z.append(x)
			z.append(btable_dictionary[y])
			by_contig.append(z)

#add all coordinates to a single defaultdictionary 
for x,y in by_contig:
	btable_dictionary_by_contig[x].append(y) 

#pick the fragment of the contig by taking the 
#smallest starting point, and largest end point
#that was hit by blast 
btable_dictionary_final = dict() 
for x in btable_dictionary_by_contig:
	starts = []
	ends = []
	for y in btable_dictionary_by_contig[x]:
		starts.append(int(y[0]))
		ends.append(int(y[1]))
	coordinates_final = [min(starts),max(ends)]
	btable_dictionary_final[x] = coordinates_final
		
#Using the blast table dictionary, screen against the fasta dictionary
#if the query search id is found within the fasta dictionary key 
#the qstart and qend will be used to trim the sequence, and then added
#to a the output dictionary with the same header + trimmed 

out_fasta_dictionary = dict() 

for x in btable_dictionary_final:
	qstart = btable_dictionary_final[x][0]-1
	qend = btable_dictionary_final[x][1]
	for y in fasta_dictionary:
		if x == y:
			new_id = y + ' trimmed'
			sequence = fasta_dictionary[y]
			sequence_trimmed = sequence[qstart:qend]
			out_fasta_dictionary[new_id]= sequence_trimmed

#add in the reading frame to out list from original blast table (column 13)
reading_frame_dict = dict() 

for x in out_fasta_dictionary:
	ID = x.strip('>').strip(' trimmed')
	z = []
	for y in btable_rows:
		if ID == y[0]:
			z.append(int(y[12]))			
	reading_frame_dict[ID] = list(set(z))
	
out_list = []

for x in out_fasta_dictionary:
	z = []
	z.append(x) 
	z.append(out_fasta_dictionary[x])
	for y in reading_frame_dict:
		if y in x:
			z.append(reading_frame_dict[y]) 
	out_list.append(z) 
		
#write to an outfile
import csv

with open(out_input,'w') as h:
	writer = csv.writer(h, delimiter='\t')
	writer.writerows(out_list)
	
quit()
