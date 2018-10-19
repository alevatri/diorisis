import os
import configparser
import sys
import re

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("clear && printf '\e[3J'")
config = configparser.ConfigParser()
config.read('config.ini')
treetagger = config['paths']['treetagger']
tt_source = config['paths']['for_treetagger']
tt_output = config['paths']['treetagger_output']
tt_comparison = config['paths']['for_treetagger_comparison']
resources = config['paths']['file_list']

while True:
	a = input('Run TreeTagger on corpus? [y/n] ')
	if re.search('[yYnN]', a) != None:
		break
if re.search('[yY]', a) != None:
	for filename in os.listdir(tt_source):
		if os.path.isfile('%s/%s'%(tt_output,filename)):continue
		os.system("{tt_folder}/tree-tagger {curr_folder}/TreeTaggerData/ancient_greek.dat \"{tt_source}/{filename}\" \"{tt_output}/{filename}\" -token".format(tt_folder=treetagger, tt_source=tt_source, tt_output=tt_output, curr_folder=os.path.dirname(os.path.realpath(__file__)), filename=filename))

print('More magic under way...')
data = {}
for filename in os.listdir(tt_comparison):
	if filename[-3:]=='txt':
		print('\tHaving fun with',filename)
		data.setdefault(filename,{})
		a_lines=[x for x in open('%s/%s'%(tt_output,filename), 'r')]
		c_lines=[x for x in open('%s/%s'%(tt_comparison,filename), 'r')]
		for idx, x in enumerate(range(0,len(a_lines))):
			data[filename].setdefault(0,0)
			data[filename][0]+=1
			data[filename].setdefault(0.00000001,0)
			word = c_lines[idx].strip().split('\t')[0]
			corpus = c_lines[idx].strip().split('\t')[1:]
			treetagger = a_lines[idx].strip().split('\t')[1]
			if len(corpus) > 1:	data[filename][0.00000001]+=1
			pos_count = {}
			for pos in corpus:
				pos_count.setdefault(pos.strip(),0)
				if pos == treetagger:
					pos_count[pos.strip()]+=1
			total_pos=len(pos_count)
			total_lemmas=len(corpus)
			if total_pos > 1:
				message = 'We can\'t disambiguate this one'
				ends_in_bucket=0.00000002
				for pos,count in pos_count.items():
					if count == 1:
						message = 'The right guess is %s'%pos
						ends_in_bucket=1
					elif count > 1:
						message = 'The guess is %s with probability %s'%(pos,round(1/count, 2))
						ends_in_bucket=round(1/count, 2)
				#print(word,corpus,treetagger,message)
				data[filename].setdefault(ends_in_bucket,0)
				data[filename][ends_in_bucket]+=1	
output = open('%s/TT_disambiguation.txt'%resources, 'w')
tot_tokens=0
tot_amb_lemmas=0
tot_disamb=0
tot_disamb_prob=0
for text,counts in data.items():
	print(text)
	output.write(text+'\n')
	print()
	prob_dis=0
	for scores in sorted(counts.items()):
		if scores[0] == 0:
			tokens = scores[1]
			print('\tTotal tokens:',tokens)
			output.write('\n\tTotal tokens: %s'%tokens)
		elif scores[0] == 0.00000001:
			ambiguous_words = scores[1]
			print('\tAmbiguous lemmas:',ambiguous_words)	
			output.write('\n\tAmbiguous lemmas: %s'%ambiguous_words)
		elif scores[0] == 0.00000002: print('\tNon-disambiguable words:',scores[1])
		elif scores[0] < 1:
			print('\tWords disambiguated with %s probability:'%scores[0],scores[1])
			output.write('\n\tWords disambiguated with %s probability: %s'%(scores[0],scores[1]))
			prob_dis+=(scores[0]*scores[1])
		elif scores[0] == 1:
			print('\tDisambiguated words:',scores[1])
			output.write('\n\tDisambiguated words: %s'%scores[1])
			disambiguated = scores[1]
	tot_tokens+=tokens
	tot_amb_lemmas+=ambiguous_words
	tot_disamb+=disambiguated
	tot_disamb_prob+=disambiguated+prob_dis		
	#Stats:
	ambiguity=round(ambiguous_words*100/tokens,2)
	disambiguation=round(disambiguated*100/ambiguous_words,2)
	disambiguation_prob=round(100*(disambiguated+prob_dis)/ambiguous_words,2)
	residual=ambiguous_words-disambiguated
	residual_prob=round(ambiguous_words-(disambiguated+prob_dis),2)
	residual_ambiguity=round(100*residual/tokens,2)
	residual_ambiguity_prob=round(100*residual_prob/tokens,2)
	print('\tAmbiguity (%):',ambiguity,sep="\t")
	output.write('\n\tAmbiguity (%%):\t%s'%ambiguity)
	print('\tDisambiguation (%):',disambiguation,sep="\t")
	output.write('\n\tDisambiguation (%%):\t%s'%disambiguation)
	print('\tDisambiguation (including probabilities of uncertain words) (%):',disambiguation_prob,sep="\t")
	output.write('\n\tDisambiguation (including probabilities of uncertain words) (%%):\t%s'%disambiguation_prob)
	print('\tResidual ambiguous tokens:',residual,sep="\t")
	output.write('\n\tResidual ambiguous tokens:\t%s'%residual)
	print('\tResidual ambiguous tokens (including probabilities of uncertain words):',residual_prob,sep="\t")
	output.write('\n\tResidual ambiguous tokens (including probabilities of uncertain words):\t%s'%residual_prob)
	print('\tResidual ambiguity (%):',residual_ambiguity,sep="\t")
	output.write('\n\tResidual ambiguity (%%):\t%s'%residual_ambiguity)
	print('\tResidual ambiguity (including probabilities of uncertain words) (%):',residual_ambiguity_prob,sep="\t")
	output.write('\n\tResidual ambiguity (including probabilities of uncertain words) (%%):\t%s'%residual_ambiguity_prob)
	print('\n######################\n')	
	output.write('\n\n######################\n')
	
print('Totals')
output.write('\nTotals')
print('\tTokens:',tot_tokens)
output.write('\n\tTokens: %s'%tot_tokens)
print('\tAmbiguous lemmas:',tot_amb_lemmas)	
output.write('\n\tAmbiguous lemmas: %s'%tot_amb_lemmas)
print('\tDisambiguated words:',tot_disamb)
output.write('\n\tDisambiguated words: %s'%tot_disamb)
print('\tDisambiguated words (including probabilities of uncertain words):',tot_disamb_prob)
output.write('\n\tDisambiguated words (including probabilities of uncertain words): %s'%tot_disamb_prob)
ambiguity=round(tot_amb_lemmas*100/tot_tokens,2)
disambiguation=round(tot_disamb*100/tot_amb_lemmas,2)
disambiguation_prob=round(100*tot_disamb_prob/tot_amb_lemmas,2)
residual=tot_amb_lemmas-tot_disamb
residual_prob=round(tot_amb_lemmas-tot_disamb_prob,2)
residual_ambiguity=round(100*residual/tot_tokens,2)
residual_ambiguity_prob=round(100*residual_prob/tot_tokens,2)
print('\tAmbiguity (%):',ambiguity,sep="\t")
output.write('\n\tAmbiguity (%%):\t%s'%ambiguity)
print('\tDisambiguation (%):',disambiguation,sep="\t")
output.write('\n\tDisambiguation (%%):\t%s'%disambiguation)
print('\tDisambiguation (including probabilities of uncertain words) (%):',disambiguation_prob,sep="\t")
output.write('\n\tDisambiguation (including probabilities of uncertain words) (%%):\t%s'%disambiguation_prob)
print('\tResidual ambiguous tokens:',residual,sep="\t")
output.write('\n\tResidual ambiguous tokens:\t%s'%residual)
print('\tResidual ambiguous tokens (including probabilities of uncertain words):',residual_prob,sep="\t")
output.write('\n\tResidual ambiguous tokens (including probabilities of uncertain words):\t%s'%residual_prob)
print('\tResidual ambiguity (%):',residual_ambiguity,sep="\t")
output.write('\n\tResidual ambiguity (%%):\t%s'%residual_ambiguity)
print('\tResidual ambiguity (including probabilities of uncertain words) (%):',residual_ambiguity_prob,sep="\t")
output.write('\n\tResidual ambiguity (including probabilities of uncertain words) (%%):\t%s'%residual_ambiguity_prob)
output.close()