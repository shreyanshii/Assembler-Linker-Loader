def link(files, symbols,offsets):
	var_loc=makeuniversal(symbols)
	var_loc2=makeuniversalacctooffset(symbols,offsets)
	# print var_loc2
	# print var_loc
	f=open(files,'r')
	data=f.read()
	f.close()
	data=data.splitlines()
	data2=data[:]
	for i in range(0,len(data)):
		line=data[i]
		line1=data[i]
		if line.startswith('J') or line.startswith('LDA') or line.startswith('STA'):
			variable_name = line.split(' ')[1]
			if(variable_name not in var_loc):
				print 'Variable '+variable_name+' Not present in any of the files'
				exit()
			val=var_loc[variable_name]
			data[i]=line.replace(variable_name,str(val))
			data2[i]=line1.replace(variable_name,str(var_loc2[variable_name]))
	
	f=open(files,'w')
	f.truncate()
	f.write('\n'.join(data))
	f.close()
	ff=open('concatinated.link','w')
	ff.write('\n'.join(data2))
	ff.close()

def makeuniversalacctooffset(symbols,offsets):
	i=0
	variable_loc={}						#global valriable locations
	for filename in symbols:
		for key,val in symbols[filename].items():
			variable_loc[key]=val+offsets[i]
		i+=1
		if(i<len(offsets)):
			offsets[i]+=offsets[i-1]
	return variable_loc
	
def makeuniversal(symbols):
	variable_loc={}						#global valriable locations
	for filename in symbols:
		for key,val in symbols[filename].items():
			variable_loc[key]=val
	return variable_loc
