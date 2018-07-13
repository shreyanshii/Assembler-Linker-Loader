
import re

pp=0

symbols = {}
symbols_extern = {}
arraytab = {}
loopend = []
startif = []


def convtoassembly(files):
	code = []
	variable_code = []
	cc=1											#for generating individual 
	pp=0
	loopcount=0
	ifcount=0
	assign=re.compile('var(.*?)=(.*)')				#assigning regular expressions
	ext=re.compile('extern (.*)')					#.*? means the first occurence of ( .(anything) *(any number of times) )
	arith=re.compile('(.*?)=(.*?)[\+\-\&\|](.*?)')
	arith_add=re.compile('(.*?)=(.*?)\+(.*)')
	arith_sub=re.compile('(.*?)=(.*?)\-(.*)')
	arith_or=re.compile('(.*?)=(.*?)\|(.*)')
	arith_and=re.compile('(.*?)=(.*?)\&(.*)')
	incrmacro=re.compile('(.*?)\+\+')
	decrmacro=re.compile('(.*?)--')
	# Array
	rearray = re.compile("\s*var\s+(\w+)\[(\w+)\]\s*")
	reassarr = re.compile("\s*(\w+)\[(\w+)\]\s*=\s*(\w+)\s*")
	remaxmacro = re.compile("\s*max\s+(\w+)\s+(\w+)\s+(\w+)\s*")
	reminmacro = re.compile("\s*min\s+(\w+)\s+(\w+)\s+(\w+)\s*")


	fileno=1
	for filen in files:								
		f=open(filen,'r')
		data=f.read()								#reading file
		f.close()
		filename=filen.split('.')[0]				#get filename
		filename=str(fileno)+filename
		symbols[filename]= {}						#dictionary with symbol of each file		
		symbols_extern[filename]= {}
		arraytab[filename] = {}
				#dictionary with external symbol of each file		
		fileno+=1	
		lines=data.splitlines()						#splitting in lines
		for line in lines:
			line=line.strip()						#remove extra white space
			if assign.match(line):					#if line matches var assign
				asign=line[3:]						#remove var part
				a=re.search(r'(.*?)=(.*)',asign)
				vari = a.group(1).strip()           #takes out variable
				val = a.group(2).strip()			#takes out value
				variable_code.append([vari,val])
				symbols[filename][vari] = 0
				pp += 0

			elif ext.match(line):
				var=line[6:].strip()
				symbols_extern[filename][var]='extern'+var

			elif rearray.match(line):
				# to initialise any array
				var = rearray.match(line).group(1)
				lent = rearray.match(line).group(2)
				
				arraytab[filename][var] = [str(var), lent]
				lent1 = int(lent)
				for x in range(0,lent1):
					symbols[filename][str(var) + "`" + str(x)] = 0



			elif reassarr.match(line):
				name = reassarr.match(line).group(1)
				disp = reassarr.match(line).group(2)
				val = reassarr.match(line).group(3)
				# if ( name not in arraytab[filename] ) or ( not isint(disp) ) or not ( isint(val) or val in symtab[filename]):
				# 	error = "Invalid line: " + line
				# 	return

				if val.isdigit():
					code.append("MVI Areg, " + str(val) + "\n")
					code.append("STA " + str(arraytab[filename][name][0]) + "`" + str(disp) + "\n" )
					pp = pp+2

				else:
					code.append("LDA " + str(val) + "\n" )
					code.append("STA " + str(arraytab[filename][name][0]) + "`" + str(disp) + "\n" )
					pp = pp + 2 



			elif remaxmacro.match(line):

				ifcount+=1

				target1 = remaxmacro.match(line).group(1)
				print (target1)
				var1 = remaxmacro.match(line).group(2)
				var2 = remaxmacro.match(line).group(3)

				code.append('LDA '+var2+'\n')
				code.append('STA ' + target1 + '\n')
				pp += 2

				code.append('LDA '+var1+'\n')
				code.append('MOV Breg, Areg\n')
				code.append('LDA '+var2+'\n')
				code.append('SUB Breg\n')
				startif.append(ifcount)
				code.append('JP P'+str(ifcount)+'\n')
				symbols[filename]['I'+str(ifcount)] = pp
				pp += 5


				code.append('LDA '+var1+'\n')
				code.append('STA ' + target1 + '\n')
				pp += 2


				currif=str(startif.pop())
				code.append('P'+currif+' PASS \n')
				symbols[filename]['P'+currif] = pp
				pp+=1




			elif reminmacro.match(line):

				ifcount+=1

				target1 = reminmacro.match(line).group(1)
				print (target1)
				var1 = reminmacro.match(line).group(2)
				var2 = reminmacro.match(line).group(3)

				code.append('LDA '+var1+'\n')
				code.append('STA ' + target1 + '\n')
				pp += 2

				code.append('LDA '+var1+'\n')
				code.append('MOV Breg, Areg\n')
				code.append('LDA '+var2+'\n')
				code.append('SUB Breg\n')
				startif.append(ifcount)
				code.append('JP P'+str(ifcount)+'\n')
				symbols[filename]['I'+str(ifcount)] = pp
				pp += 5

				
				code.append('LDA '+var2+'\n')
				code.append('STA ' + target1 + '\n')
				pp += 2


				currif=str(startif.pop())
				code.append('P'+currif+' PASS \n')
				symbols[filename]['P'+currif] = pp
				pp+=1


			elif arith.match(line):
				a=re.search(r'(.*?)=(.*?)[\+\-\&\|](.*)',line)
				if arith_add.match(line):
					op='ADD '
					opi='ADI '
				elif arith_sub.match(line):
					op='SUB '
					opi='SUI '
				elif arith_and.match(line):
					op='ANA '
					opi='ANI '
				elif arith_or.match(line):
					op='ORA '
					opi='ORI '
				vari = a.group(1).strip()
				var1 = a.group(2).strip()
				var2 = a.group(3).strip()
				# print (vari)
				# print (var1)
				# print (var2)
				if var1.isdigit() and var2.isdigit():
					code.append('MVI Areg, '+var1+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+vari+'\n')
					pp += 3
				elif var1.isdigit():
					code.append('LDA '+var2+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('MVI Areg, '+var1+'\n')
					code.append(op+'Breg\n')
					code.append('STA '+vari+'\n')
					pp += 5
				elif var2.isdigit():
					code.append('LDA '+var1+'\n')
					code.append(opi+var2+'\n')
					code.append('STA '+vari+'\n')
					pp += 3
				else:
					code.append('LDA '+var2+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var1+'\n')
					code.append(op+'Breg\n')
					code.append('STA '+vari+'\n')
					pp += 5

			elif line.startswith('loop'):
				loopcount+=1
				a=re.search(r'loop(.*)',line)
				count=a.group(1).strip()
				code.append('PUSH Dreg\n')				#for nested loops
				code.append('MVI Ereg, '+count+'\n')
				pp += 2
				code.append('L'+str(loopcount)+' PASS\n')
				symbols[filename]['L'+str(loopcount)] = pp
				pp+=1
				loopend.append(loopcount)

			elif line.startswith('endloop'):
				code.append('MOV Areg, Ereg\n')
				code.append('SUI 1\n')
				code.append('MOV Ereg, Areg\n')
				code.append('JNZ '+'L'+str(loopend.pop())+'\n')
				code.append('POP Dreg'+'\n')
				pp += 5

			elif line.startswith('if'):
				a=re.search(r'if(.*?)\((.*?)\)',line)					#if (condn)
				cond = a.group(2)
				if '>' in cond:
					ifcount+=1
					a=re.search(r'(.*?)>(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('LDA '+var1+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var2+'\n')
					code.append('SUB Breg\n')
					startif.append(ifcount)
					code.append('JP P'+str(ifcount)+'\n')
					code.append('JZ P'+str(ifcount)+'\n')
					symbols[filename]['I'+str(ifcount)] = pp
					pp += 6
				elif '=' in cond:
					ifcount+=1
					a=re.search(r'(.*?)=(.*)',cond)
					var1 = a.group(1).strip()
					var2 = a.group(2).strip()
					code.append('LDA '+var1+'\n')
					code.append('MOV Breg, Areg\n')
					code.append('LDA '+var2+'\n')
					code.append('SUB Breg\n')
					startif.append(ifcount)
					code.append('JNZ P'+str(ifcount)+'\n')
					symbols[filename]['I'+str(ifcount)] = pp
					pp += 5

			elif line.startswith('endif'):
				currif=str(startif.pop())
				code.append('P'+currif+' PASS \n')
				symbols[filename]['P'+currif] = pp
				pp+=1
				
			elif incrmacro.match(line):
				a=re.search(r'(.*?)\+\+',line)
				var_name = a.group(1).strip()
				code.append('LDA '+var_name+'\n')
				code.append('ADI 1\n')
				code.append('STA '+var_name+'\n')
				pp+=3
			
			elif decrmacro.match(line):
				a=re.search(r'(.*?)--',line)
				var_name = a.group(1).strip()
				code.append('LDA '+var_name+'\n')
				code.append('SUI 1\n')
				code.append('STA '+var_name+'\n')
				pp+=3
			else:
				a=re.search(r'(.*?)=(.*)',line)
				var=a.group(1).strip()
				val=a.group(2).strip()
				if val.isdigit():
					code.append('MVI Areg, '+val+'\n')
					code.append('STA '+var+'\n')
					pp += 2
				else:
					code.append('LDA '+val+'\n')
					code.append('STA '+var+'\n')
					pp += 2
		#finding values for each variable for symbol table
		for val in variable_code:
			code.append(val[0]+' '+'DC '+val[1]+'\n')
			symbols[filename][val[0]] =pp
			pp+=1 

		for var,p in arraytab[filename].items():
			# print (var)
			# print (p)
			i = p[1]
			# print (i)
			i = int(i)
			for x in range(0,i):
				code.append(p[0] +'`' +str(x)+ ' '+'DC '+'0'+'\n')
				symbols[filename][ p[0] +'`' + str(x) ] =pp
				pp+=1 


		####	
		variable_code=[]
		code.append('HLT\n')
		pp+=1
	filename='concatenated'
	f=open(filename+'.link','w')
	f.write(''.join(code))
	f.close()
	f=open(filename+'.assemble','w')
	f.write(''.join(code))# join concatenates list items to a string
	f.close()
	print filename+'.assemble file generated.'
	# print(symbols)
	# print (arraytab)
	return symbols
