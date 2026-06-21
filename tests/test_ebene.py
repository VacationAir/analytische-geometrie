import pytest
import numpy as np
from analytische_geometrie.ebene import Ebene
from analytische_geometrie.gerade import Gerade
from analytische_geometrie.punkt import Punkt

class TestEbene:

    def test_creation(self):
        """Testet die Erstellung einer Ebene"""
        E = Ebene([0, 0, 0], [1, 1, 1])
        assert np.array_equal(E.punkt, [0, 0, 0])
        assert np.array_equal(E.norm_vektor, [1, 1, 1])
        
    def test_from_parameterform(self):
        """Testet die Erstellung aus Parameterform"""
        E = Ebene.from_parameterform([1, 0, 0], [0, 1, 0], [0, 0, 1])
        assert np.array_equal(E.norm_vektor, [1, 0, 0])
        
    def test_enthaelt_punkt_true(self):
        """Testet ob Punkt in Ebene liegt (wahr)"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([0, 1, 2])
        assert E.enthaelt_punkt(p.punkt) is True
        
    def test_enthaelt_punkt_false(self):
        """Testet ob Punkt in Ebene liegt (falsch)"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([1, 0, 0])
        assert E.enthaelt_punkt(p.punkt) is False
        
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
        assert np.array_equal(schnitt, [0, 1, 1])
        
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
        assert np.isclose(E1.schnittwinkel_ebene(E2, deg=True), 90.0)
        
    def test_abstand_punkt(self):
        """Testet den Abstand Punkt-Ebene"""
        E = Ebene([0, 0, 0], [1, 0, 0])
        p = Punkt([3, 4, 0])
        assert E.abstand_punkt(p.punkt) == 3.0
        
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
                assert np.isclose(s[0], 0)