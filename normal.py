#!/usr/bin/env python3

import unicodedata as ucd
import sys
import argparse
import re
from urllib.parse import quote

parser = argparse.ArgumentParser(description = "Find unicode codepoints to use in normalization attacks.")
parser.add_argument('-s', '--string', default='', help="""Use this to check if any normalized codepoints appear within your given string, or if your string appears within any normalized codepoints.""")
parser.add_argument('-r', '--regex', default='', help="""Use this to check if any normalized codepoints contain a given regex pattern.""")
parser.add_argument('-c', '--codepoint', default='', help="Given an integer or character, display details about the relevant codepoint.")
parser.add_argument('--upper', default='', help="Return the upper cased version of a given string")
parser.add_argument('--lower', default='', help="Return the upper cased version of a given string")
parser.add_argument('--normalize', default='', help="Return all four unicode normalizations of a given string")

args = parser.parse_args()

if args.regex != '':
	try:
		search_pattern = re.compile(args.regex)
	except:
		print(f"Invalid regex pattern: {args.regex}")
else: search_pattern = ''

search_string = args.string

if args.codepoint != '':
	try:
		codepoint = int(args.codepoint)
	except:
	  codepoint = ord(args.codepoint[0])
else:
	codepoint = ''

# it's possible that having all four formats is dumb. I'm still unicode new. 
normalization_formats = ['NFD', 'NFC', 'NFKD', 'NFKC']

if args.lower != '':
	print(f"Lowercased: {args.lower.lower()}")
	exit()
if args.upper != '':
	print(f"Uppercased: {args.upper.upper()}")
	exit()
if args.normalize != '':
	for f in normalization_formats:
		print(f"normalize: {f} : {ucd.normalize(f,args.normalize)}")
	exit()

try:
	unicode_name = ucd.name(chr(codepoint))
except:
	unicode_name = "[No Standard Name]"

if codepoint != '':
	if type(codepoint) == str:
		print("YAY")
		codepoint = ord(codepoint[0])

	print(f"{unicode_name} : {chr(codepoint)}")

	print(f"Unicode codepoint: U+{codepoint}")
	print(f"URL Encoded: {quote(chr(codepoint), encoding='utf-8')}")
	for f in normalization_formats:
		normalized_string = ucd.normalize(f, chr(codepoint))
		print(f"{f} : {normalized_string} {[ord(a) for a in normalized_string]}")
	with open('htmlents.txt', 'r', encoding='utf-8') as infile:
		for line in infile:
			line = line.rstrip()
			entity_name, entity_codepoint = line.split(' ')
			if int(entity_codepoint) == codepoint:
				print(f"HTML Entity name: &{entity_name};")
	print(f"HTML Entity decimal: &#{codepoint}")
	print(f"HTML Entity hex: &#x{hex(codepoint).split('x')[-1]}")
	print(f"To upper-case {chr(codepoint).upper()}")
	print(f"To lower-case {chr(codepoint).lower()}")

# this will store a list of found matches
matches = []

# loop through every single unicode codepoint
for i in range(sys.maxunicode+1):

	uppercased = chr(i).upper()
	lowercased = chr(i).lower()

	if search_pattern != "":
		if search_pattern.search(uppercased):
			matches.append( (chr(i), "Upper-case") )
		if search_pattern.search(lowercased):
			matches.append( (chr(i), "Lower-case") )

	if search_string != "":
		if search_string in uppercased or uppercased in search_string:
			matches.append( (chr(i), "Upper-case") )
		if search_string in lowercased or lowercased in search_string:
			matches.append( (chr(i), "Lower-case") )

	# loop through all four normalization formats
	for f in normalization_formats:

		# Don't output anything for the case where you're looking for matches to a 
		# single character, and the codepoint == that character. We do this because 
		# standard ascii chars will always normalize to themselves, so we'll end up 
		# with four trivial cases cluttering the output.
		if len(search_string) == 1 and search_string == chr(i):
			continue 
		
		else:
			# get the normalized version of the string
			normalized_string = ucd.normalize(f, chr(i))

			# check if the supplied regex pattern finds a match in the normalized string
			if search_pattern != '':
				if search_pattern.search(normalized_string):
					matches.append( (chr(i), f) )
			# check if the normalized string is anywhere within the supplied string	or vice versa
			if search_string != '':
				if search_string in normalized_string or normalized_string in search_string:
					matches.append( (chr(i), f) )

for m in matches:
	unichar, format = m
	try:
		unichar_name = ucd.name(unichar)
	except:
		unichar_name = "[No Standard Name]"
	
	if format in normalization_formats:
		print(f"{unichar} -> {ucd.normalize(format, unichar)} | (U+{ord(unichar)}) -> {[ord(a) for a in ucd.normalize(format,unichar)]} | ({unichar_name}) : {format}")
	elif format == "Lower-case":
		print(f"{unichar} -> {unichar.lower()} | (U+{ord(unichar)}) -> {[ord(a) for a in unichar.lower()]} | ({unichar_name}) : {format}")
	elif format == "Upper-case":
		print(f"{unichar} -> {unichar.upper()} | (U+{ord(unichar)}) -> {[ord(a) for a in unichar.upper()]} | ({unichar_name}) : {format}")
