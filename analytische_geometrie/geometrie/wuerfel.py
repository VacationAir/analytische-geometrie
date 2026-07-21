import math
from .gerade import Gerade
from .ebene import Ebene
from .fassade import Fassade
from ..utils.vector_utils import Vector

class Wuerfel:
    def __init__(self, P_min, P_max):
        self.p_min = Vector(P_min)
        self.p_max = Vector(P_max)
        self.a = (self.p_max-self.p_min).mod()/math.sqrt(3)

        x0, y0, z0 = self.p_min.x, self.p_min.y, self.p_min.z
        x1, y1, z1 = self.p_max.x, self.p_max.y, self.p_max.z

        # Vértices del cubo
        v1 = Vector(x0, y0, z0)
        v2 = Vector(x1, y0, z0)
        v3 = Vector(x1, y1, z0)
        v4 = Vector(x0, y1, z0)
        
        v5 = Vector(x0, y0, z1)
        v6 = Vector(x1, y0, z1)
        v7 = Vector(x1, y1, z1)
        v8 = Vector(x0, y1, z1)

        # Creas las 6 fachadas/caras
        self.unten  = Fassade(v1, v2, v3, v4)
        self.oben   = Fassade(v5, v6, v7, v8)
        self.vorne  = Fassade(v1, v2, v6, v5)
        self.hinten = Fassade(v4, v3, v7, v8)
        self.links  = Fassade(v1, v4, v8, v5)
        self.rechts = Fassade(v2, v3, v7, v6)

        self.flaechen = [self.unten, self.oben, self.vorne, self.hinten, self.links, self.rechts]

    def flaecheninhalt(self):
        A = 0

        for F in self.flaechen:
            A += F.flaecheninhalt()

        return A
    
    def volumen(self):
        M = self.vorne.flaecheninhalt()
        h = self.a

        return M * h
    
    def umkugel_radius(self):
        return self.a/2
    
    def enthaelt_punkt(self, Q):
        q = Vector(Q)
        return (self.p_min.x <= q.x <= self.p_max.x and self.p_min.y <= q.y <= self.p_max.y and self.p_min.z <= q.z <= self.p_max.z)
    
    def flaeche_enthaelt_punkt(self, Q):
        for F in self.flaechen:
            if F.enthaelt_punkt(Q):
                return True
            
        return False

    def mittelpunkt(self):
        return Vector((self.p_max-self.p_min) *0.5)
    
    def punkt_in_kante(self, Q):
        for F in self.flaechen:
            if F.punkt_in_kante(Q):
                return True
            
        return False

    def punkt_in_ecke(self, Q):
        for F in self.flaechen:
            if F.punkt_in_ecke(Q):
                return True
            
        return False
    
    def schnitt_gerade(self, G: Gerade):
        ergebnis = []
        for F in self.flaechen:
            S = F.schnitt_gerade(G)
            if S is not None:
                ergebnis.append(S)

        return ergebnis

    def schnitt_ebene(self, E: Ebene):
        ergebnis = []
        for F in self.flaechen:
            ergebnis.append(F.schnitt_ebene(E))

        return ergebnis

    def schnitt_fassade(self, F2: Fassade):
        ergebnis = []
        for F in self.flaechen:
            ergebnis.append(F.schnitt_fassade(F2))

        return ergebnis
    
    def abstand_punkt(self, Q):
        D = []
        for F in self.flaechen:
            D.append(F.abstand_punkt(Q))

        return min(D)
    
    def abstand_gerade(self, G: Gerade):
        D = []
        for F in self.flaechen:
            D.append(F.abstand_gerade(G))

        return min(D)


    def abstand_ebene(self, E: Ebene):
        D = []
        for F in self.flaechen:
            D.append(F.abstand_ebene(E))

        return min(D)
    
    def abstand_fassade(self, F2):
        D = []
        for F in self.flaechen:
            D.append(F.abstand_fassade(F2))

        return min(D)
    
    def lage_gerade(self, G: Gerade, flaeche: Fassade = None):
        if flaeche is None:
            ergebnis = []
            for F in self.flaechen:
                ergebnis.append(F.lage_gerade(G))

            return ergebnis
        else:
            return flaeche.lage_gerade(G)

    def lage_ebene(self, E: Ebene, flaeche: Fassade = None):
        if flaeche is None:
            ergebnis = []
            for F in self.flaechen:
                ergebnis.append(F.lage_ebene(E))

            return ergebnis
        
        else:
            return flaeche.lage_ebene(E)
        
    def lage_fassade(self, F2: Fassade, flaeche: Fassade = None):
        if flaeche is None:
            ergebnis = []
            for F in self.flaechen:
                ergebnis.append(F)

            return ergebnis
        
        else:
            return flaeche.lage_fassade(F2)
        
    def lage_wuerfel(self, W2: "Wuerfel"):
        """
        auf_kante
        auf_flaeche
        auf_eckpunkt
        ist_enthalten
        enthaelt
        ausser
        identisch
        parallel
        schneidend
        """

        if self.p_min == W2.p_min and self.p_max == W2.p_max:
            return "identisch"
        
        elif self.enthaelt_punkt(W2.p_min) and self.enthaelt_punkt(W2.p_max):
            return "enthaelt"
        
        elif W2.enthaelt_punkt(self.p_min) and W2.enthaelt_punkt(self.p_max):
            return "ist_enthalten"
        
        anzahl_schnitte = 0
        anzahl_flaechen = 0
        anzahl_eckpunkte = 0
        anzahl_kanten = 0
        anzahl_parallel = 0

        for F1 in self.flaechen:
            for F2 in W2.flaechen:
                lage = F1.lage_fassade(F2)
                if  lage == "identisch":
                    anzahl_flaechen += 1
                
                elif lage == "beruehrend":
                    anzahl_eckpunkte += 1
                
                elif lage == "schneidend":
                    anzahl_schnitte += 1

                elif lage == "parallel":
                     anzahl_parallel +=1

                for K1 in F1.kanten:
                    for K2 in F2.kanten:
                        if K1.lage_gerade(K2) == "identisch":
                            anzahl_kanten += 1
                        
        if anzahl_schnitte > 0:
            return "schneidend"
        
        if anzahl_flaechen > 0:
            return "auf_flaeche"
        
        if anzahl_kanten > 0:
            return "auf_kante"
        
        if anzahl_eckpunkte > 0:
            return "auf_eckpunkt"
        
        if anzahl_parallel > 0:
            return "parallel"
        
        return "ausser"