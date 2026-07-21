from ..utils.vector_utils import Vector
class Punkt:
    """
    Repräsentiert einen Punkt im dreidimensionalen Raum.

    Ein Punkt wird durch seine Koordinaten (x1, x2, x3) im kartesischen
    Koordinatensystem definiert. Alle Operationen werden mit Hilfe von
    NumPy-Arrays effizient berechnet.

    Parameters
    ----------
    punkt : array_like
        Ein iterierbares Objekt (Liste, Tupel oder NumPy-Array) mit drei
        Koordinatenwerten für den Punkt.

    Attributes
    ----------
    punkt : numpy.ndarray
        Die Koordinaten des Punkts als 3D-Array.
    """

    def __init__(self, punkt):
        """
        Initialisiert einen neuen Punkt.

        Parameters
        ----------
        punkt : array_like
            Ein iterierbares Objekt mit drei Koordinatenwerten (x1, x2, x3).

        Raises
        ------
        ValueError
            Wenn die Eingabe nicht genau drei Koordinaten enthält.
        """
        if isinstance(punkt, Punkt):
            self.punkt = punkt.punkt
        else:
            self.punkt = Vector(punkt)
    
    def get_punkt(self):
        """
        Gibt die Koordinaten des Punkts als NumPy-Array zurück.

        Returns
        -------
        numpy.ndarray
            Ein Array der Form (3,) mit den Koordinaten (x1, x2, x3).
        """
        return self.punkt
    
    def get_x1(self):
        """
        Gibt die x1-Koordinate des Punkts zurück.

        Returns
        -------
        float
            Der Wert der x1-Koordinate.
        """
        return self.punkt[0]
    
    def get_x2(self):
        """
        Gibt die x2-Koordinate des Punkts zurück.

        Returns
        -------
        float
            Der Wert der x2-Koordinate.
        """
        return self.punkt[1]
    
    def get_x3(self):
        """
        Gibt die x3-Koordinate des Punkts zurück.

        Returns
        -------
        float
            Der Wert der x3-Koordinate.
        """
        return self.punkt[2]
    
    def abstand_zu_punkt(self, punkt2):
        """
        Berechnet den euklidischen Abstand zu einem anderen Punkt.

        Der Abstand wird nach der Formel
        d = sqrt((x1-x1')² + (x2-x2')² + (x3-x3')²) berechnet.

        Parameters
        ----------
        punkt2 : array_like
            Die Koordinaten des zweiten Punkts als Liste, Tupel oder Array.

        Returns
        -------
        float
            Der euklidische Abstand zwischen den beiden Punkten.
        """
        p2 = punkt2.punkt if isinstance(punkt2, Punkt) else Vector(punkt2)
        a = self.punkt - p2

        return a.mod()
    
    def punkt_punkt(self, punkt2):
        """
        Berechnet den Vektor von diesem Punkt zu einem anderen Punkt.

        Der resultierende Vektor zeigt vom aktuellen Punkt zum angegebenen Punkt.

        Parameters
        ----------
        punkt2 : array_like
            Die Koordinaten des Zielpunkts als Liste, Tupel oder Array.

        Returns
        -------
        Vector
            Der Verbindungsvektor (punkt2 - self.punkt) als Vector-Objekt.
        """
        p2 = punkt2.punkt if isinstance(punkt2, Punkt) else Vector(punkt2)
        return p2 - self.punkt