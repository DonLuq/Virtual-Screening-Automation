"""Short script just to prepare protein for MD calculations,
adding waters, adding ions and creating psf file with parameters for MD calculations.
To use script provide pdb file with protein, ligand pdb file, ligand param file,
For ligand param file use optional swissparam.ch online ---> use initial mol2 file from base
To obtain ligand pdb converted lines from dok file are needed
exmaple >>> MDAnalysis.Universe('best.mol2').atoms.write('best.pdb')"""

import subprocess
import os

def main(prot_name,ligand_name,ligand_param,ios_conc=0.15):
    short_name = os.path.basename(prot_name).split('.')[0]
    param_name = os.path.basename(ligand_name).split('.')[0]
    temp_name = os.path.basename(ligand_name).split('.')[0]
    temp_iter = 1

    if os.path.isdir(temp_name):
        while os.path.isdir(temp_name):
            temp_name = param_name+"__" + str(temp_iter)
            temp_iter += 1
        subprocess.run(['mkdir',temp_name])
    else:
        subprocess.run(['mkdir',temp_name])
    os.chdir(temp_name)
    subprocess.run(['cp','../'+prot_name,'.'])
    subprocess.run(['cp','../'+ligand_name,'.'])
    subprocess.run(['cp','../'+ligand_param,'.'])
    subprocess.run(['cp','-r','../required_files','.'])

    with open(str(short_name)+'.tcl', 'w') as file:
        file.write('#RUN with vmd -dispdev text -e script_name.tcl\n')
        file.write(
            'package require psfgen \npackage require solvate \npackage require autoionize\n')
        # file.write('\npsfgen_logfile '+short_name+'.log\n\n')
        file.write('''
topology required_files/top_all36_carb.rtf
#topology required_files/top_all36_cgenff.rtf
topology required_files/top_all36_lipid.rtf
topology required_files/top_all36_na.rtf
topology required_files/top_all36_prot.rtf
topology required_files/toppar_water_ions_namd.str\n''')
        file.write('topology '+os.path.basename(ligand_param))
        file.write('''

pdbalias residue HIS HSP
pdbalias atom ILE CD1 CD
pdbalias atom TIP3 O OH2
pdbalias atom ILE CD1 CD
pdbalias atom SER HG HG1
pdbalias atom LYS 1HZ HZ1
pdbalias atom LYS 2HZ HZ2
pdbalias atom LYS 3HZ HZ3
pdbalias atom ARG 1HH1 HH11
pdbalias atom ARG 2HH1 HH12
pdbalias atom ARG 1HH2 HH21
pdbalias atom ARG 2HH2 HH22
pdbalias atom ASN 1HD2 HD21
pdbalias atom ASN 2HD2 HD22
pdbalias residue HOH TIP3
pdbalias atom TIP3 O OH2\n\n''')
        file.write('segment PROT {\n pdb '+prot_name+'\n# mutate 18 GLU\n}\n\n')
        # file.write('segment WAT {\n pdb '+name+'\n auto none\n}\n\n')  # <------- Zmienic odnosnik
        file.write('segment LIG {\n pdb '+ligand_name+'\n first none\n last none\n}\n\n')
        file.write('coordpdb '+prot_name+' PROT\n')
        # file.write('coordpdb 2wq1_water.pdb WAT\n\n')  # <------- Zmienic odnosnik
        file.write('coordpdb '+ligand_name+' LIG\n\n')
        file.write('guesscoord\n\n')
        # file.write('source ligand.psfgen\n\n')
        file.write('writepsf step1.psf\n')
        file.write('writepdb step1.pdb\n\n')
        file.write("# Use the solvate plugin to add water in rectangular box\n# with 7A padding\n\n")
        file.write('solvate step1.psf step1.pdb -t 7 -o step2\n\n')
        file.write('autoionize -psf step2.psf -pdb step2.pdb -sc '+str(ios_conc)+' between 7 -o '+short_name+'_MD\n')
        file.write('quit\n')
        #Execute the script
        # A = subprocess.run(['vmd','-dispdev','text','-e','/'+short_name+'.tcl'])
        # subprocess.run(['vmd','mol','load','pdb','../pro13/pro_MD.pdb'])
        # A.args(['source','pro.tcl'])
        print(os.getcwd())
        # import vmd
        # vmd.build_parser(['vmd','-dispdev','text','-e',short_name+'.tcl'])
        # from vmd import evaltcl
        # os.system(r'vmd -dispdev text -e pro.tcl')
        # os.system('vmd -e '+short_name+'.tcl')

# -e subsprocess -> script
# - ls
import sys

if len(sys.argv)==3:
    try:
        main(sys.argv[1],sys.argv[2])
    except:
        print('Invalid parameters on input')
        print(sys.argv[1:])
elif len(sys.argv) == 4:
    try:
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    except:
        print('Invalid parameters on input')
        print(sys.argv[1:])
else:
    print('ARGS = prot_name.pdb, ligand_name.pdb,lingand param file, ions_concentration(0.15)')
    sys.exit()


