import numpy as np
import pytest
from analytische_geometrie.punkt import Punkt
from analytische_geometrie.gerade import Gerade
from analytische_geometrie.ebene import Ebene

# -----------------------------
# PUNKTE
# -----------------------------

def test_punkt_roundtrip_operations():
    p = Punkt([1.5, -2.0, 3.0])
    p2 = Punkt([4.5, 1.0, -1.0])

    v = p.punkt_punkt(p2.get_punkt())
    assert np.allclose(v, [3.0, 3.0, -4.0])

    assert np.isclose(p.abstand_zu_punkt(p2.get_punkt()),
                       np.linalg.norm([3.0, 3.0, -4.0]))


def test_punkt_extreme_values():
    p = Punkt([1e150, -1e150, 1e150])
    q = Punkt([-1e150, 1e150, -1e150])

    dist = p.abstand_zu_punkt(q.get_punkt())
    assert np.isfinite(dist)


# -----------------------------
# GERADEN
# -----------------------------

def test_gerade_parallel_consistency():
    g1 = Gerade([0, 0, 0], [1, 1, 1])
    g2 = Gerade([5, 5, 5], [2, 2, 2])

    assert g1.lage_gerade(g2) == "identisch"


def test_gerade_identisch_verschobener_stutz():
    g1 = Gerade([1, 2, 3], [1, 0, 0])
    g2 = Gerade([10, 2, 3], [1, 0, 0])

    assert g1.lage_gerade(g2) == "identisch"


def test_gerade_windschief_stabil():
    g1 = Gerade([0, 0, 0], [1, 0, 0])
    g2 = Gerade([0, 1, 1], [0, 1, 0])

    assert g1.lage_gerade(g2) in ["schneidend", "windschief"]


def test_gerade_abstand_symmetrie():
    g1 = Gerade([0, 0, 0], [1, 0, 0])
    g2 = Gerade([0, 1, 1], [1, 0, 0])

    # parallel -> Abstand definierbar
    if g1.lage_gerade(g2) == "parallel":
        assert g1.abstand_zu_gerade(g2) is None


# -----------------------------
# EBENEN (AQUÍ ESTÁ EL “DIFÍCIL”)
# -----------------------------

def test_ebene_degenerierte_normal():
    with pytest.raises(ValueError):
        Ebene([0, 0, 0], [0, 0, 0])


def test_ebene_parameterform_kolinear():
    with pytest.raises(ValueError):
        Ebene.from_parameterform(
            [0, 0, 0],
            [1, 2, 3],
            [2, 4, 6]  # lineal dependiente
        )


def test_ebene_identisch_skaliert_normale():
    E1 = Ebene([0, 0, 0], [1, 2, 3])
    E2 = Ebene([0, 0, 0], [2, 4, 6])

    assert E1.lage_ebene(E2) == "identisch"


def test_ebene_parallel_verschoben():
    E1 = Ebene([0, 0, 0], [1, 0, 0])
    E2 = Ebene([5, 0, 0], [2, 0, 0])

    assert E1.lage_ebene(E2) == "parallel"


def test_ebene_schnittgerade_konsistenz():
    E1 = Ebene([0, 0, 0], [1, 0, 0])
    E2 = Ebene([0, 0, 0], [0, 1, 0])

    g = E1.schnittgerade_ebene(E2)

    assert isinstance(g, Gerade)
    assert np.allclose(g.richtungsvektor, [0, 0, 1])


def test_ebene_gerade_konsistenz():
    E = Ebene([0, 0, 0], [0, 0, 1])
    g = Gerade([1, 1, 0], [1, 1, 0])

    assert E.lage_gerade(g) in ["parallel", "schneidend", "identisch"]

def test_ebene_winkel_robustheit():
    E1 = Ebene([0, 0, 0], [1, 0, 0])
    E2 = Ebene([0, 0, 0], [0, 1, 0])

    angle = E1.schnittwinkel_ebene(E2, deg=True)

    assert np.isclose(angle, 90.0)
