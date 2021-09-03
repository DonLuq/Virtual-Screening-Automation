#!/usr/bin/python3
import sys, os, subprocess
import threading
from time import time
from datetime import timedelta

START = time()

'''To properly script works
protein and base of 
substances are needed,
 protein.pdb file -> lepro
 base.mol2 -> lefrag'''

def makeConfigFile(proteinToCompare,ligandList = 'ligands.list',dock_str = None):
    'Takes name of file with protein to compare with and ligand list -> returns *Config.file'
    with open(ligandList.split('.')[0]+'Config.file','w') as configFile:
        configFile.write('Receptor \n' + proteinToCompare + '\n\n')
        configFile.write('RMSD \n1.0\n\n')
        if not dock_str == None:
            with open(dock_str,'r') as dockFile:
                ReadFile = dockFile.readlines()
                for element in ReadFile[6:14]:
                    configFile.write(element)
        else:
            configFile.write('Binding pocket \n-2 22\n-39 -11\n12 31\n\n')
            configFile.write('Number of binding poses\n10\n\n')

        configFile.write('Ligands list\n')
        configFile.write(ligandList + '\n')
    return ligandList.split('.')[0]+'Config.file'

def makeLigandsList(nameDirWithMol2Files = '.'):
    'Takes all files started with LIB from given directory -> returns generated files and list with names of files'
    A = os.scandir(nameDirWithMol2Files)
    iter = 0
    nameIter = 0
    for i in A:
        if iter < 10:
            if i.name[:3] == 'LIB' or 'ZIN':
                with open('ligands'+ str(nameIter) +".list", 'a') as ligandLists:
                    ligandLists.write(i.name + '\n')
                    iter +=1
            else:
                pass
        else:
            if i.name[:3] == 'LIB' or 'ZIN':
                nameIter +=1
                iter = 1
                with open('ligands'+ str(nameIter) +".list", 'a') as ligandLists:
                    ligandLists.write(i.name + '\n')
            else:
                pass
    return ['ligands'+str(i)+'.list' for i in range(nameIter+1)]

def makeLigandsListFromFile(proteinFile, subsFile = 'subs.mol2'):
    # subprocess.run(['lefrag', '-flib', '../' + subsFile])
    subprocess.run(['lefrag','-spli', '../' + subsFile])
    # print(os.getcwd(), 'TUTAJ!')


    # subprocess.run(['ledock', proteinFile, subsFile])

#test values viruses-fda.mol2
def main(*args, **kargs):
    '''first argument is base and the second is protein pdb file'''
    print(args)
    try:
        if args[0][1].split('.')[1] or kargs['base'] == 'mol2':
            baseFileMOL2 = args[0][1]
            if os.path.isdir('./temp'):
                pass
                # subprocess.run(['rm','-rf','temp'])
                # os.mkdir('./temp')
            else:
                os.mkdir('./temp')

            os.chdir('./temp')
            # subprocess.run(['cp','../lefrag'])
            # subprocess.run(['cp','../lepro'])
            # subprocess.run(['cp','../ledock'])

            subprocess.run(['lefrag', '-flib', '../' + baseFileMOL2])
            subprocess.run(['lefrag','-spli', 'flib.mol2'])
    except:
        raise Exception('Invalid base argument!')

    try:
        if args[0][2].split('.')[1] or kargs['protein'] == 'pdb':
            proteinFilePDB = args[0][2]
            subprocess.run(['lepro','../'+proteinFilePDB,'.'])
            proteinFilePDB_pro = 'pro.pdb'
            dock_instr = 'dock.in'
            print(proteinFilePDB_pro)
    except:
        raise Exception('Invalid protein argument!')

    ligandsList = makeLigandsList()

    # print(ligandsList)
    listOfConfig = []
    for i in ligandsList:
        listOfConfig.append(makeConfigFile(proteinFilePDB_pro,i,dock_instr))

    print(listOfConfig)

    listOfThreads = [threading.Thread(target=subprocess.run, args=([['ledock',i]])) for i in listOfConfig]
    for i in listOfThreads:
        print("Hello! : Thread -> ",i)
        i.start()

    for i in listOfThreads:
        print("Joining : Thread -> ",i)
        i.join()

    listOfDoksfile = [i for i in os.listdir() if os.path.splitext(i)[1]=='.dok']
    with open('results.txt','w'):
        pass
    for i in listOfDoksfile:
        with open(i) as file:
            firstLine = file.readline()
            secondLine = file.readline()
            temp_value = list(filter(lambda x: x!= '',secondLine.split(' ')))[7]
            if float(temp_value) < -5:
                with open('results.txt','a+') as results:
                    results.write(i+' -> '+ temp_value +'\n')

    listOfQueries = [i.split('.')[0]+'.mol2' for i in listOfDoksfile]
    for i in listOfQueries:
        os.system('cat '+i+' >> query.mol2')
    #print(os.getcwd())
    #print(baseFileMOL2)
    #print(proteinFilePDB)
    #print(proteinFilePDB_pro)
    subprocess.run(['lefrag','-subs','../'+baseFileMOL2]) # --> plik subs.mol2\
    if not os.path.isdir('CompoundDock'):
        os.mkdir('CompoundDock')
    os.chdir('CompoundDock')
    # subprocess.run(['cp','../lefrag'])
    # subprocess.run(['cp','../lepro'])
    # subprocess.run(['cp','../ledock'])
    subprocess.run(['cp','../pro.pdb','.'])

    makeLigandsListFromFile(proteinFilePDB_pro) # --> podzial na molekuly
    listofLigands = makeLigandsList()
    listOfConfig2 = []
    for i in listofLigands:
        listOfConfig2.append(makeConfigFile(proteinFilePDB_pro,i,'../'+dock_instr))

    listOfThreads2 = [threading.Thread(target=subprocess.run, args=([['ledock',i]])) for i in listOfConfig2]
    for i in listOfThreads2:
        #print("Hello! : Thread -> ",i)
        i.start()

    for i in listOfThreads2:
        #print("Joining : Thread -> ",i)
        i.join()

    listOfDoksfile2 = [i for i in os.listdir() if os.path.splitext(i)[1]=='.dok']
    with open('results_molecules.txt','w'):
        pass
    for i in listOfDoksfile2:
        with open(i) as file:
            firstLine = file.readline()
            secondLine = file.readline()
            print(list(filter(lambda x: x!= '',secondLine.split(' '))))
            if len(secondLine.split()) > 5:
                temp_value = list(filter(lambda x: x!= '',secondLine.split(' ')))[7]
                if float(temp_value) < -7:
                    with open('results_molecules.txt','a+') as results:
                        results.write(i+' -> '+ temp_value +'\n')
            else:
                print('Invalid .dok file --> ',i)

    #dokowanie subs.mol2, liczyc i ustawic na -7kcal/mol
    #sciagnac baze -> charm,
    #MD ambertools -> parametryzacja.
    print("FINISHED")


#ledock -subs BAZA.mol2 /// w folderze musi znajdowac sie plik query.mol2 z fragmentami ktora maja zostac znalezione w bazie


main(sys.argv)


STOP = time()

print(str(timedelta(seconds = STOP-START)))
