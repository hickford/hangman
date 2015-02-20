#!/usr/bin/python
import re
import random
import string
import sys
import optparse
import os.path
import cPickle as pickle

# Hangman
# January 2009

save_file = os.path.expanduser("~/.hangman.py-scores.pickled")

class state():
	def __init__(self,n,clues=None,guesses=None):
		self.clues = clues
		if not self.clues:
			self.clues = []
			for i in range(n):
				self.clues.append(None)

		self.guesses = guesses
		if not self.guesses:
			self.guesses = []

	def copy(self):
		return state(len(self.clues),self.clues[:],self.guesses[:])

	def pretty_clues(self):
		S = []
		for x in self.clues:
			if x:
				S.append(x)
			else:
				S.append("_")
		return " ".join(S)

	def agree(self,word):
		if len(word) != len(self.clues):
			return False

		for (n,x) in enumerate(self.clues):
			if x:
				if word[n] != x:
					return False
			else:
				if word[n] in self.guesses:
					return False
		return True

class game():
	global dictionary

	def __init__(self,length,fair=False,dumb=False,hacks=False,graphics=True,interactive=True):
		self.length = length 
		self.interactive = interactive
		self.won = False

		self.words = []

		self.state = state(self.length)

		self.incorrect = 0
		self.lose_condition = 12

		self.commands = ["help","hint","about","list","quit",]
		self.hiddencommands = ["list",]

		self.words = [w for w in dictionary if len(w) == self.length ]

		assert len(self.words) > 0, "no words of length %d" % n

		self.fair = fair
		if self.fair:
			self.words = [random.choice(self.words)]
			self.commands.remove("hint")

		self.hacks = hacks
		self.dumb = dumb
		self.graphics = graphics

	def guess(self,letter):
		self.state.guesses.append(letter)

		words_out = [w for w in self.words if letter not in w]
		words_in = [w for w in self.words if letter in w]

		# decide what to do
		# compare len(words2) with words by the second method for some random words

		words3 = []	
		if words_in:
			word = random.choice(words_in)
			state3 = self.state.copy()

			for n,x in enumerate(word):
				if x == letter:
					state3.clues[n] = letter

			words3 = [w for w in words_in if state3.agree(w)]

		# tune constants
		A = random.randrange(0,6)
		B = -1

		if words_out and  (self.dumb or   len(words_out) > A * ( len(words3) + B)) :
			self.words = words_out
			#print "letter %s not in word" % letter
			self.incorrect += 1
			return False
		else:
			self.words = words3
			self.state = state3
			if all(self.state.clues):
				self.won = True
			return [n for n,x in enumerate(word) if x == letter]


	def about(self):
		print """this game was written 30-31 January 2009, after playing hangman in lectures. Over lunch a malicious A.I. was devised to defeat Jon."""

	def help(self):
		print "you are playing hangman."
		self.listcommands()

	def listcommands(self):
		print "Other commands are %s." % ", ".join([("'%s'" % c) for c in self.commands if c not in self.hiddencommands or self.hacks ]) 

	def hint(self):
		print "the word could be '%s'" % random.choice(self.words)
		# free hint on last turn
		if self.incorrect != self.lose_condition - 1:
			self.incorrect += 1

	def quit(self):
		print "bye! the word was '%s'" % random.choice(self.words)
		sys.exit()

	def list(self):
		print " ".join(self.words)

	def play(self):
		print self.length,"letters"

		print 
		print self.state.pretty_clues()

		if self.hacks:
			print "words remaining: %d" % len(self.words)

		while True:
			print "your guess:",
			t = raw_input().lower().strip()
			if len(t) > 1 and t in self.commands:
				getattr(self,t)()
			elif len(t) == 1 and t in string.lowercase:
				if t in self.state.guesses:
					print "you have previously guessed '%s'!" % t
				else:
					if not self.guess(t):
						print "letter %s not in word" % t
			else:
				print "'%s' is not a letter." % t,
				self.listcommands()

			print

			print self.state.pretty_clues()

			#if all(self.state.clues):
			if self.won:		
				print "you win! :)"
				return True

			if self.incorrect >= self.lose_condition:
				print "you lose!"
				print "the word was: %s" % random.choice(self.words)

				if self.graphics:
					print dude[0]
				return False

			print "previous guesses:"," ".join(self.state.guesses)

			if self.hacks:
				print "words remaining: %d" % len(self.words)

			remain = self.lose_condition - self.incorrect

			if self.graphics:
				print dude[remain]
			print "%d guesses left" % remain


dude = {
12:"""\
   
     
      
      
      
	 
""",


11:"""\
   
     
      
      
      
________
""",

10:"""\
   
   |  
   |   
   |   
   |   
___|____
""",

9:"""\
   
   |  
   |   
   |   
   |   
___|\___
""",

8:"""\
   _____
   |  
   |   
   |   
   |   
___|\___
""",

7:"""\
   _____
   |/  
   |   
   |   
   |   
___|\___
""",


6:"""\
   _____
   |/   |
   |   
   |   
   |   
___|\___
""",

5:"""\
   _____
   |/   |
   |    O 
   |   
   |   
___|\___
""",

4:"""\
   _____
   |/   |
   |    O
   |    |
   |   
___|\___
""",

3:"""\
   _____
   |/   |
   |    O
   |    |
   |   / 
___|\___
""",

2:"""\
   _____
   |/   |
   |    O
   |    |
   |   / \ 
___|\___
""",


1:"""\
   _____
   |/   |
   |    O
   |   -|
   |   / \ 
___|\___
""",

0:"""\
   _____
   |/   |
   |    O
   |   -|-
   |   / \  
___|\___
""",
}


def random_length():
	min_length = 4
	max_length = 18+1
	sample = 3
	n = max_length
	for i in range(sample):
		n = min(n,random.randrange(min_length,max_length))
	return n

def load_scores():
	"""return games,wins"""
	f = open(save_file)
	games, wins = pickle.load(f)
	f.close()
	return games,wins

def save_scores(games,wins):
	f = open(save_file,"w")
	pickle.dump((games,wins),f)
	f.close()

def make_dictionary(path):
	test = re.compile(r"^[a-z]+$")
	f = open(path)
	dictionary = []
	for x in f:
		x = x.strip()
		if test.match(x):
			dictionary.append(x)
	f.close()
	return dictionary

if __name__ != "__main__":
	# imported as module
	dictionary = make_dictionary("/usr/share/dict/words")
else:
	print "HANGMAN"
	print "Matt, James, Ed and Steve "
	print "mh519@cam.ac.uk"
	print

	description = """Play a game of hangman."""
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage=usage,description=description)
	parser.add_option("-l","--length",dest="length",default=None,help="specify length of word")
	parser.add_option("-b","--boring",action="store_false",dest="graphics",default=True,help="do not display graphics")
	parser.add_option("-f","--fair",action="store_true",dest="fair",default=False,help="play fair")
	parser.add_option("-d","--dumb",action="store_true",dest="dumb",default=False,help="use early, less intelligent A.I.")
	parser.add_option("-x","--hacks",action="store_true",dest="hacks",default=False,help="show game state")
	parser.add_option("-w","--words",dest="dictionary",default="/usr/share/dict/words",help="dictionary to use")

	(options, args) = parser.parse_args()

	dictionary = make_dictionary(options.dictionary)

	try:
		games,wins = load_scores()
	except:
		games, wins = 0,0

	answer = "yes"
	while answer in "yes":
		games += 1
		if options.length:
			n = int(options.length)
		else:
			n =  random_length() 
		G = game(n,fair=options.fair,dumb=options.dumb,hacks=options.hacks,graphics=options.graphics)
		try:
			if G.play():
				wins += 1
		except KeyboardInterrupt:
			print
			print "the word was '%s'" % random.choice(G.words)
			save_scores(games,wins)
			sys.exit()
		print
		print "your stats are %d wins, %d losses" % (wins,games-wins)
		print "play again?",

		try:
			answer = raw_input().strip().lower()
		except:
			break

	save_scores(games,wins)
	print "thank you for playing hangman."


