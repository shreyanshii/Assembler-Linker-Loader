import re,compiler,linker,assembler,loader
files=[]
offsets=[]
print 'Enter file names(in descending order of execution):'
while True:
	print 'File Name:',
	fname=raw_input()
	if fname is '':
		break;
	files.append(fname)
main='concatenated'+'.link'  
symbols=compiler.convtoassembly(files)
print(symbols)
assembler.pass1(files)
assembler.pass2(files)
for filec in files:
	print '\nEnter Loading location for  '+filec 
	offset=int(raw_input())
	offsets.append(offset)
offsets2=offsets[:]
linker.link(main, symbols,offsets)
loader.load('concatinated.link',offsets2)
