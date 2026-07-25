from .vektor import Vektor

class Punkt(Vektor):
    """
    Repräsentiert einen Punkt im dreidimensionalen Raum.

    Ein Punkt beschreibt eine Position im kartesischen Koordinatensystem
    durch seine drei Koordinaten (x1, x2, x3). Die Klasse erweitert
    :class:`Vektor` um punktbezogene Operationen, beispielsweise die
    Berechnung des Abstands zwischen zwei Punkten oder des Verbindungsvektors
    zwischen ihnen.

    Parameters
    ----------
    punkt : array_like
        Ein iterierbares Objekt mit drei Koordinatenwerten (x1, x2, x3).

    Notes
    -----
    Ein Punkt ist mathematisch eng mit einem Vektor verwandt, besitzt jedoch
    eine andere geometrische Bedeutung. Während ein Vektor eine Richtung oder
    Verschiebung beschreibt, repräsentiert ein Punkt eine feste Position im
    Raum.
    """

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
        p2 = punkt2.punkt if isinstance(punkt2, Punkt) else Vektor(punkt2)
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
            Der Verbindungsvektor (punkt2 - self.punkt) als Vektor-Objekt.
        """
        p2 = punkt2.punkt if isinstance(punkt2, Punkt) else Vektor(punkt2)
        return p2 - self.punkt