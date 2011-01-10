#!/usr/bin/python
import re
import random
import string
import sys
import optparse
import os.path
import cPickle as pickle
import hangman
dictionary = hangman.dictionary[:]	# copy

def play(length,verbose=False):
	G = hangman.game(length)
	letters = list(string.lowercase)
	incorrect = 0
	while not G.won:
		words = [w for w in dictionary if G.state.agree(w)]	# delay!
		comparison = {}
		for letter in letters:
			comparison[letter] = len([w for w in words if letter in w])

		maximal = max(comparison.values())
		best_letters = [letter for letter,count in comparison.items() if count == maximal]
		if len(best_letters) > 1:
			mega = "".join(words)
			second_comparison = {}
			for letter in best_letters:
				second_comparison[letter] = mega.count(letter)
			maximal = max(second_comparison.values())
			best_letters = [letter for letter,count in second_comparison.items() if count == maximal]

		letter = random.choice(best_letters)
		reply = G.guess(letter)
		if not reply:
			incorrect += 1	

		if verbose:
			#print letter, reply
			print letter, str(reply).ljust(8), len([w for w in dictionary if G.state.agree(w)])
		letters.remove(letter)
	return "".join(G.state.clues),incorrect	
	#else:
	#	print "".join(G.state.clues),"after %d incorrect guesses" % incorrect

if __name__=="__main__":
	length = random.randrange(3,12)
	#length = 12
	print length,"letters"
	word, incorrect = play(length,verbose=True)
	print word,"after %d incorrect guesses" % incorrect


