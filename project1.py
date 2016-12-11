import json
import numpy
import csv
from collections import Counter
import re
from string import punctuation
import string
import sys
import matplotlib.pyplot as plt
import datetime
import time
from pprint import pprint
import re

def read_stocktwits():
	#with open('BAC.json') as read_stocktwits: 
	f = open('BAC.json','r')
	json.text = f.read()   
	data = json.loads(json.text)
	print data
	
	tweet = []
	
	for i in data:
		a = i["created_at"].values()[0]
		a = datetime.datetime.fromtimestamp(a/1000).strftime('%Y-%m-%d %H:%M:%S')
		
		b = i["body"]
		b = b.encode("ascii","ignore")
		b = b.lower()
		b = b.translate(string.maketrans("",""),string.punctuation)
		c = i["entities"]["sentiment"]
		if c is None:
			c = "Unknown"
		else:
			c = i["entities"]["sentiment"]["basic"]
			c = c.encode("ascii","ignore").lower()
		tweet.append([a,b,c])
	print tweet
	
	file = open("myBAC.csv","w")
	for j in tweet:
		j = ",".join(j)
		j = j.replace("\n","")
		j = j + "\n"
		file.write(j)
	file.close()
	return
		
def sentiment_analysis():
	
	##Opening csv file
	f = csv.reader(open('myBAC.csv','rb'))
	
	
	##Creating sentiment dictionary 
	sentimentDict = {
    	'positive': {},
    	'negative': {}
   	}
   	
   	##Creating empty list
   	lis = []
   	##Opening positive words text and putting it into a dictionary
	p = open('positive_words.txt','r')
	for line in p:
		sentimentDict['positive'][line.strip()] = 1
		#print line
	p.close()
	
	##Opening negative words text and putting it into a dictionary
	n = open('negative_words.txt','r')
	print n
	for line in n:
		sentimentDict['negative'][line.strip()] = 1
	#print n
	n.close()
	
	for row in f:
		if row[2] =="Unknown":
			#print row
				pcount = 0
				ncount = 0
				words = row[1].split()
				for w in words:
					if w in sentimentDict['positive']:
						pcount +=1
						#print pcount
					elif w in sentimentDict['negative']:
						ncount +=1
						#print ncount
				if pcount==ncount:
					row[2] = string.replace(row[2],'Unknown','Neutral')
					#print row[2]
				elif pcount < ncount:
					row[2] = string.replace(row[2],'Unknown','Bearish')
				elif pcount > ncount:
					row[2] = string.replace(row[2],'Unknown', 'Bullish')
				lis.append([row[0],row[2].title()])
		else:
			lis.append([row[0],row[2].title()])
		##Writing csv file
	file = open("myBAC2.csv","w")
	for j in lis:
		j = ",".join(j)
		j = j + "\n"
		file.write(j)
	file.close()
	return

def get_sentiment_dates(start_date, end_date):
	
    ##Creating dictionaries
	positive_dict = {} 
	negative_dict = {}
	neutral_dict = {}
    
  	## Formatting end and start date
	start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
	 
    ##reading csv file
	with open('BAC2.csv','r') as f:
		r = csv.reader(f)
		for row in r:
			date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
			if (date >= start) & (date<= end):
				date = date.date()
				sentiment = row[1]
				if sentiment == "Bullish":
					if positive_dict.has_key(date):
						positive_dict[date] = positive_dict[date] + 1
					else:
						positive_dict[date] = 1
				elif sentiment == "Bearish":
					if negative_dict.has_key(date):
						negative_dict[date] = negative_dict[date] + 1
					else:
						negative_dict[date] = 1
				else:
					if neutral_dict.has_key(date):
						neutral_dict[date] = neutral_dict[date] + 1 
					else: 
						neutral_dict[date] = 1
		
	print [positive_dict,negative_dict,neutral_dict]
	return [positive_dict,negative_dict,neutral_dict]
	
	
def drawing_pie(start_date, end_date):
	l = get_sentiment_dates(start_date,end_date)
	mylabels = 'Positive','Negative','Neutral'
	mycolors = 'red','green', 'blue'
	
	sum = []
	for i in l:
		t = sum(i.values())
		sum.append(t) 
	
	plt.pie(x = sum,labels = mylabels, colors = mycolors, autopct = '%1.1f%%',shadow = TRUE)
	plt.axis('equal')
	plt.suptitle("Sentiment is Positive")
	plt.show()
	return

def make_tuple(dict):
    fl = []
    for k in dict.keys():
        listTupleI = (k,dict[k])
        fl.append(listTupleI)
    return fl

def drawing_lines(start_date, end_date):
	#Changing the tuple to array
	rl = np.array(p, dtype = [('date',datetime.date),('count',int)])
	rl = rl.view(np.recarray)
	
	
	fl = get_sentiment_dates(start_date,end_date)
	pos = make_tuple(fl[0])
	neg = make_tuple(fl[1])
	neut = make_tuple(fl[2])
	
	pos = rl(pos)
	neg = rl(neg)	
	neut = rl(neut)
	
	pos.sort()
	neg.sort()
	neut.sort()
	
	##Plotting
	fx = plt.subplots()
	pos_plt = ax.plot(pos.date, pos.count, 'o-', label = 'Positive')
	neg_plt = ax.plot(neg.date, neg.count, 'o-', label = 'Negative')
	neut_plt = ax.plot(neut.date, neut.count, 'o-', label = 'Neutral')
	plt.legend(handles=[pos_plt,neg_plt,neut_plt],labels = ['Positive','Negative','Neutral'])
	plt.suptitle("Sentiment between " + start_date + " and " + end_date,fontsize=10)
	fig.autofmt_xdate()
	
	plt.show()
	return

def main():
    read_stocktwits()# output: BAC.csv
    sentiment_analysis()
    get_sentiment_dates('2013-01-02', '2013-01-31')#output:[{datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 44, datetime.date(2013, 1, 6): 31, datetime.date(2013, 1, 4): 63, datetime.date(2013, 1, 2): 108, datetime.date(2013, 1, 23): 41, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 25, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 11, datetime.date(2013, 1, 17): 153, datetime.date(2013, 1, 10): 75, datetime.date(2013, 1, 31): 19, datetime.date(2013, 1, 8): 66, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 6, datetime.date(2013, 1, 25): 25, datetime.date(2013, 1, 7): 79, datetime.date(2013, 1, 5): 27, datetime.date(2013, 1, 3): 60, datetime.date(2013, 1, 22): 44, datetime.date(2013, 1, 15): 45, datetime.date(2013, 1, 20): 7, datetime.date(2013, 1, 13): 14, datetime.date(2013, 1, 18): 59, datetime.date(2013, 1, 11): 52, datetime.date(2013, 1, 16): 66, datetime.date(2013, 1, 9): 137, datetime.date(2013, 1, 30): 19, datetime.date(2013, 1, 28): 23}, {datetime.date(2013, 1, 26): 3, datetime.date(2013, 1, 24): 20, datetime.date(2013, 1, 6): 5, datetime.date(2013, 1, 4): 24, datetime.date(2013, 1, 2): 27, datetime.date(2013, 1, 23): 18, datetime.date(2013, 1, 21): 2, datetime.date(2013, 1, 14): 18, datetime.date(2013, 1, 19): 1, datetime.date(2013, 1, 12): 2, datetime.date(2013, 1, 17): 70, datetime.date(2013, 1, 10): 37, datetime.date(2013, 1, 31): 10, datetime.date(2013, 1, 8): 39, datetime.date(2013, 1, 29): 11, datetime.date(2013, 1, 27): 1, datetime.date(2013, 1, 25): 4, datetime.date(2013, 1, 7): 33, datetime.date(2013, 1, 5): 6, datetime.date(2013, 1, 3): 8, datetime.date(2013, 1, 22): 24, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 4, datetime.date(2013, 1, 18): 36, datetime.date(2013, 1, 11): 17, datetime.date(2013, 1, 16): 22, datetime.date(2013, 1, 9): 124, datetime.date(2013, 1, 30): 12, datetime.date(2013, 1, 28): 6}, {datetime.date(2013, 1, 26): 4, datetime.date(2013, 1, 24): 15, datetime.date(2013, 1, 6): 9, datetime.date(2013, 1, 4): 40, datetime.date(2013, 1, 2): 63, datetime.date(2013, 1, 23): 34, datetime.date(2013, 1, 21): 4, datetime.date(2013, 1, 14): 19, datetime.date(2013, 1, 19): 6, datetime.date(2013, 1, 12): 12, datetime.date(2013, 1, 17): 148, datetime.date(2013, 1, 10): 51, datetime.date(2013, 1, 31): 13, datetime.date(2013, 1, 8): 49, datetime.date(2013, 1, 29): 18, datetime.date(2013, 1, 27): 3, datetime.date(2013, 1, 25): 15, datetime.date(2013, 1, 7): 77, datetime.date(2013, 1, 5): 7, datetime.date(2013, 1, 3): 40, datetime.date(2013, 1, 22): 37, datetime.date(2013, 1, 15): 21, datetime.date(2013, 1, 20): 4, datetime.date(2013, 1, 13): 6, datetime.date(2013, 1, 18): 48, datetime.date(2013, 1, 11): 40, datetime.date(2013, 1, 16): 49, datetime.date(2013, 1, 9): 104, datetime.date(2013, 1, 30): 26, datetime.date(2013, 1, 28): 15}]
    #As you can see in the output, I used datetime.date objects as keys of a dictionary. You can also do this, you can use date strings as keys.
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png - you can see a graph in a pop-up window. you don't need to save the graph
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return

if __name__ == '__main__':
    main()
