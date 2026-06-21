import numpy as np
from .punkt import Punkt
from .gerade import Gerade
import math

class Ebene:
    """
    Repräsentiert eine Ebene im dreidimensionalen Raum.

    Eine Ebene wird durch einen Punkt und einen Normalenvektor definiert.
    Die Normalengleichung lautet: (x - punkt) · norm_vektor = 0.

    Parameters
    ----------
    punkt : array_like
        Ein Punkt auf der Ebene (Stützvektor).
    norm_vektor : array_like
        Der Normalenvektor der Ebene (darf nicht der Nullvektor sein).

    Attributes
    ----------
    punkt : numpy.ndarray
        Ein Punkt auf der Ebene.
    norm_vektor : numpy.ndarray
        Der Normalenvektor der Ebene.
    """

    def __init__(self, punkt, norm_vektor):
        """
        Initialisiert eine neue Ebene mit Punkt und Normalenvektor.

        Parameters
        ----------
        punkt : array_like
            Ein Punkt auf der Ebene.
        norm_vektor : array_like
            Der Normalenvektor der Ebene (darf nicht der Nullvektor sein).

        Raises
        ------
        ValueError
            Wenn die Vektoren nicht die Dimension 3 haben oder der
            Normalenvektor der Nullvektor ist.
        """
        self.punkt = np.array(punkt)
        self.norm_vektor = np.array(norm_vektor)
    
    @classmethod
    def from_parameterform(cls, punkt, v1, v2):
        """
        Erstellt eine Ebene aus der Parameterform.

        Die Ebene wird durch einen Punkt und zwei Richtungsvektoren definiert.
        Der Normalenvektor ergibt sich aus dem Kreuzprodukt v1 × v2.

        Parameters
        ----------
        punkt : array_like
            Ein Punkt auf der Ebene.
        v1 : array_like
            Erster Richtungsvektor der Ebene.
        v2 : array_like
            Zweiter Richtungsvektor der Ebene.

        Returns
        -------
        Ebene
            Die durch Punkt und Richtungsvektoren definierte Ebene.

        Raises
        ------
        ValueError
            Wenn die Vektoren nicht die Dimension 3 haben oder die
            Richtungsvektoren linear abhängig sind.
        """
        norm_vektor = np.cross(v1, v2)
        return cls(punkt, norm_vektor)
    
    def ebene(self, x_vektor):
        """
        Prüft, ob ein gegebener Vektor die Ebenengleichung erfüllt.

        Ein Vektor x liegt in der Ebene, wenn (x - punkt) · norm_vektor = 0.

        Parameters
        ----------
        x_vektor : array_like
            Der zu prüfende Vektor (Punkt).

        Returns
        -------
        bool
            True, wenn der Vektor in der Ebene liegt, sonst False.
        """
        return np.isclose(np.dot(x_vektor, self.norm_vektor), 
                         np.dot(self.punkt, self.norm_vektor))
    
    def enthaelt_punkt(self, p1):
        """
        Prüft, ob ein gegebener Punkt in der Ebene liegt.

        Parameters
        ----------
        p1 : array_like
            Der zu prüfende Punkt.

        Returns
        -------
        bool
            True, wenn der Punkt in der Ebene liegt, sonst False.
        """
        if np.isclose(np.dot(p1, self.norm_vektor), 
                     np.dot(self.punkt, self.norm_vektor)):
            return True
        else:
            return False

    def lage_gerade(self, gerade):
        """
        Bestimmt die Lagebeziehung einer Geraden zu dieser Ebene.

        Die möglichen Lagebeziehungen sind:
        - "identisch": Die Gerade liegt vollständig in der Ebene.
        - "parallel": Die Gerade ist parallel zur Ebene, aber nicht in ihr.
        - "schneidend": Die Gerade schneidet die Ebene in einem Punkt.

        Parameters
        ----------
        gerade : Gerade
            Die zu prüfende Gerade.

        Returns
        -------
        str
            Die Lagebeziehung als String: "identisch", "parallel" oder "schneidend".
        """
        if np.isclose(np.dot(gerade.richtungsvektor, self.norm_vektor), 0):
            if self.enthaelt_punkt(gerade.gerade(0)):
                return "identisch"
            else:
                return "parallel"
        else:
            return "schneidend"
 
    def lage_ebene(self, E2):
        """
        Bestimmt die Lagebeziehung einer anderen Ebene zu dieser Ebene.

        Die möglichen Lagebeziehungen sind:
        - "identisch": Die Ebenen sind identisch.
        - "parallel": Die Ebenen sind parallel, aber nicht identisch.
        - "schneidend": Die Ebenen schneiden sich in einer Geraden.

        Parameters
        ----------
        E2 : Ebene
            Die zweite Ebene.

        Returns
        -------
        str
            Die Lagebeziehung als String: "identisch", "parallel" oder "schneidend".
        """
        if np.allclose(np.cross(self.norm_vektor, E2.norm_vektor), 0):
            if self.enthaelt_punkt(E2.punkt):
                return "identisch"
            else:
                return "parallel"
        else:
            return "schneidend"

    def schnittpunkt_gerade(self, g: Gerade):
        """
        Berechnet den Schnittpunkt einer Geraden mit dieser Ebene.

        Der Schnittpunkt wird nur für sich schneidende Geraden berechnet.

        Parameters
        ----------
        g : Gerade
            Die Gerade, deren Schnittpunkt mit der Ebene berechnet werden soll.

        Returns
        -------
        numpy.ndarray or None
            Der Schnittpunkt, wenn die Gerade die Ebene schneidet,
            sonst None.
        """
        if self.lage_gerade(g) == "schneidend":
            zaehler = np.dot(self.norm_vektor, self.punkt - g.stutzvektor)
            nenner = np.dot(self.norm_vektor, g.richtungsvektor)
            r = zaehler / nenner
            return g.gerade(r)
        else:
            return None
    
    def schnittgerade_ebene(self, E2):
        """
        Berechnet die Schnittgerade dieser Ebene mit einer anderen Ebene.

        Die Schnittgerade wird nur für sich schneidende Ebenen berechnet.

        Parameters
        ----------
        E2 : Ebene
            Die zweite Ebene.

        Returns
        -------
        Gerade or None
            Die Schnittgerade, wenn die Ebenen sich schneiden,
            sonst None.
        """
        if self.lage_ebene(E2) == "schneidend":
            richt_vektor = np.cross(self.norm_vektor, E2.norm_vektor)

            d1 = np.dot(self.norm_vektor, self.punkt)
            d2 = np.dot(E2.norm_vektor, E2.punkt)
            d = np.array([d1, d2])

            A = np.array([self.norm_vektor, E2.norm_vektor])

            stutz_vektor, _, _, _ = np.linalg.lstsq(A, d, rcond=None)
            schnitt_gerade = Gerade(stutz_vektor, richt_vektor)

            return schnitt_gerade
        else:
            return None

    def schnittwinkel_gerade(self, g: Gerade, deg=None):
        """
        Berechnet den Schnittwinkel zwischen einer Geraden und dieser Ebene.

        Der Winkel wird aus dem Sinus des Winkels zwischen dem Normalenvektor
        der Ebene und dem Richtungsvektor der Geraden berechnet.

        Parameters
        ----------
        g : Gerade
            Die Gerade.
        deg : bool, optional
            Wenn True, wird der Winkel in Grad zurückgegeben.
            Wenn False oder None, wird der Winkel in Radiant zurückgegeben.
            Standard ist None (Radiant).

        Returns
        -------
        float
            Der Schnittwinkel in Radiant oder Grad.
        """
        zaehler = abs(np.dot(self.norm_vektor, g.richtungsvektor))
        nenner = np.linalg.norm(self.norm_vektor) * np.linalg.norm(g.richtungsvektor)
        los_rad = math.asin(zaehler / nenner)

        return math.degrees(los_rad) if deg else los_rad
    
    def schnittwinkel_ebene(self, E2, deg=None):
        """
        Berechnet den Schnittwinkel zwischen dieser Ebene und einer anderen Ebene.

        Der Winkel wird aus dem Skalarprodukt der Normalenvektoren berechnet.

        Parameters
        ----------
        E2 : Ebene
            Die zweite Ebene.
        deg : bool, optional
            Wenn True, wird der Winkel in Grad zurückgegeben.
            Wenn False oder None, wird der Winkel in Radiant zurückgegeben.
            Standard ist None (Radiant).

        Returns
        -------
        float
            Der Schnittwinkel in Radiant oder Grad.
        """
        zaehler = abs(np.dot(self.norm_vektor, E2.norm_vektor))
        nenner = np.linalg.norm(self.norm_vektor) * np.linalg.norm(E2.norm_vektor)
        los_rad = math.acos(zaehler / nenner)

        return math.degrees(los_rad) if deg else los_rad
    
    def spurpunkte(self):
        """
        Berechnet die Spurpunkte der Ebene.

        Spurpunkte sind die Schnittpunkte der Ebene mit den Koordinatenachsen:
        - S1: Schnitt mit der x1-Achse (x2 = 0, x3 = 0)
        - S2: Schnitt mit der x2-Achse (x1 = 0, x3 = 0)
        - S3: Schnitt mit der x3-Achse (x1 = 0, x2 = 0)

        Wenn die Ebene parallel zu einer Achse ist, wird an dieser Stelle
        None zurückgegeben.

        Returns
        -------
        list
            Eine Liste mit drei Einträgen [S1, S2, S3], wobei jeder Eintrag
            ein Punkt (Liste) oder None ist.
        """
        S = []
        for i in range(3):
            d = np.dot(self.punkt, self.norm_vektor)
            x = [0] * 3
            if not np.isclose(self.norm_vektor[i], 0):
                x[i] = d / self.norm_vektor[i]
            else:
                x[i] = None

            S.append(x)
        return S

    def abstand_punkt(self, punkt: Punkt):
        """
        Berechnet den Abstand eines Punkts zu dieser Ebene.

        Parameters
        ----------
        punkt : Punkt
            Der Punkt, dessen Abstand zur Ebene berechnet werden soll.

        Returns
        -------
        float
            Der Abstand des Punkts zur Ebene. Wenn der Punkt in der Ebene
            liegt, wird 0 zurückgegeben.
        """
        if not self.enthaelt_punkt(punkt):
            zaehler = abs(np.dot(punkt - self.punkt, self.norm_vektor))
            nenner = np.linalg.norm(self.norm_vektor)
            d = zaehler / nenner
        
            return d
        else:
            return 0
    
    def abstand_gerade(self, g: Gerade):
        """
        Berechnet den Abstand einer Geraden zu dieser Ebene.

        Der Abstand wird nur für zur Ebene parallele Geraden berechnet.

        Parameters
        ----------
        g : Gerade
            Die Gerade, deren Abstand zur Ebene berechnet werden soll.

        Returns
        -------
        float or None
            Der Abstand der Geraden zur Ebene, wenn sie parallel ist,
            sonst None.
        """
        if self.lage_gerade(g) == "parallel":
            q = g.stutzvektor
            return self.abstand_punkt(q)
        else:
            return None

    def abstand_ebene(self, E2):
        """
        Berechnet den Abstand dieser Ebene zu einer anderen Ebene.

        Der Abstand wird nur für parallele Ebenen berechnet.

        Parameters
        ----------
        E2 : Ebene
            Die zweite Ebene.

        Returns
        -------
        float or None
            Der Abstand der Ebenen, wenn sie parallel sind,
            sonst None.
        """
        if self.lage_ebene(E2) == "parallel":
            return self.abstand_punkt(E2.punkt)
        else:
            return None

    def __repr__(self):
        """
        Gibt eine lesbare String-Repräsentation der Ebene zurück.

        Returns
        -------
        str
            Eine String-Repräsentation der Ebene.
        """
        return f"Ebene(punkt={self.punkt}, norm={self.norm_vektor})"