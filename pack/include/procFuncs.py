#######################################################
# Module: procFuncs
# Description: module containing the function to create
# 			   Process Class instances.
# Functions included:
#	- createProcess
#	- symetricActionSites
#	- equivalent
#	- replaceZeros
#	- showConfig
#######################################################


from itertools import chain
import random
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

from pack.include.process import Process
from pack.include.latticeFunc import createLattice
from pack.utilities.neighbourgsDicts import neighboursDict, neighboursDict1, neighboursDict2


def createProcess( name, category, activation_energy = None, prefactor = None, rate=None, new_sites = None, old_sites = None, empty = None, shell = None, shells = None, sym6 = False, sym3 = False, atoms = None, sb2=None, sb4 = None, unid = None):
    """
    Function needed to generate Process Class object
    Args:
        name (Str)
        category (Str)
    kArgs :
        activation_energy (Float)
        prefactor (Float)
        rate (Float) : transition rate
        new_sites : (Int or Tuple(int))
        old_sites : (Int or Tuple(int))
        empty (Tuple(Int)) : id numbers of empty sites
        shell (Int) : if a complete shell is empty
        shells (Tuple(Int)) : if many shells are empty
        sym6 (Bool) : if True, also returns symetric processes (following 6-fold symetry)
        sym3 (Bool) : if True, also returns symetric processes (following 3-fold symetry)
        atoms (Tuple(int) or int) : id numbers of sites occupied by atoms
        * sb2 (Tuple(int) or int)   : id numbers of sites occupied by sb2 (DONT USE THIS - not implemented)
        sb4 (Tuple(int) or int)   : id numbers of sites occupied by sb4
        unid (Tuple(int) or int)  : id numbers of sites of unidentified state
    Returns:
        List(Process) : list of all equivalent processes
    """
    # input sanity : verify where either in one or the other of the 2 cases, not both !
    case1 = activation_energy!=None and rate==None
    case2 = activation_energy==None and rate!=None
    assert( not (case1 and case2) ), 'Input activation energy OR transition rate. If process is thermally activated enter activation_energy. If not, enter the rate'

    # rest of the function
    list_of_equiv_proc = []

    t = list(np.arange(0,19))

    empty_sites = []

    conditions = []

    if empty != None:
        if type(empty) == int:
            empty_sites.append(empty)
        else:
            empty_sites += list(empty)

    if shells:
        for i in shells:
            if i == 1:
                empty_sites += t[1:7]
            elif i == 2:
                empty_sites += t[7:19]


    if shell:
        if shell == 1:
            empty_sites += t[1:7]
        elif shell == 2:
            empty_sites += t[7:19]



    if atoms != None:
        if type(atoms) == int:
            conditions.append( (atoms, 2) )
        else:
            for atom in atoms:
                conditions.append( (atom, 2) )


    if sb4 != None:
        if type(sb4) == int:
            conditions.append( (sb4, 4) )
        else:
            for j in sb4:
                conditions.append( (j, 4) )

    if unid != None:
        if type(unid) == int:
            conditions.append( (unid, 0) )
        else:
            for k in unid:
                conditions.append( (k, 0) )

    list_of_config_and_sites = equivalent(category, conditions, empty_sites, sym6_ = sym6, sym3_ = sym3,
    new = new_sites, old = old_sites)

    list_config = list_of_config_and_sites[0]
    list_actionsites = list_of_config_and_sites[1]


    for i in range(len(list_config)):

        config = list_config[i]

        if sym3 == True:
            name__ = name + '_#' +str(i)
        elif sym6 == True:
            name__ = name + '_#'+str(i)
        else:
            name__ = name + '_#' + str(i)

        if category == 'deposition':
            actionsite = None
        elif category == 'evaporation':
            actionsite = None
        else:
            actionsite = list_actionsites[i]

        list_of_equiv_proc.append( Process(name__, category, config, activation_energy=activation_energy, action_sites=actionsite, prefactor=prefactor, rate=rate ) )

    return list_of_equiv_proc


def symetricActionSites(categ, new_ = None, old_ = None, sym6__ = False, sym3__ = False):
    """
    Returns the possible action sites considering the given symetries.
    Args:
        categ (string):
            'diffusion', 'molecule separation', 'molecule creation'
    KArgs:
        new_ ()
        old_
        sym6__
        sym3__
    Returns:
        list
    """

    y = list(np.arange(0,19))
    seg1 = y[1:7]
    seg2 = y[7:19]

    list_of_symetric_sites = []

    if sym3__ == True:

        if categ == 'diffusion':
            index = seg1.index(new_)
            for i in range(3):
                new_site = np.roll(seg1, -i*2)[index]
                list_of_symetric_sites.append(new_site)


        elif categ == 'molecule separation':

            for i in range(3):
                new_sites = []
                for j in new_ :
                    if new_ == 0:
                        new_sites.append(new_)
                    elif j in seg1:
                        index = seg1.index(j)
                        new_site = np.roll(seg1, -2*i)[index]
                        new_sites.append(new_site)
                    elif j in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -4*i)[index]
                        new_sites.append(new_site)
                list_of_symetric_sites.append(new_sites)



        elif categ == 'molecule creation':

            for i in range(3):
                new_sites = []
                olds = []
                for j in old_:
                    if j == 0:
                        olds.append(0)
                    elif j in seg1:
                        index = seg1.index(j)
                        new_site = np.roll(seg1, -2*i)[index]
                        olds.append(new_site)
                    elif j in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -4*i)[index]
                        olds.append(new_site)

                new_sites.append(olds)

                if new_ == 0:
                    new_sites.append(new_)
                elif new_ in seg1:
                        index = seg1.index(new_)
                        new_site = np.roll(seg1, -2*i)[index]
                        new_sites.append(new_site)
                elif new_ in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -4*i)[index]
                        new_sites.append(new_site)

                list_of_symetric_sites.append(new_sites)

    if sym6__ == True:

        if categ == 'diffusion':
            index = seg1.index(new_)
            for i in range(6):
                new_site = np.roll(seg1, -i)[index]
                list_of_symetric_sites.append(new_site)

        elif categ == 'molecule separation':

            for i in range(6):
                new_sites = []
                for j in new_ :
                    if new_ == 0:
                        new_sites.append(new_)
                    elif j in seg1:
                        index = seg1.index(j)
                        new_site = np.roll(seg1, -1*i)[index]
                        new_sites.append(new_site)
                    elif j in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -2*i)[index]
                        new_sites.append(new_site)

                list_of_symetric_sites.append(new_sites)


        elif categ == 'molecule creation':
            for i in range(6):
                new_sites = []
                olds = []
                for j in old_:
                    if j == 0:
                        olds.append(0)
                    elif j in seg1:
                        index = seg1.index(j)
                        new_site = np.roll(seg1, -i)[index]
                        olds.append(new_site)
                    elif j in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -2*i)[index]
                        olds.append(new_site)
                new_sites.append(olds)

                if new_ == 0:
                    new_sites.append(new_)
                elif new_ in seg1:
                        index = seg1.index(new_)
                        new_site = np.roll(seg1, -i)[index]
                        new_sites.append(new_site)
                elif new_ in seg2:
                        index = seg2.index(j)
                        new_site = np.roll(seg2, -2*i)[index]
                        new_sites.append(new_site)

                list_of_symetric_sites.append(new_sites)

    return list_of_symetric_sites






def equivalent(category_, conditions_, empty_, sym6_ = False, sym3_ = False, new = None, old = None):
    """
    Returns equivalent configurations and sites given the symetries AND the unidentified sites.
    Args:
        same as generate processes
        conditions_ : List(tuples): conditions on certain sites (see condition documentation)
    Returns:
       list_of_equivalent_config, list_of_sites
          list_of_equivalent_config - List(int) :
          list_of_sites - List(action sites*)   :
          *see documentation
    """
    initial_condition = list( np.zeros(19, dtype = int) )

    if empty_:
        for nb in empty_:
            initial_condition[nb] = 1

    if conditions_ != []:
        for condition in conditions_:
            cw = condition[0]
            value = condition[1]
            initial_condition[cw] = value

    # Safety net ------------------
    if np.count_nonzero(initial_condition) < 6 :
        print('Not enough conditions to build equivalent processes')
    #-------------------------------
    else :

        list_of_equivalent_config = []
        list_of_sites = []

        if sym3_ == True:

            sym_sites = symetricActionSites(category_, new_ = new, old_ = old, sym3__ = True)

            seg0 = initial_condition[0]
            seg1 = initial_condition[1:7]
            seg2 = initial_condition[7:19]



            for i in range(3):

                l0 = len(list_of_equivalent_config)
                seg1_ = list( np.roll(seg1, i*2) )
                seg2_ = list( np.roll(seg2, i*4) )
                sym_condition = [seg0] + seg1_ + seg2_
                replaceZeros(sym_condition, list_of_equivalent_config,
                action_sites = sym_sites[i], category =category_)
                l1 = len(list_of_equivalent_config)
                if sym_sites:
                    for j in range(l1 - l0):
                        list_of_sites.append(sym_sites[i])


        elif sym6_ == True:

            sym_sites = symetricActionSites(category_, new_ = new, old_ = old, sym6__ = True)

            seg0 = initial_condition[0]
            seg1 = initial_condition[1:7]
            seg2 = initial_condition[7:19]

            for i in range(6):
                l0 = len(list_of_equivalent_config)
                seg1_ = list( np.roll(seg1, i) )
                seg2_ = list( np.roll(seg2, i*2) )

                sym_condition = [seg0] + seg1_ + seg2_
                replaceZeros(sym_condition, list_of_equivalent_config,
                action_sites = sym_sites[i], category =category_)
                l1 = len(list_of_equivalent_config)
                if sym_sites:
                    for j in range(l1 - l0):
                        list_of_sites.append(sym_sites[i])


        else:

            replaceZeros(initial_condition, list_of_equivalent_config,
            action_sites = new, category =category_ )

            if category_ == 'diffusion':
                for k in range(len(list_of_equivalent_config)):
                    list_of_sites.append(new)
            if category_ == 'molecule creation':
                for k_ in range(len(list_of_equivalent_config)):
                    list_of_sites.append([old, new])
            if category_ == 'molecule separation':
                for k__ in range(len(list_of_equivalent_config)):
                    list_of_sites.append(new)

        for config in list_of_equivalent_config:   ## ok
            for i in range(len(config)):
                if config[i] != 4:
                    config[i] -=1


        return list_of_equivalent_config, list_of_sites


def replaceZeros(t, list_,  action_sites = None,  category = None):
    """
    Recursive function
    Appends to list_ all possibilities generated by replacing the zeros in t by 1 (empty), 2 (atom) or 4 (Sb4).
    Args:
        t (List)    : list from which the other lists are generated.
        list_ (List): list where the results are stored
    kwArgs :
        action_sites (list(int) or int)
        category (str)
    Returns:
        None
    """
    if 0 in t:

        n = t.index(0)
        occNeighbours = np.array([ t[index] for index in  neighboursDict[n] ])
        anySb4 = any( occNeighbours == 4 )
        anyAtoms = any( occNeighbours == 2 )

        if category == 'diffusion' and t[0] == 4 : #diffusion de sb4
            anySb4 += action_sites in neighboursDict[n]


        if anySb4:
            ## Check if there's any Sb4 in the first neighbours or a Sb4 that will diffuse in the first neighbors
            # If True, this site has to be empty.
            n1 = t[:n] + [1] + t[n+1:]
            replaceZeros(n1, list_, action_sites = action_sites, category =category)

        else:
            """Vide"""
            n1 = t[:n] + [1] + t[n+1:]
            replaceZeros(n1, list_,  action_sites = action_sites, category =category)

            """Ajouter un atome
            1) Il faut verifier que le site n'a pas plus que 3 voisins et qu'il soit dans la configuration 1-3-5 ou 2-4-6 (avant le processus)
            2) Il faut verifier ce qui arrive aux voisins si on ajoute un atome sur le site n. Tous les voisins doivent etre dans une ou l'autre des configurations
            3) Verifier qu'il n'y a pas de probleme a ajouter un atome sur le site n dependamment du processus : diffusion ou separation de molecule
            """
            # 1)
            occ1 = np.array([ t[index] for index in  neighboursDict1[n] ]) #voisins 1-3-5
            occ2 = np.array([ t[index] for index in  neighboursDict2[n] ]) #voisins 2-4-6
            any1 = any(occ1 ==2) # si aucun voisin 135 any1=0
            any2 = any(occ2 == 2 ) # si aucun voisin 246 any2=0
            siteOK = not (any1*any2) # Si le site est ok, siteOK vaut 1.

            # 2)
            if siteOK:
                t_apres = t[:];  t_apres[n] = 2;
                voisinsOK =1
                for voisin in neighboursDict[n]:
                    if t[voisin] == 2:
                        occ1 = np.array([ t_apres[index] for index in  neighboursDict1[voisin] ]) #voisins 1-3-5
                        occ2 = np.array([ t_apres[index] for index in  neighboursDict2[voisin] ]) #voisins 2-4-6
                        any1 = any(occ1 == 2)
                        any2 = any(occ2 == 2 )
                        voisinOKapres = not (any1*any2)
                        voisinsOK = voisinsOK*voisinOKapres
                # 3)
                if voisinsOK:
                    if category == 'diffusion':
                        if n !=action_sites:
                            t_proc = t_apres[:]; t_proc[0]=1; t_proc[action_sites] = 2;
                            diffOK = 1
                            for voisin in neighboursDict[n]:
                                if t_proc[voisin]== 2:
                                    occ1 = np.array([ t_proc[index] for index in  neighboursDict1[voisin] ]) #voisins 1-3-5
                                    occ2 = np.array([ t_proc[index] for index in  neighboursDict2[voisin] ]) #voisins 2-4-6
                                    any1 = any(occ1 == 2)
                                    any2 = any(occ2 == 2 )
                                    ok = not any1*any2
                                    diffOK = diffOK*ok
                            if diffOK:
                                n2 = t[:n] + [2] + t[n+1:]
                                replaceZeros(n2, list_,  action_sites = action_sites, category =category)


                    elif category == 'molecule separation':
                        if n not in action_sites:
                            t_proc = t_apres[:]; t_proc[0]=1;
                            for action_site in action_sites:
                                t_proc[action_site] = 2
                            diffOK = 1
                            for voisin in neighboursDict[n]:
                                if t_proc[voisin]== 2:
                                    occ1 = np.array([ t_proc[index] for index in  neighboursDict1[voisin] ]) #voisins 1-3-5
                                    occ2 = np.array([ t_proc[index] for index in  neighboursDict2[voisin] ]) #voisins 2-4-6
                                    any1 = any(occ1 == 2)
                                    any2 = any(occ2 == 2 )
                                    ok = not any1*any2
                                    diffOK = diffOK*ok
                            if diffOK:
                                n2 = t[:n] + [2] + t[n+1:]
                                replaceZeros(n2, list_,  action_sites = action_sites, category =category)
                    else : #autres categories
                        n2 = t[:n] + [2] + t[n+1:]
                        replaceZeros(n2, list_, action_sites = action_sites, category =category)



            """ Pour ajouter un Sb4:
            1) Il ne doit pas y avoir d'atome ou de molecule dans les premiers voisins
            2) Regarder si ajouter un Sb4 sur le site n derange la configuration apres le processus
                - Pour la diffusion : l'objet ne doit pas diffuser vers un des sites voisins du site n ou on veut mettre un Sb4
                - Pour la separation de molecule : aucun atome ne doit pas se retrouver sur un des sites voisins du site n ou on veut mettre un Sb4
                - Pour les autres processus il n'y a pas de conditions
            """
            #1)
            if not anyAtoms:
                #2)
                if action_sites :
                    if category == 'diffusion':  #Pour la diffusion, action_sites est un int
                        if not n in neighboursDict[action_sites]:
                            n4 = t[:n] + [4] + t[n+1:]
                            replaceZeros(n4, list_, action_sites = action_sites, category =category)
                    elif category == 'molecule separation':
                        actionSitesOk = True
                        for site in list(action_sites):
                            if n in neighboursDict[site]:
                                actionSitesOk = False
                        if actionSitesOk:
                            n4 = t[:n] + [4] + t[n+1:]
                            replaceZeros(n4, list_, action_sites = action_sites, category =category)
                else : # evaporation et creation de molecule
                    n4 = t[:n] + [4] + t[n+1:]
                    replaceZeros(n4, list_, action_sites = action_sites, category =category)

    else:
        list_.append(t)



def showConfig(process, filename):
    """
    * This is a function just for testing and visualising processes.
    Shows the configuration before a process and after.
    Args:
        process (Process) : the process to visualize
    kwArgs:
        filename (srting) : path to filename to save image
    """
    lattice = createLattice((5,3,1))
    sites_coordinates = [lattice.sites[45].coordinates] + [neighbour.coordinates for neighbour in lattice.sites[45].neighbours]
    # print(sites_coordinates)
    config = process.configuration

    x = []; y = []; o = []

    for k in range(len(config)):
        x.append(sites_coordinates[k][0])
        y.append(sites_coordinates[k][1])
        o.append(config[k])

    X = np.array(x); Y = np.array(y); O = np.array(o)

    action = process.action_sites
    Oa = np.array(o)
    if process.category == 'deposition':
        Oa[0] += 4
    elif process.category == 'evaporation':
        Oa[0] = 0
    elif process.category == 'diffusion':
        value = O[0]
        Oa[0] = 0
        Oa[action] += value
    elif process.category == 'molecule creation':
        value = len(action[0])
        index = action[1]
        for i in action[0]:
            Oa[i] = 0
        Oa[index] += value
    elif process.category == 'molecule separation':
        for i in action:
            Oa[0] -=1
            Oa[i] += 1

    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
    # plt.tight_layout(pad=1.0, w_pad=10.0, h_pad=3)
    plt.xlim(-2e-9,2e-9)
    plt.ylim(-2e-9,2e-9)


    # ax1.scatter(X, Y, c=O, marker = 'o', cmap=plt.cm.get_cmap('PuRd', 4), vmin = 0, vmax = 4 )
    ax1.scatter(X, Y, c=O, marker = 'o')
    ax1.axis('on')

    # ax2.scatter(X,Y, c=Oa, marker = 'o', cmap=plt.cm.get_cmap('PuRd', 4), vmin = 0, vmax = 4 )
    ax2.scatter(X, Y, c=Oa, marker = 'o')
    ax2.axis('on')

    ax1.set_title("Avant")
    ax2.set_title("Apres")

    # plt.show()

    if filename:
        plt.savefig(str(filename), format = "png", transparent = False )
