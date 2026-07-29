import math 
from .vektor import Vektor
from ..utils.linal_utils import linsys_solve, close

class Gerade:
    """
    Repräsentiert eine Gerade im dreidimensionalen Raum.

    Eine Gerade wird durch einen Stützvektor und einen Richtungsvektor
    definiert. Die Parametergleichung lautet: g: x = stutz + r * richtung.

    Parameters
    ----------
    stutzvektor : array_like
        Der Stützvektor (Ortsvektor eines Punkts auf der Geraden).
    richtungsvektor : array_like
        Der Richtungsvektor der Geraden (darf nicht der Nullvektor sein).

    Attributes
    ----------
    stutzvektor : Vektor
        Der Stützvektor der Geraden.
    richtungsvektor : Vektor
        Der Richtungsvektor der Geraden.
    """
    # ======================================================================
    # Konstruktor
    # ======================================================================

    def __init__(self, stutzvektor, richtungsvektor):
        """
        Initialisiert eine neue Gerade mit Stütz- und Richtungsvektor.

        Parameters
        ----------
        stutzvektor : array_like
            Der Stützvektor (Ortsvektor eines Punkts auf der Geraden).
        richtungsvektor : array_like
            Der Richtungsvektor der Geraden (darf nicht der Nullvektor sein).

        Raises
        ------
        ValueError
            Wenn die Vektoren nicht die Dimension 3 haben oder der
            Richtungsvektor der Nullvektor ist.
        """
        self.stutzvektor = Vektor(stutzvektor)
        self.richtungsvektor = Vektor(richtungsvektor)

    @classmethod
    def from_punkte(cls, punkt1, punkt2):
        """
        Erstellt eine Gerade aus zwei gegebenen Punkten.

        Die Gerade verläuft durch die beiden Punkte. Der Richtungsvektor
        ergibt sich aus der Differenz punkt2 - punkt1.

        Parameters
        ----------
        punkt1 : array_like
            Koordinaten des ersten Punkts.
        punkt2 : array_like
            Koordinaten des zweiten Punkts.

        Returns
        -------
        Gerade
            Die durch die beiden Punkte verlaufende Gerade.

        Raises
        ------
        ValueError
            Wenn die Punkte nicht die Dimension 3 haben oder identisch sind.
        """
        p1 = Vektor(punkt1)
        p2 = Vektor(punkt2)
        return cls(p1, p2 - p1)
    
    # ======================================================================
    # Grundlegende Operationen
    # ======================================================================

    def gerade(self, r):
        """
        Berechnet den Punkt auf der Geraden für einen gegebenen Parameter r.

        Die Parametergleichung lautet: x(r) = stutz + r * richtung.

        Parameters
        ----------
        r : float
            Der Parameterwert.

        Returns
        -------
        Vektor
            Der Punkt auf der Geraden.
        """
        return self.stutzvektor + r * self.richtungsvektor

    def quotient_berechnen(self, punkt):
        """
        Berechnet den Parameter r für einen gegebenen Punkt.

        Diese Methode wird intern verwendet, um zu prüfen, ob ein Punkt
        auf der Geraden liegt.

        Parameters
        ----------
        punkt : array_like
            Der zu prüfende Punkt.

        Returns
        -------
        float or None
            Der Parameter r, wenn der Punkt auf der Geraden liegt,
            sonst None.
        """
        punkt = Vektor(punkt)
        losungen_r = []

        for i in range(3):
            if close(self.richtungsvektor[i], 0):
                if not close(punkt[i], self.stutzvektor[i]):
                    return None
            else:
                r = (punkt[i] - self.stutzvektor[i]) / self.richtungsvektor[i]
                losungen_r.append(r)

        if len(losungen_r) == 0:
            return 0.0

        if close(losungen_r, losungen_r[0]):
            return losungen_r[0]

        return None

    def enthaelt_punkt(self, punkt):
        """
        Prüft, ob ein gegebener Punkt auf der Geraden liegt.

        Parameters
        ----------
        punkt : array_like
            Der zu prüfende Punkt.

        Returns
        -------
        bool
            True, wenn der Punkt auf der Geraden liegt, sonst False.
        """
        if self.quotient_berechnen(punkt) != None:
            return True
        else:
            return False
        
    def lotfusspunkt(self, Q):
        AQ = Q- self.stutzvektor
        r = AQ.dot(self.richtungsvektor)/ self.richtungsvektor.dot(self.richtungsvektor)
        
        return self.gerade(r)
    
    # ======================================================================
    # Lagebeziehungen
    # ======================================================================
    
    def lage_gerade(self, g2):
        """
        Bestimmt die Lagebeziehung dieser Geraden zu einer anderen Geraden.

        Die möglichen Lagebeziehungen sind:
        - "identisch": Die Geraden sind identisch.
        - "parallel": Die Geraden sind parallel, aber nicht identisch.
        - "schneidend": Die Geraden schneiden sich in einem Punkt.
        - "windschief": Die Geraden sind windschief (nicht parallel, nicht schneidend).

        Parameters
        ----------
        g2 : Gerade
            Die zweite Gerade.

        Returns
        -------
        str
            Die Lagebeziehung als String: "identisch", "parallel",
            "schneidend" oder "windschief".
        """
        # Zuerst kolinear oder nicht
        kolinear = close(self.richtungsvektor.cross(g2.richtungsvektor),0)
        if kolinear:
            if self.enthaelt_punkt(g2.stutzvektor):
                return "identisch"
            else:
                return "parallel"
        else:
            pq = g2.stutzvektor - self.stutzvektor
            n = self.richtungsvektor.cross(g2.richtungsvektor)
            abstand = abs(pq.dot(n)/n.mod())
            if close(abstand, 0):
                return "schneidend"
            
            else:
                return "windschief"
            
    # ======================================================================
    # Schnittberechnungen
    # ======================================================================

    def schnitt_mit_gerade(self, g2: "Gerade"):
        """
        Berechnet den Schnittpunkt dieser Geraden mit einer anderen Geraden.

        Der Schnittpunkt wird nur für sich schneidende Geraden berechnet.

        Parameters
        ----------
        g2 : Gerade
            Die zweite Gerade.

        Returns
        -------
        Vektor or None
            Der Schnittpunkt, wenn die Geraden sich schneiden,
            sonst None.
        """
        if self.lage_gerade(g2) == "schneidend":
            A = [
                [self.richtungsvektor[0], -g2.richtungsvektor[0]],
                [self.richtungsvektor[1], -g2.richtungsvektor[1]],
                [self.richtungsvektor[2], -g2.richtungsvektor[2]]
            ]

            b = g2.stutzvektor - self.stutzvektor

            losung = linsys_solve(A, b)

            if losung is None:
                return None
            
            return self.gerade(losung[0])
        
        else:
            return None
        
    def spurpunkte_gerade(self):
        """
        Berechnet die Spurpunkte der Geraden.

        Spurpunkte sind die Schnittpunkte der Geraden mit den Koordinatenebenen:
        - S1: Schnitt mit der x1-Achse (x2 = 0, x3 = 0)
        - S2: Schnitt mit der x2-Achse (x1 = 0, x3 = 0)
        - S3: Schnitt mit der x3-Achse (x1 = 0, x2 = 0)

        Wenn die Gerade parallel zu einer Achse ist, wird an dieser Stelle
        None zurückgegeben.

        Returns
        -------
        list
            Eine Liste mit drei Einträgen [S1, S2, S3], wobei jeder Eintrag
            ein Punkt (Vektor) oder None ist.
        """
        S = []
        for i in range(3):
            if self.richtungsvektor[i] != 0:
                r = -self.stutzvektor[i]/self.richtungsvektor[i]
                S.append(self.gerade(r))
            else:
                S.append(None)
        return S

    # ======================================================================
    # Abstandsberechnungen
    # ======================================================================

    def abstand_zu_punkt(self, q):
        """
        Berechnet den Abstand eines Punkts zu dieser Geraden.

        Der Abstand wird über die Formel d = |(q - stutz) x richtung| / |richtung|
        berechnet, wobei x das Kreuzprodukt bezeichnet.

        Parameters
        ----------
        q : array_like
            Der Punkt, dessen Abstand zur Geraden berechnet werden soll.

        Returns
        -------
        float
            Der Abstand des Punkts zur Geraden.
        """
        vektor_pq = q - self.stutzvektor
        kreuzprodukt = vektor_pq.cross(self.richtungsvektor)
        zaehler = kreuzprodukt.mod()
        nenner  = self.richtungsvektor.mod()
        return zaehler/nenner

    def abstand_zu_gerade(self, g2):
        """
        Berechnet den Abstand zwischen dieser Geraden und einer anderen Geraden.

        Der Abstand wird nur für windschiefe Geraden berechnet.
        Für sich schneidende, parallele oder identische Geraden wird None zurückgegeben.

        Parameters
        ----------
        g2 : Gerade
            Die zweite Gerade.

        Returns
        -------
        float or None
            Der Abstand zwischen den Geraden, wenn sie windschief sind,
            sonst None.
        """
        if self.lage_gerade(g2) == "windschief":
            vektor_pq = g2.stutzvektor - self.stutzvektor

            normalvektor = self.richtungsvektor.cross(g2.richtungsvektor)
            skalar_produkt = vektor_pq.dot(normalvektor)

            zaehler = abs(skalar_produkt)
            nenner = normalvektor.mod()
            abstand = zaehler/nenner

            return abstand
        else:
            return None

    # ======================================================================
    # Winkelberechnungen
    # ======================================================================
    
        
    def winkel_zwei_geraden(self, g2, deg=None):
        """
        Berechnet den Winkel zwischen dieser Geraden und einer anderen Geraden.

        Der Winkel wird aus dem Skalarprodukt der Richtungsvektoren berechnet.

        Parameters
        ----------
        g2 : Gerade
            Die zweite Gerade.
        deg : bool, optional
            Wenn True, wird der Winkel in Grad zurückgegeben.
            Wenn False oder None, wird der Winkel in Radiant zurückgegeben.
            Standard ist None (Radiant).

        Returns
        -------
        float
            Der Winkel zwischen den Geraden in Radiant oder Grad.
        """
        zaehler = abs(self.richtungsvektor.dot(g2.richtungsvektor))
        nenner = self.richtungsvektor.mod() * g2.richtungsvektor.mod()
        result_in_radians = math.acos(zaehler/nenner)
        if deg:
            return math.degrees(result_in_radians)
        return result_in_radians

    # ======================================================================
    # Transformationen
    # ======================================================================

    def skalieren(self, faktor):
        return Gerade(self.stutzvektor.skalieren(faktor), self.richtungsvektor.skalieren(faktor))

    def drehen(self, winkel, achse):
        return Gerade(self.stutzvektor.drehen(winkel, achse), self.richtungsvektor.drehen(winkel, achse))

    def verschieben(self, v):
        return Gerade(self.stutzvektor.verschieben(v), self.richtungsvektor)

    def spiegeln_an_punkt(self, P):
        return Gerade(self.stutzvektor.spiegeln_an_punkt(P), self.richtungsvektor.spiegeln_an_punkt(P))

    def spiegeln_an_gerade(self, g):
        return Gerade(self.stutzvektor.spiegeln_an_gerade(g), self.richtungsvektor.spiegeln_an_gerade(g))

    def spiegeln_an_ebene(self, E):
        return Gerade(self.stutzvektor.spiegeln_an_ebene(E), self.richtungsvektor.spiegeln_an_ebene(E))
    
    def __repr__(self):
        """
        Gibt eine lesbare String-Repräsentation der Geraden zurück.

        Returns
        -------
        str
            Eine String-Repräsentation der Geraden.
        """
        return f"Gerade(stutz={self.stutzvektor}, richtung={self.richtungsvektor})"
