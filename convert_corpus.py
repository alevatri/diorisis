import sys
from lxml import etree as document
from openpyxl import load_workbook
import configparser
import os
import re
from beta2utf import convertBeta

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
annotated = config['paths']['annotated']
resources = config['paths']['file_list']
dir = config['paths']['output']
TT = config['paths']['treetagger_output']
fc = config['paths']['final_corpus']

wb2 = load_workbook('%s/file_list.xlsx'%resources)
ws2 = wb2.active
headers = ws2[config['excel_range']['headers']]
h_file = {cell.value : n for n, cell in enumerate(headers[0])}
files = ws2[config['excel_range']['range']]

for idx,record in enumerate(files):
	file = '%s/%s'%(annotated,record[h_file['Tokenized file']].value)
	if os.path.isfile('%s/%s'%(fc,record[h_file['Tokenized file']].value)): continue
	curr_text = document.parse(file)
	print("Converting %s"%os.path.basename(file))
	init_tokens = str(len(curr_text.xpath('//word')))
	init_lemmas = str(len(curr_text.xpath('//lemma')))
	sys.stdout.write("\r\033[\tWord tokens: %s, lemmas: %s"%(init_tokens, init_lemmas))
	sys.stdout.flush()
	TT_doc = open('%s/%s'%(TT,record[h_file['Tokenized file']].value.replace('xml','txt')), 'r')
	TT_lines=[x for x in TT_doc]
	nodes = curr_text.xpath('//word|//punct')
	word_count = 0
	for node in nodes:
		if node.tag == 'word':
			lemma_count = len(node.xpath('./lemma'))
			if lemma_count > 1:
				TT_POS = TT_lines[word_count].split('\t')[1].strip()
				try:
					toAdd = node.xpath('lemma[@POS="%s"]'%TT_POS)[0]
					toAdd.set('disambiguated', str(round(1/len(node.xpath('lemma[@POS="%s"]'%TT_POS)),2)))
					toAdd.set('TreeTagger', 'true')
					toRemove = node.xpath('lemma')
					[node.remove(x) for x in toRemove]
					node.append(toAdd)
				except:
					if TT_POS == 'proper':
						TT_POS='noun'
					try:
						toAdd = node.xpath('lemma[@POS="%s"]'%TT_POS)[0]
						toAdd.set('disambiguated', str(round(1/len(node.xpath('lemma[@POS="%s"]'%TT_POS)),2)))
						toAdd.set('TreeTagger', 'true')
						toRemove = node.xpath('lemma')
						[node.remove(x) for x in toRemove]
						node.append(toAdd)
					except:
						TT_POS='adjective'
						try:
							toAdd = node.xpath('lemma[@POS="%s"]'%TT_POS)[0]
							toAdd.set('disambiguated', str(round(1/len(node.xpath('lemma[@POS="%s"]'%TT_POS)),2)))
							toAdd.set('TreeTagger', 'true')
							toRemove = node.xpath('lemma')
							[node.remove(x) for x in toRemove]
							node.append(toAdd)
						except:
							toAdd = node.xpath('lemma')[0]
							toAdd.set('disambiguated', str(round(1/lemma_count, 2)))
							toAdd.set('TreeTagger', 'false')
							toRemove = node.xpath('lemma')
							[node.remove(x) for x in toRemove]
							node.append(toAdd)
			else:
				node.xpath('./lemma')[0].set('TreeTagger', 'false')
				node.xpath('./lemma')[0].set('disambiguated', 'n/a')
			word_count+=1				
		elif node.tag == 'punct':
			word_count+=1
			
	finalXML = document.tostring(curr_text, pretty_print=True, encoding='unicode')
		
	f = open('%s/%s'%(fc,record[h_file['Tokenized file']].value), 'w')
	f.write(finalXML)
	f.close()
	curr_text_check = document.parse('%s/%s'%(fc,record[h_file['Tokenized file']].value))
	final_tokens = str(len(curr_text_check.xpath('//word')))
	final_lemmas = str(len(curr_text_check.xpath('//lemma')))
	sys.stdout.write("\r\033[\tWord tokens: %s, lemmas: %s\tFinal: %s, lemmas:%s\n"%(init_tokens, init_lemmas, final_tokens, final_lemmas))
	sys.stdout.flush()
	if init_tokens != final_tokens: input('Problem!')
	if final_lemmas != final_tokens: input('Problem!')
	del curr_text, curr_text_check