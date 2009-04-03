import os

___machines___ = "fisher.math.grinnell.edu ampere.math.grinnell.edu blanch.cs.grinnell.edu boole.cs.grinnell.edu chapanis.cs.grinnell.edu even.cs.grinnell.edu flowers.cs.grinnell.edu forsythe.cs.grinnell.edu friedman.cs.grinnell.edu hollerith.cs.grinnell.edu karp.cs.grinnell.edu mauchly.cs.grinnell.edu stockmeyer.cs.grinnell.edu strachey.cs.grinnell.edu wang.cs.grinnell.edu wheeler.cs.grinnell.edu wijngaarden.cs.grinnell.edu wilkins.cs.grinnell.edu bethe.math.grinnell.edu bohr.math.grinnell.edu kaluza.math.grinnell.edu lorentz.math.grinnell.edu maxwell.math.grinnell.edu nicolson.math.grinnell.edu ohm.math.grinnell.edu planck.math.grinnell.edu thomson.math.grinnell.edu".split(" ")

def execute(commands):
    machines = [ x for x in ___machines___ ]
    for command in commands:
        machine = machines.pop()
        print "Running %s on %s..." % (command, machine)
        os.spawnl(os.P_NOWAIT, '/usr/bin/ssh', 'ssh', machine, command)
