machines="blanch.cs.grinnell.edu boole.cs.grinnell.edu chapanis.cs.grinnell.edu even.cs.grinnell.edu flowers.cs.grinnell.edu forsythe.cs.grinnell.edu friedman.cs.grinnell.edu hollerith.cs.grinnell.edu karp.cs.grinnell.edu mauchly.cs.grinnell.edu stockmeyer.cs.grinnell.edu strachey.cs.grinnell.edu wang.cs.grinnell.edu wheeler.cs.grinnell.edu wijngaarden.cs.grinnell.edu wilkins.cs.grinnell.edu bethe.math.grinnell.edu bohr.math.grinnell.edu coulomb.math.grinnell.edu kaluza.math.grinnell.edu lorentz.math.grinnell.edu maxwell.math.grinnell.edu nicolson.math.grinnell.edu ohm.math.grinnell.edu planck.math.grinnell.edu thomson.math.grinnell.edu".split(" ")

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

import os
for i in alphabet:
        m = machines.pop()
        print "running %s on %s" %(i,m)
        os.spawnl(os.P_NOWAIT, '/usr/bin/ssh', 'ssh', m, 'python /home/athanasa/thesis/get_data.py %s > /home/athanasa/thesis/data/logging-%s &' % (i,i))
