#!/usr/bin/python3.7
import time
import requests

numberlevels = 5000
#whalemixer's output to TryNinja
seed = 'a576790d4b0180611d9703d86538f943120ce928dafc4daf016128a66fb4730a'
#my own last unspent output funding my public address
#seed = 'b3c2c7d070d970e4af4a9eeb229ce645a556f969e1d3b556593c08ff5e1ee2ef'
todo = [seed]
lijnen = []
f = open(seed + ".txt", "w")
f.write("digraph "+seed+" {\n")
f.close()
level = 0
while len(todo) > 0 and level < numberlevels:
	time.sleep(1)
	level += 1
	print(str(level))
	currenttx = todo.pop(0)
	currenturl = "https://sochain.com/api/v2/get_tx_inputs/BTC/" + currenttx
	r = requests.get(currenturl)
	inputs = r.json()['data']['inputs']
	for input in inputs:
		print(input)
		address = input['address']
		if address == 'coinbase':
			f = open(seed + ".txt", "a")
			f.write("coinbase -> \""+ currenttx + "\";\n")
			lijnen.append({"van": "coinbase", "tot": currenttx})
			f.close()
		else:
			previous_tx = input['from_output']['txid']
			f = open(seed + ".txt", "a")
			f.write("\""+ previous_tx + "\" -> \"" + currenttx  + "\";\n")
			lijnen.append({"van": previous_tx, "tot": currenttx})
			f.close()
			todo.append(previous_tx)
	
f = open(seed + ".txt", "a")
f.write("}")
f.close()

print("voor verwijderen dupes:" + str(len(lijnen)))
lijnen = [dict(t) for t in {tuple(d.items()) for d in lijnen}]
print("na verwijderen dupes:" + str(len(lijnen)))

coinbase = []
f = open(seed + ".coinbase.txt", "w")
f.write("digraph "+seed+" {\n")

for lijn in lijnen:
	van = lijn["van"]
	tot = lijn["tot"]
	if van == "coinbase":
		print("coinbase gevonden: " + tot)
		coinbase.append(tot)
		f.write("coinbase -> \""+ tot + "\";\n")

if len(coinbase) > 0:
	while len(coinbase) > 0:
		currentcoinbase = coinbase.pop(0)
		for lijn in lijnen:
			van = lijn["van"]
			tot = lijn["tot"]
			if van == currentcoinbase:
				coinbase.append(tot)
				f.write("\""+ van + "\" -> \"" + tot  + "\";\n")
	

f.write("}")
f.close()
		
