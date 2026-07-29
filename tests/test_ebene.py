import random
from analytische_geometrie.geometrie.ebene import Ebene
from analytische_geometrie.geometrie.gerade import Gerade
from analytische_geometrie.geometrie.punkt import Punkt
from analytische_geometrie.geometrie.vektor import Vektor
from analytische_geometrie.utils.linal_utils import close

class TestEbene:

    def test_creation(self):
        """Testet die Erstellung einer Ebene"""
        E = Ebene([0, 0, 0], [1, 1, 1])
        assert E.punkt == Vektor(0, 0, 0)
        assert E.norm_vektor == Vektor(1, 1, 1)
        
    def test_from_parameterform(self):
        """Testet die Erstellung aus Parameterform"""
        E = Ebene.from_parameterform([1, 0, 0], [0, 1, 0], [0, 0, 1])
        assert E.norm_vektor == Vektor(1, 0, 0)
        
    def test_enthaelt_punkt_true(self):
        """Testet ob Punkt in Ebene liegt (wahr)"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([0, 1, 2])
        assert E.enthaelt_punkt(p) is True
        
    def test_enthaelt_punkt_false(self):
        """Testet ob Punkt in Ebene liegt (falsch)"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([1, 0, 0])
        assert E.enthaelt_punkt(p) is False
        
    def test_lage_gerade_schneidend(self):
        """Testet schneidende Gerade-Ebene"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        g = Gerade([-1, 0, 0], [1, 0, 0])
        assert E.lage_gerade(g) == "schneidend"
        
    def test_lage_gerade_parallel(self):
        """Testet parallele Gerade-Ebene"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        g = Gerade([1, 0, 0], [0, 1, 0])
        assert E.lage_gerade(g) == "parallel"
        
    def test_lage_gerade_identisch(self):
        """Testet in Ebene liegende Gerade"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        g = Gerade([0, 1, 0], [0, 1, 0])
        assert E.lage_gerade(g) == "identisch"
        
    def test_schnittpunkt_gerade(self):
        """Testet den Schnittpunkt Gerade-Ebene"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        g = Gerade([-1, 1, 1], [1, 0, 0])
        schnitt = E.schnittpunkt_gerade(g)
        assert schnitt == Vektor(0, 1, 1)

    def test_lage_ebene_identisch(self):
        """Testet identische Ebenen"""
        E1 = Ebene([0, 0, 0], [1, 0, 0])
        E2 = Ebene([0, 0, 0], [2, 0, 0])
        assert E1.lage_ebene(E2) == "identisch"
        
    def test_lage_ebene_parallel(self):
        """Testet parallele Ebenen"""
        E1 = Ebene([0, 0, 0], [1, 0, 0])
        E2 = Ebene([2, 0, 0], [1, 0, 0])
        assert E1.lage_ebene(E2) == "parallel"
        
    def test_lage_ebene_schneidend(self):
        """Testet sich schneidende Ebenen"""
        E1 = Ebene([0, 0, 0], [1, 0, 0])
        E2 = Ebene([0, 0, 0], [0, 1, 0])
        assert E1.lage_ebene(E2) == "schneidend"
        
    def test_schnittwinkel_ebene(self):
        """Testet den Winkel zwischen Ebenen"""
        E1 = Ebene([0, 0, 0], [1, 0, 0])
        E2 = Ebene([0, 0, 0], [0, 1, 0])
        assert close(E1.schnittwinkel_ebene(E2, deg=True), 90.0)
        
    def test_abstand_punkt(self):
        """Testet den Abstand Punkt-Ebene"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([3, 4, 0])
        assert E.abstand_punkt(p) == 3.0
        
    def test_abstand_gerade_parallel(self):
        """Testet den Abstand Gerade-Ebene (parallel)"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        g = Gerade([1, 1, 0], [0, 1, 0])
        assert E.abstand_gerade(g) == 1.0
        
    def test_abstand_ebene_parallel(self):
        """Testet den Abstand Ebene-Ebene (parallel)"""
        E1 = Ebene([0, 0, 0], [1, 0, 0])
        E2 = Ebene([5, 0, 0], [2, 0, 0])
        assert E1.abstand_ebene(E2) == 5.0
        
    def test_spurpunkte(self):
        """Testet die Spurpunkte einer Ebene"""
        E = Ebene([0, 0, 0], [1, 1, 1])
        spur = E.spurpunkte()
        for s in spur:
            if s[0] is not None:
                assert close(s[0], 0)

    def test_huge_numbers(self):
        E = Ebene(
            [1e150, 1e150, 1e150],
            [1e150, -1e150, 1e150]
        )

        p = Vektor(1e150, 1e150, 1e150)

        assert E.enthaelt_punkt(p)

    def test_random_intersections(self):
        random.seed(42)

        for _ in range(10000):

            p = Vektor(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            n = Vektor(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            E = Ebene(p, n)

            q = p + Vektor(
                random.gauss(0, 1),
                random.gauss(0, 1),
                random.gauss(0, 1)
            )

            q = q - ((q - p).dot(n) / n.dot(n)) * n

            assert E.enthaelt_punkt(q)

class TestTransformEbene:

    def test_skalieren(self):
        """Testet die Skalierung einer Ebene"""
        E = Ebene(
            Vektor([1, 2, 3]),
            Vektor([0, 0, 1])
        )

        E2 = E.skalieren(2)

        assert close(E2.punkt, Vektor([2, 4, 6]))
        assert close(E2.norm_vektor, Vektor([0, 0, 2]))

    def test_verschieben(self):
        """Testet die Verschiebung einer Ebene"""
        E = Ebene(
            Vektor([1, 2, 3]),
            Vektor([0, 0, 1])
        )

        E2 = E.verschieben(Vektor([1, 1, 1]))

        assert close(E2.punkt, Vektor([2, 3, 4]))
        assert close(E2.norm_vektor, Vektor([0, 0, 1]))

    def test_drehen_x(self):
        """Testet die Rotation einer Ebene um die x-Achse"""
        E = Ebene(
            Vektor([0, 1, 0]),
            Vektor([0, 1, 0])
        )

        E2 = E.drehen(90, "x")

        assert close(E2.punkt, Vektor([0, 0, 1]))
        assert close(E2.norm_vektor, Vektor([0, 0, 1]))

    def test_drehen_y(self):
        """Testet die Rotation einer Ebene um die y-Achse"""
        E = Ebene(
            Vektor([0, 0, 1]),
            Vektor([0, 0, 1])
        )

        E2 = E.drehen(90, "y")

        assert close(E2.punkt, Vektor([1, 0, 0]))
        assert close(E2.norm_vektor, Vektor([1, 0, 0]))

    def test_drehen_z(self):
        """Testet die Rotation einer Ebene um die z-Achse"""
        E = Ebene(
            Vektor([1, 0, 0]),
            Vektor([1, 0, 0])
        )

        E2 = E.drehen(90, "z")

        assert close(E2.punkt, Vektor([0, 1, 0]))
        assert close(E2.norm_vektor, Vektor([0, 1, 0]))

    def test_spiegeln_an_punkt(self):
        """Testet die Spiegelung einer Ebene an einem Punkt"""
        E = Ebene(
            Vektor([1, 2, 3]),
            Vektor([0, 0, 1])
        )

        E2 = E.spiegeln_an_punkt(Vektor([0, 0, 0]))

        assert close(E2.punkt, Vektor([-1, -2, -3]))
        assert close(E2.norm_vektor, Vektor([0, 0, -1]))

    def test_spiegeln_an_gerade(self):
        """Testet die Spiegelung einer Ebene an einer Geraden"""
        g = Gerade(
            Vektor([0, 0, 0]),
            Vektor([1, 0, 0])
        )

        E = Ebene(
            Vektor([0, 1, 0]),
            Vektor([0, 1, 0])
        )

        E2 = E.spiegeln_an_gerade(g)

        assert close(E2.punkt, Vektor([0, -1, 0]))
        assert close(E2.norm_vektor, Vektor([0, -1, 0]))

    def test_spiegeln_an_ebene(self):
        """Testet die Spiegelung einer Ebene an einer Ebene"""
        spiegel = Ebene(
            Vektor([0, 0, 0]),
            Vektor([0, 0, 1])
        )

        E = Ebene(
            Vektor([1, 2, 3]),
            Vektor([0, 1, 1])
        )

        E2 = E.spiegeln_an_ebene(spiegel)

        assert close(E2.punkt, Vektor([1, 2, -3]))
        assert close(E2.norm_vektor, Vektor([0, 1, -1]))