from analytische_geometrie.geometrie import Vektor
from analytische_geometrie.geometrie import Gerade
from analytische_geometrie.geometrie import Punkt
from analytische_geometrie.geometrie import Ebene
from analytische_geometrie.geometrie import Wuerfel
from analytische_geometrie.utils.linal_utils import close

class TestWuerfelTransformationen:
    """
    Testet Transformationen eines Würfels mit den Eckpunkten
    P_min = (0,0,0) und P_max = (2,2,2).
    """

    def setup_method(self):
        """Erstellt einen Würfel mit Kantenlänge 2"""
        self.w = Wuerfel(
            [0, 0, 0],
            [2, 2, 2]
        )

    def test_skalieren(self):
        """Überprüft, ob der Würfel korrekt skaliert wird"""
        skaliert = self.w.skalieren(2)

        assert close(skaliert.p_min, [0, 0, 0])
        assert close(skaliert.p_max, [4, 4, 4])


    def test_drehen_um_z_achse(self):
        """Überprüft eine Drehung um 90 Grad um die z-Achse"""
        gedreht = self.w.drehen(90, "z")

        assert close(gedreht.p_min, [0, 0, 0])
        assert close(gedreht.p_max, [-2, 2, 2])


    def test_verschieben(self):
        """Überprüft eine Verschiebung des Würfels"""
        v = Vektor(1, 2, 3)

        verschoben = self.w.verschieben(v)

        assert close(verschoben.p_min, [1, 2, 3])
        assert close(verschoben.p_max, [3, 4, 5])


    def test_spiegeln_an_punkt(self):
        """Überprüft die Punktspiegelung am Ursprung"""
        P = Punkt([0, 0, 0])

        gespiegelt = self.w.spiegeln_an_punkt(P)

        assert close(gespiegelt.p_min, [0, 0, 0])
        assert close(gespiegelt.p_max, [-2, -2, -2])


    def test_spiegeln_an_gerade(self):
        """Überprüft die Spiegelung an der x-Achse"""
        g = Gerade(
            Punkt([0, 0, 0]),
            Vektor(1, 0, 0)
        )

        gespiegelt = self.w.spiegeln_an_gerade(g)

        assert close(gespiegelt.p_min, [0, 0, 0])
        assert close(gespiegelt.p_max, [2, -2, -2])


    def test_spiegeln_an_ebene(self):
        """Überprüft die Spiegelung an der xy-Ebene"""
        E = Ebene.from_parameterform(
            Punkt([0, 0, 0]),
            Vektor(1, 0, 0),
            Vektor(0, 1, 0)
        )

        gespiegelt = self.w.spiegeln_an_ebene(E)

        assert close(gespiegelt.p_min, [0, 0, 0])
        assert close(gespiegelt.p_max, [2, 2, -2])