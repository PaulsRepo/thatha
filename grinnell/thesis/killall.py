import mathlan

machines = mathlan.machines
alphabet = mathlan.alphabets

import os
for i in alphabet:
        m = machines.pop()
        print "running %s on %s" %(i,m)
        os.system('ssh %s "killall python"' % m)
