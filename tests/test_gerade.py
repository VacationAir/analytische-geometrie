from analytische_geometrie.geometrie.gerade import Gerade
from analytische_geometrie.geometrie.punkt import Punkt
from analytische_geometrie.geometrie.vektor import Vektor
from analytische_geometrie.geometrie.ebene import Ebene
from analytische_geometrie.utils.linal_utils import close

class TestGerade:

    def test_creation_from_punkte(self):
        """Testet die Erstellung einer Gerade aus zwei Punkten"""
        g = Gerade.from_punkte([0, 0, 0], [1, 1, 1])
        assert close(g.stutzvektor, [0, 0, 0])
        assert close(g.richtungsvektor, [1, 1, 1])
        
    def test_gerade(self):
        """Testet die Punktberechnung auf der Gerade"""
        g = Gerade([0, 0, 0], [1, 1, 1])
        assert close(g.gerade(2), [2, 2, 2])
        
    def test_enthaelt_punkt_true(self):
        """Testet ob ein Punkt auf der Gerade liegt (wahr)"""
        g = Gerade.from_punkte([0, 0, 0], [2, 2, 2])
        p = Punkt([1, 1, 1])
        assert g.enthaelt_punkt(p) is True
        
    def test_enthaelt_punkt_false(self):
        """Testet ob ein Punkt auf der Gerade liegt (falsch)"""
        g = Gerade.from_punkte([0, 0, 0], [2, 2, 2])
        p = Punkt([1, 2, 3])
        assert g.enthaelt_punkt(p) is False
        
    def test_abstand_zu_punkt(self):
        """Testet den Abstand zwischen Punkt und Gerade"""
        g = Gerade([0, 0, 0], [1, 0, 0])
        p = Punkt([1, 1, 0])
        assert g.abstand_zu_punkt(p) == 1.0
        
    def test_winkel_zwei_geraden(self):
        """Testet den Winkel zwischen zwei Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        assert close(g1.winkel_zwei_geraden(g2, deg=True), 90.0)
        
    def test_lage_gerade_gerade_identisch(self):
        """Testet identische Geraden"""
        g1 = Gerade([0, 0, 0], [1, 1, 1])
        g2 = Gerade([1, 1, 1], [2, 2, 2])
        assert g1.lage_gerade(g2) == "identisch"
        
    def test_lage_gerade_gerade_parallel(self):
        """Testet parallele Geraden"""
        g1 = Gerade([0, 0, 0], [1, 1, 1])
        g2 = Gerade([1, 0, 0], [2, 2, 2])
        assert g1.lage_gerade(g2) == "parallel"
        
    def test_lage_gerade_gerade_schneidend(self):
        """Testet sich schneidende Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        assert g1.lage_gerade(g2) == "schneidend"
        
    def test_lage_gerade_gerade_windschief(self):
        """Testet windschiefe Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 1, 0], [0, 1, 1])
        assert g1.lage_gerade(g2) == "windschief"
        
    def test_schnitt_mit_gerade(self):
        """Testet den Schnittpunkt zweier Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        schnitt = g1.schnitt_mit_gerade(g2)
        assert close(schnitt, [0, 0, 0])
        
    def test_spurpunkte_gerade(self):
        """Testet die Spurpunkte einer Gerade"""
        g = Gerade.from_punkte([1, 2, 3], [2, 3, 4])
        spur = g.spurpunkte_gerade()
        assert len(spur) == 3


class TestTransformGerade:

    def test_skalieren(self):
        """Testet die Skalierung einer Geraden"""
        g = Gerade(
            Vektor([1, 2, 3]),
            Vektor([4, 5, 6])
        )

        g2 = g.skalieren(2)

        assert close(g2.stutzvektor, Vektor([2, 4, 6]))
        assert close(g2.richtungsvektor, Vektor([8, 10, 12]))

    def test_verschieben(self):
        """Testet die Verschiebung einer Geraden"""
        g = Gerade(
            Vektor([1, 2, 3]),
            Vektor([4, 5, 6])
        )

        g2 = g.verschieben(Vektor([1, 1, 1]))

        assert close(g2.stutzvektor, Vektor([2, 3, 4]))
        assert close(g2.richtungsvektor, Vektor([4, 5, 6]))

    def test_drehen_x(self):
        """Testet die Rotation einer Geraden um die x-Achse"""
        g = Gerade(
            Vektor([0, 1, 0]),
            Vektor([0, 1, 0])
        )

        g2 = g.drehen(90, "x")

        assert close(g2.stutzvektor, Vektor([0, 0, 1]))
        assert close(g2.richtungsvektor, Vektor([0, 0, 1]))

    def test_drehen_y(self):
        """Testet die Rotation einer Geraden um die y-Achse"""
        g = Gerade(
            Vektor([0, 0, 1]),
            Vektor([0, 0, 1])
        )

        g2 = g.drehen(90, "y")

        assert close(g2.stutzvektor, Vektor([1, 0, 0]))
        assert close(g2.richtungsvektor, Vektor([1, 0, 0]))

    def test_drehen_z(self):
        """Testet die Rotation einer Geraden um die z-Achse"""
        g = Gerade(
            Vektor([1, 0, 0]),
            Vektor([1, 0, 0])
        )

        g2 = g.drehen(90, "z")

        assert close(g2.stutzvektor, Vektor([0, 1, 0]))
        assert close(g2.richtungsvektor, Vektor([0, 1, 0]))

    def test_spiegeln_an_punkt(self):
        """Testet die Spiegelung einer Geraden an einem Punkt"""
        g = Gerade(
            Vektor([1, 2, 3]),
            Vektor([1, 0, 0])
        )

        g2 = g.spiegeln_an_punkt(Vektor([0, 0, 0]))

        assert close(g2.stutzvektor, Vektor([-1, -2, -3]))
        assert close(g2.richtungsvektor, Vektor([-1, 0, 0]))

    def test_spiegeln_an_gerade(self):
        """Testet die Spiegelung einer Geraden an einer Geraden"""
        achse = Gerade(
            Vektor([0, 0, 0]),
            Vektor([1, 0, 0])
        )

        g = Gerade(
            Vektor([0, 1, 0]),
            Vektor([1, 0, 0])
        )

        g2 = g.spiegeln_an_gerade(achse)

        assert close(g2.stutzvektor, Vektor([0, -1, 0]))
        assert close(g2.richtungsvektor, Vektor([1, 0, 0]))

    def test_spiegeln_an_ebene(self):
        """Testet die Spiegelung einer Geraden an einer Ebene"""
        E = Ebene(
            Vektor([0, 0, 0]),
            Vektor([0, 0, 1])
        )

        g = Gerade(
            Vektor([1, 2, 3]),
            Vektor([1, 0, 0])
        )

        g2 = g.spiegeln_an_ebene(E)

        assert close(g2.stutzvektor, Vektor([1, 2, -3]))
        assert close(g2.richtungsvektor, Vektor([1, 0, 0]))