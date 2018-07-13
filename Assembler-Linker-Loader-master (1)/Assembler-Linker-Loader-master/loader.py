import re

def load(files, offsets):
	f=open(files,'r')
	data=f.read()
	f.close()
	data=data.splitlines()
	datanew=[]
	f=open(files.split('.')[0]+'.load','w')
	k=0
	t=0
	p=0
	q=0
	offset1 = offsets
	offset1 = makeuniversalacctooffset(offset1)
	for offset in offsets:
		if(offsets[0]!=0):
			f.write('JMP '+str(offset[0]))	
		for i in range(0,offset):
			f.write('\n')
			q+=1
		for i in range(k,len(data)):
			line=data[i]
			t+=1
			q+=1
			if (('HLT' in line) and (i == len(data))):
				datanew.append(data[i])
				f.write(('\n'.join(datanew))+'\n')
				datanew=[]
				k=t
				break
			elif ('HLT' in line):
				if(p<len(offset1)-1):
					datanew.append("JMP "+str(offset1[p+1]+q))		
				f.write(('\n'.join(datanew))+'\n')
				datanew=[]
				k=t
				p=p+1
				break
			else:
				datanew.append(data[i])	
	f.write('HLT')				
	#f.write('\n'.join(data))
	f.close()
	print (files.split('.')[0]+'.load file is generated')

def makeuniversalacctooffset(offsets):
	i=0						#global valriable locations
	for offset in offsets:
		i+=1
		if(i<len(offsets)):
			offsets[i]+=offsets[i-1]
	return offsets