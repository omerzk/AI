def createDomainFile(domainFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  pegSet = set(pegs)
  with open(domainFileName, 'w') as domain:                       #use domainFile.write(str) to write to domainFile
    domain.write("Propositions:\n")
    for i in numbers:
       domain.write("{0}a {0}b {0}c ".format(str(i)))
    domain.write("\nActions:\n")
    for i in numbers:
      disk = str(i)
      for originPeg in pegs:
        for destPeg in pegs:
          if originPeg != destPeg:
            domain.write(("Name: M{0}" + originPeg + destPeg + "\n").format(disk))
            domain.write("pre: " + disk + originPeg + " ")
            otherPeg = list(pegSet - set({originPeg, destPeg}))[0]
            for smaller in range(i):
              domain.write(str(smaller) + otherPeg + " ")

            domain.write("\nadd: " + disk + destPeg)
            domain.write("\ndelete: " + disk + originPeg + "\n")



          
  
def createProblemFile(problemFileName, n):
  numbers = list(range(n))                                              # [0,...,n-1]
  pegs = ['a','b', 'c']
  initial = "Initial state:"
  goal = "Goal state:"
  for diskNum in numbers[::-1]:
    disk = str(diskNum) 
    initial += " " + disk + pegs[0]
    goal += " " + disk + pegs[-1]

  with open(problemFileName, 'w') as problem:                             #use problemFile.write(str) to write to problemFile
    problem.write(initial + "\n" + goal + "\n")

import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)
  
  n = int(float(sys.argv[1]))                                           #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'
  
  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)