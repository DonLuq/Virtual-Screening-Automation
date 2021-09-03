import os, sys

def main(name = 'pro_MD',params = 'param.par',**kwargs):
    with open(name+'.namd','w') as file:
        file.write("#input\n")
        file.write("coordinates             "+name+".pdb\n")
        file.write("structure               "+name+".psf\n")
        file.write("parameters              "+params+"\n")
        file.write('''parameters		required_files/toppar_water_ions_namd.str
parameters              required_files/par_all36_carb.prm
parameters              required_files/par_all36_cgenff.prm
parameters              required_files/par_all36_lipid.prm
parameters              required_files/par_all36m_prot.prm
parameters              required_files/par_all36_na.prm
paratypecharmm          on

# output\n''')
        file.write("set output              "+name+"\n")
        file.write(
'''outputname              $output
dcdfile                 ${output}.dcd
xstFile                 ${output}.xst
dcdfreq                 2000
xstFreq                 2000

binaryoutput            no
binaryrestart           no
outputEnergies          2000
restartfreq             1000000

fixedAtoms              off

# Basic dynamics
exclude                 scaled1-4
1-4scaling              1
COMmotion               no
dielectric              1.0

# Simulation space partitioning
switching               on
switchdist              11
cutoff                  12
pairlistdist            14

# Multiple timestepping
firsttimestep           0
timestep                1
stepspercycle           20
nonbondedFreq           2
fullElectFrequency      4

# Temperature control

set temperature         298
temperature             $temperature;  # initial temperature

# Langevin Dynamics
langevin                on;            # do langevin dynamics
langevinDamping         1;              # damping coefficient (gamma) of 1/ps
langevinTemp            $temperature;   # bath temperature
langevinHydrogen        no;             # don't couple langevin bath to hydrogens
seed                    12345\n\n''')
        file.write('''# Pressure control
langevinPiston on
langevinPistonTarget 1.01325; # in bar -> 1.01325 bar = 1 atm
langevinPistonPeriod 200
langevinPistonDecay 100
langevinPistonTemp $temperature
useFlexibleCell no
useGroupPressure no
fixedAtomsForces off\n\n''')
        file.write("# PBC\n")
        with open('coords.txt','r') as f:
            F = f.read()
            file.write(F)
        file.write('''wrapAll                 on
dcdUnitCell             yes


# Scripting

minimize            1000
reinitvels          $temperature
run                 10000000
''')




main(sys.argv[1],sys.argv[2])
