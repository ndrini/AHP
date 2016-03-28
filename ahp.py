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
import numpy as np
# import ML

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

    def equiparo_lunghezze(self, lista):
        """max(mylist, key=len)"""
        a = len(max(lista, key=len))        # trovo la lunghezza del valore + lungo
        for i in range(len(lista)):
            # print len(lista[i]) 
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
        [g_c.append( [0] * len(x) ) for i in range(len(x))]   # appendo la stessa variabile (che punta alla ipse lista a!!!)
        for i in range(l):          # vale 0 --> 3
            for j in range(l):      # vale 0 --> 3
                if j == i: 
                    g_c[i][i] = 1
                if j > i:
                    testo = "Giudizio di" + x[i] + "rispetto a" +  x[j] + ": ..."    # cambia!!
                                    # era "Giudizio di", x[i], "rispetto a", x[j], ": ..."
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

        # stampo la matrice di confronto dei criteri
        intestazione = "\t\t\t" + crit[0]
        for j in range(1, len(g_c[0])):          # per tutti i criteri
            intestazione += "\t"+crit[j] 
        print intestazione
        for i in range(len(g_c)):
            numeri = [str(g_c[i][j]) for j in range(len(g_c[0]))]
            print '\t', crit[i],'\t', "\t\t".join(numeri)   #  join
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
                print '\t » Has juzgado', opz[i],'\t segun el criterio',crit[j],'\tcon un', G[i][j] 
                # print frase
        self.separatore()

        # stampo la matrice dei giudizi
        intestazione = "\t\t" + crit[0]
        for j in range(1, len(G[0])):          # per tutti i criteri
            intestazione += "\t"+crit[j] 
        print intestazione
        for i in range(len(G)):
            numeri = [str(G[i][j]) for j in range(len(G[0]))]
            print '\t', opz[i],'\t', "\t\t".join(numeri)   #  join
        self.separatore()

    def giudizio_da_matrice(self, C = [[1, 3, 9], [0.33, 1, 6], [1/9, 1/6, 1]]): 
        """ attribuisco ad ogni riga i pesi partendo 
            dalla matrice di confonto binario C        """ 
        C = np.matrix(C)        # trasformo in matrice
        C.astype('float')    
        g = C.sum(axis=1)
        return g /sum(g)   # restituisco normalizzato


    def risultato(self, opz = ['o1', 'o2'], c = ['c1', 'c2', 'c3',], \
        G = [[5, 8, 2], [1, 9, 3]], C = [[1, 3, 9], [0.33, 1, 6], [1/9, 1/6, 1]]):
        """ G i giudizi delle opzioni rispetto ai criteri
            C la matrice di confronto dei criteri  
                a. ottengo i pesi normalizzati dei criteri g_c
                b. moltiplico il giudizio G (normalizzato) per g_c
                c. stampo il risultato  
        """
        print "El resultado de la elaboracion ha sido:"
        g_c = self.giudizio_da_matrice(C)

        ris = []        # serve per il grafico

        R = G * g_c    # {2 · 3} {3·1}      = {2·1}
        for j in range(len(opz)):
            print "\tLa alternativa ", opz[j], "\ttiene judicio global de", "{:6.4f}".format(float(R[[j], :])) 
            
            # ris.append([opz[j], float(R[[j], :]) )
            ris.append(float(R[[j], :]) )
        self.separatore()
        print "La alternativa mejor ha resultado", opz[ris.index(max(ris))], \
               "con un judicio de ", "{:6.4f}".format(max(ris)), ".\n\n"
        
        
        plt.bar(range(len(opz)), ris)
        plt.ylim(0,1.2*max(ris))
        plt.title('Histograma del judicio con AHP')
        plt.xlabel('Alternativas')
        plt.ylabel('Evaluacion')    # si pianta con 'Evaluación'
        plt.axhline(y=max(ris))     # http://matplotlib.org/examples/pylab_examples/axhspan_demo.html
        plt.xticks(range(len(opz)), opz, rotation=45)  # http://matplotlib.org/examples/ticks_and_spines/ticklabels_demo_rotation.html
        
        """
        """
        plt.show()

    def esecuzione(self, opz = ['o1', 'o2', 'o3',], 
                         crit = ['c1', 'c2', 'c3', 'c4', ], 
                         G = [[10, 9, 8, 7], [9, 8, 7, 6], [8, 7, 6, 5]],
                         g_c = [[  1, 10,  5, 2], 
                                [0.1,  1, 10, 4], 
                                [0.2, .1,  1, 5], 
                                [0.5,.25, .2, 1]]):          # permetto di eseguire lo script 
        """ faccio chiedere i valori se lo richiamo come 
        """
        if opz == []:               
            opz = self.in_opz()
        self.equiparo_lunghezze(opz)
        testo_opz = 'juzgando la "mejor" entre estas alternativas (opciones):'
        self.show_opz(opz, testo_opz )
        self.stop()

        if crit == []: 
            crit = self.in_crit()
        self.equiparo_lunghezze(crit)
        testo_crit = 'utilizando estos criterios:'
        self.show_opz(crit, testo_crit)
        self.stop()

        # print "le opzioni sono", opz,"i criteri sono", crit 
        """ ora che ho raccolto i criteri e le opzioni, 
            a. prima giudico le opzioni, rispetto ai criteri
            b. poi giudico l'importanza dei criteri
            c. infine do il risultato """
        # a. 
        if G == []:
            G = self.giudico_opzioni_in_base_ai_criteri(opz, crit)
        self.show_giudizio_opz_su_crit(opz, crit, G)
        self.stop()

        # b. 
        if  g_c == []:
            g_c = self.confronto_criteri(crit)    
        self.show_confronto_criteri(crit, g_c) 
        self.stop()

        self.risultato(opz, crit, G, g_c)
        self.stop()

# Esecuzione ========================================
if __name__ == "__main__":
    print(chr(27) + "[2J")
    a1 = ahp()
    # opz = a1.in_opz()
    # crit = a1.in_crit()

    # a1.risultato()
    # a1.giudico_opzioni_in_base_ai_criteri()
    # a1.esecuzione(opz = []) 
    # a1.esecuzione() 

    a1.esecuzione(  opz = ['gato', 'perro', 'pez',], 
                    crit = ['autonomia', 'economia', 'compañia', 'belleza'], 
                         G = [[10, 7, 7, 9], [5, 5, 10, 7], [10, 9, 2, 5]],   # [], #
                         g_c = [[    1,  8,  7, 9],                           # se voglio immetterle a mano  
                                [0.125,  1,  7, 8], 
                                [ 0.14,.11,  1, 7], 
                                [0.111,.12,.11 , 1]])