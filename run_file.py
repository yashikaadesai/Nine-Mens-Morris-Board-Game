

import subprocess
n = input("Enter a single-digit test number: ")
myoutput = open("output"+n+".txt","w")
myinput = open("input"+n+".txt",encoding="ascii",errors="surrogateescape")
p1 = subprocess.check_call(['python',"Ninemill.py"],stdin=myinput,stdout=myoutput)
myinput.close()
myoutput.close()


