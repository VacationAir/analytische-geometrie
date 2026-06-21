import pytest
import numpy as np
from analytische_geometrie.gerade import Gerade
from analytische_geometrie.punkt import Punkt

class TestGerade:

    def test_creation_from_punkte(self):
        """Testet die Erstellung einer Gerade aus zwei Punkten"""
        g = Gerade.from_punkte([0, 0, 0], [1, 1, 1])
        assert np.array_equal(g.stutzvektor, [0, 0, 0])
        assert np.array_equal(g.richtungsvektor, [1, 1, 1])
        
    def test_gerade(self):
        """Testet die Punktberechnung auf der Gerade"""
        g = Gerade([0, 0, 0], [1, 1, 1])
        assert np.array_equal(g.gerade(2), [2, 2, 2])
        
    def test_enthaelt_punkt_true(self):
        """Testet ob ein Punkt auf der Gerade liegt (wahr)"""
        g = Gerade.from_punkte([0, 0, 0], [2, 2, 2])
        p = Punkt([1, 1, 1])
        assert g.enthaelt_punkt(p.punkt) is True
        
    def test_enthaelt_punkt_false(self):
        """Testet ob ein Punkt auf der Gerade liegt (falsch)"""
        g = Gerade.from_punkte([0, 0, 0], [2, 2, 2])
        p = Punkt([1, 2, 3])
        assert g.enthaelt_punkt(p.punkt) is False
        
    def test_abstand_zu_punkt(self):
        """Testet den Abstand zwischen Punkt und Gerade"""
        g = Gerade([0, 0, 0], [1, 0, 0])
        p = Punkt([1, 1, 0])
        assert g.abstand_zu_punkt(p.punkt) == 1.0
        
    def test_winkel_zwei_geraden(self):
        """Testet den Winkel zwischen zwei Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        assert np.isclose(g1.winkel_zwei_geraden(g2, deg=True), 90.0)
        
    def test_lage_gerade_gerade_identisch(self):
        """Testet identische Geraden"""
        g1 = Gerade([0, 0, 0], [1, 1, 1])
        g2 = Gerade([1, 1, 1], [2, 2, 2])
        assert g1.lage_gerade_gerade(g2) == "identisch"
        
    def test_lage_gerade_gerade_parallel(self):
        """Testet parallele Geraden"""
        g1 = Gerade([0, 0, 0], [1, 1, 1])
        g2 = Gerade([1, 0, 0], [2, 2, 2])
        assert g1.lage_gerade_gerade(g2) == "parallel"
        
    def test_lage_gerade_gerade_schneidend(self):
        """Testet sich schneidende Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        assert g1.lage_gerade_gerade(g2) == "schneidend"
        
    def test_lage_gerade_gerade_windschief(self):
        """Testet windschiefe Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 1, 0], [0, 1, 1])
        assert g1.lage_gerade_gerade(g2) == "windschief"
        
    def test_schnitt_mit_gerade(self):
        """Testet den Schnittpunkt zweier Geraden"""
        g1 = Gerade([0, 0, 0], [1, 0, 0])
        g2 = Gerade([0, 0, 0], [0, 1, 0])
        schnitt = g1.schnitt_mit_gerade(g2)
        assert np.array_equal(schnitt, [0, 0, 0])
        
    def test_spurpunkte_gerade(self):
        """Testet die Spurpunkte einer Gerade"""
        g = Gerade.from_punkte([1, 2, 3], [2, 3, 4])
        spur = g.spurpunkte_gerade()
        assert len(spur) == 3