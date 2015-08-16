#!/usr/bin/env python3

from sh import mv

import glob
import os


MAPPING = {
	'gbs': 'smb',
	'gbp': 'bsp',
	'gbo': 'bsk',
	'drl': 'drd',
	'gm1': 'oln',
	'gts': 'smt',
	'gtp': 'tsp',
	'gto': 'slk'
}

LAYERS_MAPPING = {
	2: {
		'gbl': 'bot',
		'gtl': 'top'
	},
	4: {
		'gbl': 'L1',
		'g2':  'L2',
		'g3':  'L3',
		'gtl': 'L4'
	}
}



fnames = glob.glob('./*')

# Determine if 2 layer or 4
layers = 2
for fname in fnames:
	name,ext = os.path.splitext(fname)
	ext = ext[1:]

	if ext == 'g2':
		layers = 4
		break

# Determine the real name of the gerbers
# (not the renamed crap kicad does)
true_name = None
for fname in fnames:
	name,ext = os.path.splitext(fname)
	ext = ext[1:]

	if ext == 'drl':
		true_name = os.path.basename(name)
		break
else:
	print('Could not find drill file (.drl file). Generate one.')
	os.path.exit(1)


# Do some renaming
for fname in fnames:
	name,ext = os.path.splitext(fname)
	ext = ext[1:]
	root = os.path.dirname(fname)
	if ext in MAPPING:
		new_ext = MAPPING[ext]
	else:
		try:
			new_ext = LAYERS_MAPPING[layers][ext]
		except:
			print('Could not find a mapping for "{}".'.format(fname))

	mv('{}'.format(fname), '{}/{}.{}'.format(root, true_name, new_ext))




