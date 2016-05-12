# -*- coding: utf-8 -*-
# Obiettivo: valutare come sono variati i pazienti nel tempo
""" eseguo un AHP

    Attenzione: script va eseguito in python, non in sublime!!
                Se in sublime ottengo errore
                                      EOFError: EOF when reading a line

    posizione in /home/ca/Dropbox/Dojo Python/AHP/    
    """
# import unittest 
import os
import matplotlib.pyplot as plt
import shutil
import numpy as np
# import ML

HERE = os.path.dirname(os.path.realpath(__file__))

def fench_files(relative_path):   # relative path
    # retrive files from a certain directory
    # files = [f for f in os.listdir(HERE+"/"+relative_path) if path.isfile(f)]
    files = [f for f in os.listdir(HERE+"/"+relative_path) \
             if os.path.isfile(os.path.join(HERE +"/"+relative_path, f))]
    print "Founded file/s: ", files, "\n"
    return files

class ahp():

    def input(self, testo = "Scrivi l'input\n»"):
        s = []
        l = []
        while s != '###':
            s = []
            s = raw_input(testo)        # ottengo una stringa s con tutti gli elementi del primo nome
            print s
            l.append(s)          # separatore.join(s)  separatore.join(lista)
        return l[:-1]
    
    def stop(self):
        raw_input("»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»\n\n")
        pass

    def smart_div(self, testo):
        # allow text value to have this form 1/2,
        # with the result of float(smart_div("1/2"))= 0.5
        if "/" in testo:
            b = testo.split("/")
            return int(b[0]) / float(b[1])
        else:
            return testo

    def remove_CC(self, case):
        due = case.split("_CC")                                                                                                                                                                                                                                                                                                                                                             
        return ("").join(due)
 
    def prepara_file(self, nome_file):
        """ inside choices"""
        H = HERE +'/choices/'
        new_name = self.remove_CC(nome_file)
        shutil.copy2( H + nome_file, H + new_name)
        
        # with open(HERE +'/choices/' + new_name, a):

        a = self.inpt_from_file(nome_file)
        self.equiparo_lunghezze( a[0]) 
        self.equiparo_lunghezze( a[1])
        with open( H + new_name, 'a') as f: 
            f.write('\n[:giud:]        solo da 0 a 10 \n')
            for i in a[1]: 
                f.write('\t\t'+ i + "\t\t# \n")
                for j in a[0]: 
                    f.write('\t' + j + '\t\t-->          --> \n' )
            f.write('[/:giud:] \n')

            f.write('\n[:g_c:]        from 1/10 to 10 rate the left lower criterio against the upper right   \n')
            l = a[1]
            while len(l) > 1 :
                temp = l[0]
                l.pop(0)
                for i in l:
                    f.write( '\t\t\t' + i + '\n') 
                    f.write('\t' + temp + '\t\t -->            -->\n') 
            f.write('[/:g_c:] \n')

    def che_riga(self, numero, giud = ["a","b","c","e","f","g"],):
        # for a number, return the position (row and column) in a 
        # triangular matrix 
        # all values are stored in a dictionay, called riga_colonna
        num = 0            # initial value of numero
        # i = 0              # erase!!    
        riga = 0           # initial row number
        riga_colonna = {}  # row and column for each number in a list
        while riga < len(giud):  #only for valid row
            # print "riga: ", riga
            num_last = num + len(giud) - 1 - riga # last row number + 1
            # print "-- num_last + 1:", num_last 
            num_iniz = num
            for j in range(num, num_last):
                riga_colonna[j]= (riga, riga + 1 + j - num_iniz )   # (j)%(len(giud)) 
                # print "\t\tj: ", j
                # print "\triga_colonna[",j,"]:", riga_colonna[j]
                num += 1
            num_last =  num + len(giud) - 1 - riga
            riga += 1
            # print "\t\t\tnum aggiornato:", num 
        # print riga_colonna

        return riga_colonna[numero]

    def gira_matrice(self, opz = ["a","b","c"], 
        li = ['10', '5', '10',   
              '7', '5', '9',
              '7', '10', '2',
              '9', '7', '5']):
        # from a list of string values a list of float

        # print sum([int(j) for j in li])
        max_ = len(li)/len(opz)
        # print max_
        varie = []
        for a in range(len(opz)):
            # print "a:",a
            sublist = []
            i=0
            while i < len(li)/len(opz):          # 3 ? 
                sublist.append(int(li[a+i*len(opz)])) 
                i +=1
            varie.append(sublist)
        return varie


    def componi_matrice(self, giud = ["a","b","c", "e"], g_c_half = ['8', '7', '9', '7', '8', '7']):
        l = len(giud)   # numbers of criterias  
        # # print "numbers of criterias:", l     
        matrice = [[] for x in range(l)]   # initialize the matrix as a list of list
        # print "First version of the matrix:\n", matrice
        for j_r in range(l):               # initialize the matrix with lower and diagonal values
            # # print j_r
            for j_c in range(l):
                if j_c < j_r:  
                    matrice[j_r].append(0)
                if j_c == j_r:  
                    matrice[j_r].append(1)
        # print "Second version of the matrix:\n", matrice

        #cont = l - 1   # the number of active rows
        for i in range(len(g_c_half)):
            
            matrice[self.che_riga(i, giud)[0]].append(float( self.smart_div(g_c_half[i]) ))
                # exchange row and column
            matrice[self.che_riga(i, giud)[1]][self.che_riga(i, giud)[0]] = float(1.0/float( self.smart_div(g_c_half[i]))) 
            
            # @ matrice[]
            # cont -= 1            

        # }    matrice = [[1],]
        """
        for i in range(l-1):
            matrice[0].append(g_c_half[i])
        """
        # # print "Third version of the matrix:\n", matrice
        return matrice

    def inpt_from_file(self, nombre, c="/choices/"):
        """ read variables from a file in a choice_all directory """
        variabili = [] 
        opz_lines, crit_lines, giud_lines , g_c_lines = [], [], [], []     
        opz_ok, crit_ok, giud_ok, g_c_ok = False, False, False, False 
        with open( HERE+ c + nombre, 'r') as data:
            lines = [line for line in data.readlines()]  
            for i in lines:
                if i[:7] == "[:opz:]":
                    opz_ok = True
                if i[:8] == "[/:opz:]":
                    opz_ok = False
                if opz_ok:
                    opz_lines.append(i)

                if i[:8] == "[:crit:]":
                    crit_ok = True
                if i[:9] == "[/:crit:]":
                    crit_ok = False
                if crit_ok:
                    crit_lines.append(i)

                if i[:8] == "[:giud:]":
                    giud_ok = True
                if i[:9] == "[/:giud:]":
                    giud_ok = False
                if giud_ok:
                    giud_lines.append(i)

                if i[:7] == "[:g_c:]":
                    g_c_ok = True
                if i[:8] == "[/:g_c:]":
                    g_c_ok = False
                if g_c_ok:
                    g_c_lines.append(i)

                    
        # # # print opz_lines, "\n", crit_lines, "\n", giud_lines  # ok

        opz_clean = []
        for testo in opz_lines:
            if testo[:7] != "[:opz:]":
                opz_clean.append(testo.split("#")[0].strip())
        """    
        # print len(opz_clean), opz_clean """
        variabili.append(opz_clean)
        # print variabili
        
        crit_clean = []
        for testo in crit_lines:
            if testo[:8] != "[:crit:]":     
                crit_clean.append(testo.split("#")[0].strip())  
        variabili.append(crit_clean)

        giud_clean = []
        for testo in giud_lines:
            if testo[:8] != "[:giud:]":
                if "-->" in testo:
                    giud_clean.append(testo.split("-->")[1].strip())  # was int()
        # print giud_clean
        variabili.append(self.gira_matrice(variabili[0], giud_clean))

        # HERE!!!
        g_c_clean = []
        for testo in g_c_lines:
            if testo[:7] != "[:g_c:]":
                if "-->" in testo:
                    g_c_clean.append(testo.split("-->")[1].strip())
        """    
        # print len(opz_clean), opz_clean """
        variabili.append(self.componi_matrice(crit_clean, g_c_clean))

        # print variabili
        # print g_c_clean

        # print variabili
        return variabili    

    def equiparo_lunghezze(self, lista):
        """max(mylist, key=len)"""
        a = len(max(lista, key=len))        # trovo la lunghezza del valore + lungo
        for i in range(len(lista)):
            # # print len(lista[i]) 
            b = a - len(lista[i])
            lista[i] = lista[i]+ " "*b      # equiparo la lunghezza al massimo
        return lista

    def in_opz(self):
        testo = "Scrivi le diverse opzioni far cui scegliere e separale con l'invio \
        alla fine della lista termina la procedura ripetendo tre volte il carattere #, \
        che apparira, quindi, come ###: \n» "
        opz = self.input(testo)
        return opz

    def separatore(self):
        print '_'*65, '\n\n'

    def show_opz(self, cosa, testo): 
        """ mostro opzioni e criteri"""
        print 'Estas', testo
        for i in cosa:
            print "\t # ", i
        self.separatore()

    def in_crit(self):
        testo = "Scrivi i crireti secondo cui giudicare le opzioni\
        alla fine della lista termina la procedura ripetendo tre volte il carattere #, \
        che apparira, quindi, come ###: \n» "
        crit = self.input(testo)
        return crit

        """ a questo punto devo confrontare e pesare, opzioni fra di loro, criteri fra di loro, 
            attribuire i criteri alle opzioni e calcolare il risultato """

    def normalizzazione(self, values, x_min, x_max, tipo = "linear"):
        """lineare or Square or Square Root 
            https://www.mathsisfun.com/sets/function-inverse.html 
            uso Square          se voglio differenziare maggiormente i valori alti
            uso Square Root     se voglio differenziare maggiormente i valori bassi """
        values = np.array([float(i) for i in values])
        if tipo == "linear": 
            v = (values - x_min) / (x_max - x_min)
        elif tipo == "Square": 
            v = (np.power(values,2) - np.power(x_min,2)) / (np.power(x_max,2) - np.power(x_min,2))    
        elif tipo == "Square Root": 
            v = (np.sqrt(values) - np.sqrt(x_min)) / (np.sqrt(x_max) - np.sqrt(x_min))    
        return v

    def confronto_criteri(self, x = ['c1', 'c2', 'c3', 'c4', 'c5'] ):
        """ con normalizzazione di dati nuemrici:
            chiedendo il minimo, il massimo e se è lineare la differenza 
              o logaritmica o quadratica """
        l = len(x)
        g_c = []
        [g_c.append( [0] * len(x) ) for i in range(len(x))]   
        # appendo la stessa variabile (che punta alla ipse lista a!!!)
        for i in range(l):          # vale 0 --> 3
            for j in range(l):      # vale 0 --> 3
                if j == i: 
                    g_c[i][i] = 1
                if j > i:
                    testo = "Giudizio di", x[i], "rispetto a", x[j], ": ..." 
                    g_c[i][j] = input(testo)         # lo giudico
                    g_c[j][i] = 1./g_c[i][j]      # scrivo il valore trasposto
        print "g_c =", g_c
        return g_c

    def show_confronto_criteri(self, crit, g_c): 
        print "Has juzgando la importancia de los criterios como sigue:"
        l = len(crit)
        for i in range(l):          # vale 0 --> 3
            for j in range(l):      # vale 0 --> 3
                if j == i: 
                    pass
                if j > i:
                    print '\t', crit[i], "\tcon respeto a \t", crit[j], "\t:", g_c[i][j]
        self.separatore()

    def giudico_opzioni_in_base_ai_criteri(self, opz = ['o1', 'o2'], c = ['c1', 'c2', 'c3',] ):
        G = []
        v = []
        for j in range(len(opz)):       # per tutte le opzioni, creo una lista di zero
            G.append([0] * len(c))      
        print G
        for j in range(len(G[0])):
            for i in range(len(G)):
                frase = "come giudichi " + opz[i] + " secondo il criterio " + c[j] + "\n »"
                # print frase
                G[i][j] = input(frase)  # 2    self.input(frase)
        print G
        return G

    def show_giudizio_opz_su_crit(self, opz, crit, G):
        """mostro il giudizio """
        print "Has juzgando las alternativas segun los criterios como sigue:"

        for j in range(len(G[0])):          # per tutti i criteri
            for i in range(len(G)):
                print '\t » Has juzgado', opz[i],'\t en función del criterio',crit[j],'\tcon un', G[i][j] 
                # print frase
        self.separatore()

        # stampo la matrice dei giudizi
        intestazione = "\t\t" + crit[0]
        for j in range(1, len(G[0])):          # per tutti i criteri
            intestazione += crit[j] 

        print intestazione
        
             
        for i in range(len(G)):
            # numeri = [G[i][j] for j in range(len(G[0])]
            numeri = [str(G[i][j]) for j in [0,1,2,3]]
            # numeri = ["\t"+str(G[i][j]) for j in [0,1,2,3]]
            print '\t', opz[i],'\t', "\t\t".join(numeri)   #  join

        # '\t segun el criterio',crit[j],'\tcon un', G[i][j] 
                # print frase
        self.separatore()

    def giudizio_da_matrice(self, C = [[1, 3, 9], [0.33, 1, 6], [1/9, 1/6, 1]]): 
        """ attribuisco ad ogni riga i pesi partendo 
            dalla matrice di confonto binario C        """ 
        C = np.matrix(C)        # trasformo in matrice
        C.astype('float')    
        g = C.sum(axis=1)
        return g /sum(g)   # restituisco normalizzato


    def risultato(self, opz = ['o1', 'o2'], c = ['c1', 'c2', 'c3',], \
        G = [[5, 8, 2], [1, 9, 3]], C = [[1, 3, 9], [0.33, 1, 6], [1/9, 1/6, 1]], 
        grafico = "no", verbose = False):
        """ G i giudizi delle opzioni rispetto ai criteri
            C la matrice di confronto dei criteri  
                a. ottengo i pesi normalizzati dei criteri g_c
                b. moltiplico il giudizio G (normalizzato) per g_c
                c. stampo il risultato  
        """
        if verbose:  
            print "El resultado de la elaboracion ha sido:"
        g_c = self.giudizio_da_matrice(C)

        ris = []        # serve per il grafico

        R = G * g_c    # {2 · 3} {3·1}      = {2·1}
        for j in range(len(opz)):
            if verbose:  
                print "\tLa alternativa ", opz[j], "\ttiene judicio global de", "{:6.4f}".format(float(R[[j], :])) 
            
            # ris.append([opz[j], float(R[[j], :]) )
            ris.append(float(R[[j], :]) )
        # self.separatore()
        if verbose:  
            print "La alternativa mejor ha resultado", opz[ris.index(max(ris))], \
               "con un judicio de ", "{:6.4f}".format(max(ris)), ".\n\n"
        
        if grafico == "yes":
            plt.bar(range(len(opz)), ris)
            plt.ylim(0,1.2*max(ris))
            plt.title('Histograma del judicio con AHP')
            plt.xlabel('Alternativas')
            plt.ylabel('Evaluacion')    # si pianta con 'Evaluación'
            plt.axhline(y=max(ris))     # http://matplotlib.org/examples/pylab_examples/axhspan_demo.html
            plt.xticks(range(len(opz)), opz, rotation=45)  # http://matplotlib.org/examples/ticks_and_spines/ticklabels_demo_rotation.html
            
            value_min = -0.5
            value_max_x = len(opz)+0.5
            value_max_y = 10.5
            axes = plt.gca()             # gca stands for 'get current axis'
            axes.set_xlim([value_min, value_max_x])
            axes.set_ylim([value_min, value_max_y])
            plt.annotate(s='', xytext=(value_min, 0), xy=(value_max_x, 0), arrowprops=dict(arrowstyle='->'))
            plt.annotate(s='', xytext=(0,value_min), xy=(0,value_max_y), arrowprops=dict(arrowstyle='->'))
            plt.grid()    # grid
            plt.show()

        #  extract the result as a dictionay -- estraggo il risultato  
        opz_values = dict(zip(opz, ris))
        if verbose:  
            print opz_values
        return opz_values

    def esecuzione(self, opz = ['o1', 'o2', 'o3',], 
                         crit = ['c1', 'c2', 'c3', 'c4', ], 
                         G = [[10, 9, 8, 7], [9, 8, 7, 6], [8, 7, 6, 5]],
                         g_c = [[  1, 10,  5, 2], 
                                [0.1,  1, 10, 4], 
                                [0.2, .1,  1, 5], 
                                [0.5,.25, .2, 1]],
                    grafico = "no"):          # permetto di eseguire lo script 
        """ faccio chiedere i valori se lo richiamo come        """
        if opz == []:               
            opz = self.in_opz()
        self.equiparo_lunghezze(opz)
        testo_opz = 'juzgando la "mejor" entre estas alternativas (opciones):'
        self.show_opz(opz, testo_opz )
        # self.stop()()

        if crit == []: 
            crit = self.in_crit()
        self.equiparo_lunghezze(crit)
        testo_crit = 'utilizando estos criterios:'
        self.show_opz(crit, testo_crit)
        # self.stop()()

        # print "le opzioni sono", opz,"i criteri sono", crit 
        """ ora che ho raccolto i criteri e le opzioni, 
            a. prima giudico le opzioni, rispetto ai criteri
            b. poi giudico l'importanza dei criteri
            c. infine do il risultato """
        # a. 
        if G == []:
            G = self.giudico_opzioni_in_base_ai_criteri(opz, crit)
        self.show_giudizio_opz_su_crit(opz, crit, G)
        # self.stop()()

        # b. 
        if  g_c == []:
            g_c = self.confronto_criteri(crit)    
        self.show_confronto_criteri(crit, g_c) 
        # self.stop()()

        self.risultato(opz, crit, G, g_c, grafico = grafico)
        # # self.stop()()

        # return 

# Esecuzione ========================================
if __name__ == "__main__":
    a1 = ahp()
    for case in fench_files("choices"):
        # print case
        # print type(case)
        if not("_CC" in case):
            v = a1.inpt_from_file(case)
            a1.esecuzione(v[0], v[1], v[2], v[3], grafico = "yes")
        else:
            # print "c'è un _CC !!"
            a1.prepara_file( case )
            # prepare file



        