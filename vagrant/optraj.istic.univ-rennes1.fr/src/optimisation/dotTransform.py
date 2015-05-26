# coding=utf8'''
'''
Ce module sert à transformer des dictionnaires imbriqués, représentant des arbres valués, en représentation dotty

Certains graphes étant très volumineux, zgrviewer ou un équivalent peut être nécéssaire pour exploiter les fichiers .dot produits
'''

def individual(individual, filename, prog="dot"):
    '''
    Transforme un individu en représentation dotty
    
    l'argument est un individu, c'est à dire un dict(numYear, dict(numWeek, setWeek))
    avec setWeek.assigns::dict(num site, set(num worker))
    
    La fonction génère une image png
    
    Args:
        individual l'individu à représenter dict(numYear, dict(numWeek, setWeek))
        filename nom du fichier dans lequel écrire (str)
        prog le programme à utiliser pour l'agencement des noeuds (str)
    '''
    try:
        import pygraphviz as pgv
    except:
        print "pygraphviz ne semble pas installé, arrêt de dotTransform.individual"
        return
    g = pgv.AGraph()
    g.add_node("individual")
    for yearK in individual.keys():
        # création du noeud de l'année
        g.add_node("y{}".format(yearK))
        n1=g.get_node("y{}".format(yearK))
        n1.attr['label']=yearK
        g.add_edge("individual", n1)
        
        for weekK in individual[yearK].keys():
            # création du noeud de la semaine
            g.add_node("y{}:w{}".format(yearK,weekK))
            n2=g.get_node("y{}:w{}".format(yearK,weekK))
            n2.attr['label']=weekK
            g.add_edge(n1, n2)
            
            #création du noeud des assigns
            g.add_node("y{}:w{}:assigns".format(yearK,weekK))
            n3=g.get_node("y{}:w{}:assigns".format(yearK,weekK))
            n3.attr['label']="assigns"
            g.add_edge(n2, n3)
            
            for siteK in individual[yearK][weekK]["assigns"].keys():
                #puis de chaque site
                g.add_node("y{}:w{}:assigns:s{}".format(yearK,weekK,siteK))
                n4=g.get_node("y{}:w{}:assigns:s{}".format(yearK,weekK,siteK))
                n4.attr['label']=siteK
                g.add_edge(n3, n4)
                
                for workerNum in individual[yearK][weekK]["assigns"][siteK]:
                    g.add_node("y{}:w{}:assigns:s{}:o{}".format(yearK,weekK,siteK, workerNum))
                    n5=g.get_node("y{}:w{}:assigns:s{}:o{}".format(yearK,weekK,siteK, workerNum))
                    n5.attr['label']=workerNum
                    g.add_edge(n4, n5)
            
            # création du noeaud des availables Workers
            g.add_node("y{}:w{}:avail".format(yearK,weekK))
            n6=g.get_node("y{}:w{}:avail".format(yearK,weekK))
            n6.attr['label']="availablesWorkers"
            g.add_edge(n2, n6)
            
            for craftNum in individual[yearK][weekK]["availablesWorkers"].keys():
                g.add_node("y{}:w{}:avail:c{}".format(yearK,weekK,craftNum))
                n7=g.get_node("y{}:w{}:avail:c{}".format(yearK,weekK,craftNum))
                n7.attr['label']=craftNum
                g.add_edge(n6, n7)
                
                for qualifNum in individual[yearK][weekK]["availablesWorkers"][craftNum].keys():
                    g.add_node("y{}:w{}:avail:c{}:q{}".format(yearK,weekK,craftNum,qualifNum))
                    n8=g.get_node("y{}:w{}:avail:c{}:q{}".format(yearK,weekK,craftNum,qualifNum))
                    n8.attr['label']=qualifNum
                    g.add_edge(n7, n8)
                    
                    for workerNum in individual[yearK][weekK]["availablesWorkers"][craftNum][qualifNum]:
                        g.add_node("y{}:w{}:avail:c{}:q{}:w{}".format(yearK,weekK,craftNum,qualifNum,workerNum))
                        n9=g.get_node("y{}:w{}:avail:c{}:q{}:w{}".format(yearK,weekK,craftNum,qualifNum,workerNum))
                        n9.attr['label']=workerNum
                        g.add_edge(n8, n9)
            
        g.layout(prog=prog)
        g.draw(filename)
        print "dot {} généré".format(filename)

"""        
def must(must, filename, prog="dot"):
    '''
    Transforme un must en représentation dotty
    
    l'argument est un must, c'est à dire un dict(numYear, dict(numWeek, setWeek))
    avec setWeek.assigns::dict(num site, set(num worker))
    
    La fonction génère une image png
    
    Args:
        must le must à représenter dict(numYear, dict(numWeek, setWeek))
        filename nom du fichier dans lequel écrire (str)
        prog le programme à utiliser pour l'agencement des noeuds (str)
    '''
    import pygraphviz as pgv
    g = pgv.AGraph()
    g.add_node("must")
    for yearK in must.keys():
        # création du noeud de l'année
        g.add_node("y{}".format(yearK))
        n1=g.get_node("y{}".format(yearK))
        n1.attr['label']="y{}".format(yearK)
        g.add_edge("must", n1)
        
        for weekK in must[yearK].keys():
            # création du noeud de la semaine
            g.add_node("y{}:w{}".format(yearK,weekK))
            n2=g.get_node("y{}:w{}".format(yearK,weekK))
            n2.attr['label']="w{}".format(weekK)
            g.add_edge(n1, n2)
            
            for siteK in must[yearK][weekK].keys():
                #puis de chaque site
                g.add_node("y{}:w{}:s{}".format(yearK,weekK,siteK))
                n4=g.get_node("y{}:w{}:s{}".format(yearK,weekK,siteK))
                n4.attr['label']="s{}".format(siteK)
                g.add_edge(n2, n4)
                
                for craftNum in must[yearK][weekK][siteK].keys():
                    g.add_node("y{}:w{}:s{}:c{}".format(yearK,weekK,siteK,craftNum))
                    n7=g.get_node("y{}:w{}:s{}:c{}".format(yearK,weekK,siteK,craftNum))
                    n7.attr['label']="c{}".format(craftNum)
                    g.add_edge(n4, n7)
                    
                    for qualifNum in must[yearK][weekK][siteK][craftNum].keys():
                        g.add_node("y{}:w{}:s{}:c{}:q{}".format(yearK,weekK,siteK,craftNum,qualifNum))
                        n8=g.get_node("y{}:w{}:s{}:c{}:q{}".format(yearK,weekK,siteK,craftNum,qualifNum))
                        n8.attr['label']="q{}".format(qualifNum)
                        g.add_edge(n7, n8)
                        
                        for workerNum in must[yearK][weekK][siteK][craftNum][qualifNum]:
                            g.add_node("y{}:w{}:s{}:c{}:q{}:w{}".format(yearK,weekK,siteK,craftNum,qualifNum,workerNum))
                            n9=g.get_node("y{}:w{}:s{}:c{}:q{}:w{}".format(yearK,weekK,siteK,craftNum,qualifNum,workerNum))
                            n9.attr['label']="w{}".format(workerNum)
                            g.add_edge(n8, n9)
                
        g.layout(prog=prog)
        g.draw(filename)"""

def workerSorted(workerSorted, filename):
    '''
    Créé une image représentant des ouvriers rangées par Craft/Qualif
    
    La fonction génère une image png
    
    Args:
        workerSorted : les identifiant des ouvriers rangés par craft/qualif (dict(Craft.num, dict(id Qualification.num, set(Worker.num))))
        filename : nom du fichier (avec extension)
    '''
    try:
        import pygraphviz as pgv
    except:
        print "pygraphviz ne semble pas installé, arrêt de dotTransform.workerSorted"
        return
    g = pgv.AGraph()
    g.add_node("racine")
    for ncraft in workerSorted.keys():
        g.add_edge("racine", "c{}".format(ncraft))
        for nqual in workerSorted[ncraft].keys():
            g.add_edge("c{}".format(ncraft), "q{}".format(nqual))
            for nworker in workerSorted[ncraft][nqual]:
                g.add_edge("q{}".format(nqual), "o{}".format(nworker))
    g.layout(prog="dot")
    g.draw(filename)
    
def unavailabilities(unavail, filename):
    try:
        import pygraphviz as pgv
    except:
        print "pygraphviz ne semble pas installé, arrêt de dotTransform.individual"
        return
    g = pgv.AGraph()
    g.add_node("racine")
    for year in unavail.keys():
        g.add_edge("racine", "y{}".format(year))
        for week in unavail[year].keys():
            g.add_edge("y{}".format(year), "y{}w{}".format(year,week))
            for nworker in unavail[year][week]:
                g.add_edge("y{}w{}".format(year,week), "y{}w{}o{}".format(year,week,nworker))
    g.layout(prog="dot")
    g.draw(filename)