from analytische_geometrie.geometrie.vektor import Vektor
from analytische_geometrie.geometrie.gerade import Gerade
from analytische_geometrie.geometrie.ebene import Ebene
from analytische_geometrie.utils.linal_utils import close


class TestVektor:

    def test_skalieren(self):
        """Testet die Skalierung eines Vektors"""
        v = Vektor([1, 2, 3])

        assert close(v.skalieren(2), [2, 4, 6])
        assert close(v.skalieren(-1), [-1, -2, -3])
        assert close(v.skalieren(0), [0, 0, 0])

    def test_verschieben(self):
        """Testet die Verschiebung eines Vektors"""
        v = Vektor([1, 2, 3])

        assert close(v.verschieben(Vektor([4, 5, 6])), Vektor([5, 7, 9]))
        assert close(v.verschieben(Vektor([-1, -2, -3])), Vektor([0, 0, 0]))

    def test_drehen_x(self):
        """Testet die Rotation um die x-Achse"""
        v = Vektor([0, 1, 0])

        assert close(v.drehen(90, "x"), [0, 0, 1])

    def test_drehen_y(self):
        """Testet die Rotation um die y-Achse"""
        v = Vektor([0, 0, 1])

        assert close(v.drehen(90, "y"), [1, 0, 0])

    def test_drehen_z(self):
        """Testet die Rotation um die z-Achse"""
        v = Vektor([1, 0, 0])

        assert close(v.drehen(90, "z"), [0, 1, 0])

    def test_spiegeln_an_punkt(self):
        """Testet die Spiegelung eines Vektors an einem Punkt"""
        v = Vektor([1, 2, 3])

        assert close(
            v.spiegeln_an_punkt(Vektor([0, 0, 0])),
            [-1, -2, -3]
        )

        assert close(
            v.spiegeln_an_punkt(Vektor([1, 1, 1])),
            [1, 0, -1]
        )

    def test_spiegeln_an_gerade(self):
        """Testet die Spiegelung eines Vektors an einer Geraden"""
        g = Gerade([0, 0, 0], [1, 0, 0])

        assert close(
            Vektor([1, 2, 0]).spiegeln_an_gerade(g),
            [1, -2, 0]
        )

        assert close(
            Vektor([3, 0, 0]).spiegeln_an_gerade(g),
            [3, 0, 0]
        )

    def test_spiegeln_an_ebene(self):
        """Testet die Spiegelung eines Vektors an einer Ebene"""
        E = Ebene([0, 0, 0], [0, 0, 1])

        assert close(
            Vektor([1, 2, 3]).spiegeln_an_ebene(E),
            [1, 2, -3]
        )

        assert close(
            Vektor([4, 5, 0]).spiegeln_an_ebene(E),
            [4, 5, 0]
        )

    def test_rotation_preserves_length(self):
        """Eine Rotation erhält den Betrag eines Vektors"""
        v = Vektor([1, 2, 3])

        assert close(
            v.mod(),
            v.drehen(123, "x").mod()
        )

    def test_double_reflection_point(self):
        """Zweimalige Punktspiegelung ergibt den Ausgangsvektor"""
        v = Vektor([1, 2, 3])
        P = Vektor([5, 1, -2])

        assert close(
            v,
            v.spiegeln_an_punkt(P).spiegeln_an_punkt(P)
        )