import numpy as np
import pytest
from analytische_geometrie.fassade import Fassade
from analytische_geometrie.punkt import Punkt


class TestFassadeQuadratischEben:
    """
    Testet eine einfache, quadratische Fassade in der xy-Ebene (z = 0).
    Größe: 2x2, Ecken bei (0,0,0), (2,0,0), (2,2,0) und (0,2,0).
    """

    def setup_method(self):
        """Erstellt eine quadratische Fassade in der xy-Ebene"""
        self.f = Fassade(
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        )

    def test_flaecheninhalt(self):
        """Überprüft, ob der Flächeninhalt korrekt als 4.0 berechnet wird"""
        assert np.isclose(self.f.flaecheninhalt(), 4.0)

    def test_mittelpunkt(self):
        """Überprüft, ob der Mittelpunkt bei (1, 1, 0) liegt"""
        assert np.allclose(self.f.mittelpunkt, [1.0, 1.0, 0.0])

    def test_enthaelt_punkt_innen(self):
        """Testet einen Punkt innerhalb der Fassade"""
        p = Punkt([1, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_ausserhalb(self):
        """Testet einen Punkt weit außerhalb der Fassade"""
        p = Punkt([3, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_auf_kante(self):
        """Testet einen Punkt genau auf der unteren Kante"""
        p = Punkt([1, 0, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_auf_ecke(self):
        """Testet einen Punkt genau auf einer der Ecken"""
        p = Punkt([0, 0, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_nicht_in_ebene(self):
        """Testet einen Punkt, der zwar im 'Schatten' liegt, aber auf z=1 (nicht in der Ebene)"""
        p = Punkt([1, 1, 1])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_hinter_kante_unten(self):
        """Testet einen Punkt in der Ebene, aber unterhalb der Fassade"""
        p = Punkt([1, -1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is False
    
    def test_enthaelt_punkt_links_ausserhalb(self):
        """Testet einen Punkt in der Ebene, aber links außerhalb der Fassade"""
        p = Punkt([-1, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_eck_nah_ausserhalb(self):
        """
        Testet einen Punkt, der knapp außerhalb einer Ecke liegt (z.B. nahe an (2,2,0)).
        Wichtig, um Grenzfälle des Lotfußpunkts oder der Winkelsumme zu prüfen.
        """
        p = Punkt([2.1, 2.1, 0.0])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_centro(self):
        p = Punkt([1, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True


    def test_enthaelt_punto_muy_cerca_borde(self):
        p = Punkt([1e-7, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True


    def test_enthaelt_punto_muy_cerca_fuera(self):
        p = Punkt([-1e-7, 1, 0])
        assert self.f.enthaelt_punkt(p.punkt) is False


    def test_enthaelt_punto_casi_esquina(self):
        p = Punkt([2-1e-7, 2-1e-7, 0])
        assert self.f.enthaelt_punkt(p.punkt) is True


    def test_enthaelt_punto_casi_fuera_esquina(self):
        p = Punkt([2+1e-4, 2+1e-4, 0])
        assert self.f.enthaelt_punkt(p.punkt) is False

class TestFassadeInkliniert3D:
    """
    Testet eine geneigte Fassade im echten 3D-Raum (schiefe Ebene).
    Das stellt sicher, dass das Lotfußpunkt- und Projektionsverfahren 
    unabhängig von der Raumorientierung der Fassade funktioniert.
    """

    def setup_method(self):
        """
        Erstellt ein geneigtes Rechteck im Raum.
        Breite = 2, Höhe = sqrt(2). Fläche sollte 2 * sqrt(2) ≈ 2.828427.
        """
        self.f = Fassade(
            [0, 0, 0],
            [2, 0, 0],
            [2, 1, 1],  # Nach oben gekippt um 45 Grad auf der yz-Achse
            [0, 1, 1]
        )

    def test_flaecheninhalt_geneigt(self):
        """Überprüft den Flächeninhalt der schiefen Fassade (Breite * Höhe)"""
        erwartete_flaeche = 2.0 * np.sqrt(2.0)
        assert np.isclose(self.f.flaecheninhalt(), erwartete_flaeche)

    def test_enthaelt_punkt_innen_geneigt(self):
        """Testet den exakten Mittelpunkt der geneigten Fassade"""
        # Der Mittelpunkt der geneigten Fassade liegt bei (1.0, 0.5, 0.5)
        p = Punkt([1.0, 0.5, 0.5])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_ausserhalb_ebene_geneigt(self):
        """Testet einen Punkt, der zwar 'drinnen' wäre, aber flach am Boden (z=0) liegt"""
        # Liegt im 2D-Schatten bei (1, 0.5, 0), ist aber nicht auf der schiefen Ebene
        p = Punkt([1.0, 0.5, 0.0])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_auf_geneigter_kante(self):
        """Testet einen Punkt genau auf der geneigten oberen Kante"""
        # Die obere Kante verläuft von (2,1,1) nach (0,1,1). Die Mitte ist (1,1,1)
        p = Punkt([1.0, 1.0, 1.0])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_geneigt_ausserhalb(self):
        """Testet einen Punkt auf der schiefen Ebene, aber außerhalb der oberen Grenze"""
        # Wir gehen entlang der Ebene weiter nach oben: (1, 2, 2)
        p = Punkt([1.0, 2.0, 2.0])
        assert self.f.enthaelt_punkt(p.punkt) is False

class TestFassadeSuperIrregular3D:
    """
    Testet die Methode `enthaelt_punkt` mit einem absolut unregelmäßigen Viereck 
    (Trapezoid ohne parallele Seiten oder gleiche Winkel), das im Raum geneigt ist.
    
    Geometrie im flachen Zustand:
      - X1 = [0, 0, 0]
      - X2 = [5, -1, 0]
      - X3 = [4, 3, 0]
      - X4 = [-0.5, 2.5, 0]
      
    Rotiert um 45 Grad um die x-Achse:
      - y_rot = y * cos(45°) - z * sin(45°) = y * 0.7071
      - z_rot = y * sin(45°) + z * cos(45°) = y * 0.7071
    """

    def setup_method(self):
        """Erstellt das geneigte, komplett asymmetrische Trapezoid"""
        c = np.cos(np.radians(45))  # ca. 0.70710678
        
        self.f = Fassade(
            [0.0, 0.0, 0.0],          # X1
            [5.0, -1.0 * c, 1.0 * c],  # X2 (ursprünglich [5, -1, 0])
            [4.0, 3.0 * c, 3.0 * c],   # X3 (ursprünglich [4, 3, 0])
            [-0.5, 2.5 * c, 2.5 * c]   # X4 (ursprünglich [-0.5, 2.5, 0])
        )

    def test_enthaelt_punkt_innen_chaos(self):
        """
        Ein Punkt tief im Inneren des unregelmäßigen Vierecks.
        Flach: [2.0, 1.5, 0.0]
        Rotiert: [2.0, 1.5 * cos(45°), 1.5 * sin(45°)]
        """
        c = np.cos(np.radians(45))
        p = Punkt([2.0, 1.5 * c, 1.5 * c])
        assert self.f.enthaelt_punkt(p.punkt) is True

    def test_enthaelt_punkt_ausserhalb_nahe_einbuchtung(self):
        """
        Ein Punkt, der knapp außerhalb liegt, dort wo das Viereck asymmetrisch verläuft.
        Flach: [-1.0, 1.0, 0.0] (Liegt links außerhalb der Kante X4-X1)
        Rotiert: [-1.0, 1.0 * cos(45°), 1.0 * sin(45°)]
        """
        c = np.cos(np.radians(45))
        p = Punkt([-1.0, 1.0 * c, 1.0 * c])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_nahe_ecke_ausserhalb(self):
        """
        Testet ein Punkt nahe der spitzen Ecke X2, aber knapp außerhalb der Kante X1-X2.
        Flach: [4.0, -1.5, 0.0]
        Rotiert: [4.0, -1.5 * cos(45°), -1.5 * sin(45°)]
        """
        c = np.cos(np.radians(45))
        p = Punkt([4.0, -1.5 * c, -1.5 * c])
        assert self.f.enthaelt_punkt(p.punkt) is False

    def test_enthaelt_punkt_nicht_koplanar_chaos(self):
        """
        Testet einen Punkt, der in 2D passt, aber im 3D-Raum über der schiefen Fassade schwebt.
        """
        c = np.cos(np.radians(45))
        # Korrekter Innenpunkt, aber z-Koordinate manipuliert (+1.0)
        p = Punkt([2.0, 1.5 * c, (1.5 * c) + 1.0])
        assert self.f.enthaelt_punkt(p.punkt) is False

class TestFassadeInteraktionen3D:
    """
    Testet die fortgeschrittenen Interaktionen zwischen zwei Fassaden im Raum:
    Lage, Abstand und Schnittfläche/Schnittpunkte.
    """

    def setup_method(self):
        """Erstellt die Basis-Fassade (F1) in der xy-Ebene (z=0)"""
        self.f1 = Fassade(
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        )

    #-----------------------------------------------------------------------#
    # 1. Tests für LAGE_FASSADE & SCHNITT_FASSADE (Intersektion im Raum)
    #-----------------------------------------------------------------------#

    def test_interaktion_identisch(self):
        """Zwei exakt identische Fassaden"""
        f2 = Fassade([0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0])
        assert self.f1.lage_fassade(f2) == "identisch"
        
        # Schnitt einer identischen Fassade gibt die Fassade selbst zurück
        schnitt = self.f1.schnitt_fassade(f2)
        assert isinstance(schnitt, Fassade)
        assert np.allclose(schnitt.mittelpunkt, self.f1.mittelpunkt)

    def test_interaktion_parallel(self):
        """Fassade parallel verschoben auf z = 5.0"""
        f2 = Fassade([0, 0, 5], [2, 0, 5], [2, 2, 5], [0, 2, 5])
        assert self.f1.lage_fassade(f2) == "parallel"
        assert self.f1.schnitt_fassade(f2) is None
        assert np.isclose(self.f1.abstand_fassade(f2), 5.0)

    def test_interaktion_schneidend_perfekt(self):
        """
        F2 schneidet F1 genau in der Mitte wie ein T-Stück.
        F2 steht senkrecht auf F1 bei x = 1.0.
        """
        f2 = Fassade(
            [1, 0, -1],
            [1, 2, -1],
            [1, 2, 1],
            [1, 0, 1]
        )
        assert self.f1.lage_fassade(f2) == "schneidend"
        
        # Der Schnitt muss die unendliche Schnittgerade der Ebenen liefern
        gS = self.f1.schnitt_fassade(f2)
        assert gS is not None
        # Die Gerade muss durch den Schnittbereich verlaufen (z.B. Punkt [1, 1, 0])
        assert np.isclose(gS.abstand_zu_punkt([1, 1, 0]), 0.0)

    def test_interaktion_ausserhalb(self):
        """
        Die Ebenen schneiden sich, aber die Fassaden verfehlen sich im Raum.
        F2 ist senkrecht, steht aber weit verschoben bei x = 10.0.
        """
        f2 = Fassade([10, 0, -1], [10, 2, -1], [10, 2, 1], [10, 0, 1])
        assert self.f1.lage_fassade(f2) == "ausserhalb"
        assert self.f1.schnitt_fassade(f2) is None
        # Der Abstand sollte einfach die Distanz zwischen den nächsten Kanten sein (10 - 2 = 8)
        assert np.isclose(self.f1.abstand_fassade(f2), 8.0)

    #-----------------------------------------------------------------------#
    # 2. Tests für KOPLANARE Fälle (Gleiche Ebene z=0)
    #-----------------------------------------------------------------------#

    def test_interaktion_koplanar_ausserhalb(self):
        """In der selben Ebene, aber weit weg verschoben (kein Kontakt)"""
        f2 = Fassade([5, 0, 0], [7, 0, 0], [7, 2, 0], [5, 2, 0])
        assert self.f1.lage_fassade(f2) == "koplanar_ausserhalb"
        assert self.f1.schnitt_fassade(f2) is None
        assert np.isclose(self.f1.abstand_fassade(f2), 3.0) # Distanz zwischen x=2 und x=5

    def test_interaktion_kanten_schneidend(self):
        """
        Zwei Rahmen kreuzen sich in der selben Ebene an genau einem Punkt.
        F2 ist ein schiefes Viereck, das die Kante von F1 nur an einem Punkt piekst.
        """
        # Ein Dreieck/Viereck, das die Kante x=2 von F1 exakt bei [2, 1, 0] schneidet
        f2 = Fassade([2, 1, 0], [4, 0, 0], [4, 2, 0], [3, 1, 0])
        assert self.f1.lage_fassade(f2) == "kanten_schneidend"
        
        # Sollte exakt den einzelnen Schnittpunkt der Rahmen zurückgeben
        schnitt_pt = self.f1.schnitt_fassade(f2)
        assert schnitt_pt is not None
        assert np.allclose(schnitt_pt, [2.0, 1.0, 0.0])
        assert np.isclose(self.f1.abstand_fassade(f2), 0.0)

    def test_interaktion_koplanar_schneidend(self):
        """
        Überlappung wie zwei Karten auf dem Tisch. 
        F2 ist um 1.0 nach rechts und 1.0 nach oben verschoben.
        Überlappungsbereich ist das Quadrat von [1,1,0] bis [2,2,0].
        """
        f2 = Fassade([1, 1, 0], [3, 1, 0], [3, 3, 0], [1, 3, 0])
        assert self.f1.lage_fassade(f2) == "koplanar_schneidend"
        
        # Deine geniale Methode erzeugt hier eine neue Schnitt-Fassade!
        f_schock = self.f1.schnitt_fassade(f2)
        assert isinstance(f_schock, Fassade)
        # Die Fläche des überlappenden 1x1 Quadrats muss 1.0 sein
        assert np.isclose(f_schock.flaecheninhalt(), 1.0)
        assert np.isclose(self.f1.abstand_fassade(f2), 0.0)

    def test_interaktion_auf_kante(self):
        """Zwei Fassaden liegen perfekt Kante an Kante (Bordsteinkontakt)"""
        f2 = Fassade([2, 0, 0], [4, 0, 0], [4, 2, 0], [2, 2, 0])
        assert self.f1.lage_fassade(f2) == "auf_kante"
        assert np.isclose(self.f1.abstand_fassade(f2), 0.0)

    def test_interaktion_beruehrend_ecke(self):
        """Zwei Fassaden berühren sich nur exakt an einer einzigen Ecke (z.B. bei [2,2,0])"""
        f2 = Fassade([2, 2, 0], [4, 2, 0], [4, 4, 0], [2, 4, 0])
        assert self.f1.lage_fassade(f2) == "beruehrend"
        
        schnitt_pt = self.f1.schnitt_fassade(f2)
        assert schnitt_pt is not None
        assert np.allclose(schnitt_pt, [2.0, 2.0, 0.0])
        assert np.isclose(self.f1.abstand_fassade(f2), 0.0)

    def test_interaktion_auf_kante_teilweise(self):
        f2 = Fassade(
            [2, 1, 0],
            [4, 1, 0],
            [4, 2, 0],
            [2, 2, 0],
        )

        assert self.f1.lage_fassade(f2) == "auf_kante"
        assert np.isclose(self.f1.abstand_fassade(f2), 0.0)

    def test_interaktion_colinear_getrennt(self):
        f2 = Fassade(
            [2, 3, 0],
            [4, 3, 0],
            [4, 5, 0],
            [2, 5, 0],
        )

        assert self.f1.lage_fassade(f2) == "koplanar_ausserhalb"

    def test_interaktion_nur_ein_eckpunkt(self):
        f2 = Fassade(
            [2,2,0],
            [3,2,0],
            [3,3,0],
            [2,3,0],
        )

        assert self.f1.lage_fassade(f2) == "beruehrend"

    def test_interaktion_kante_enthalten(self):
        f2 = Fassade(
            [2,0.5,0],
            [3,0.5,0],
            [3,1.5,0],
            [2,1.5,0],
        )

        assert self.f1.lage_fassade(f2) == "auf_kante"

    def test_interaktion_auf_kante_nur_ende(self):
        f2 = Fassade(
            [2,2,0],
            [4,2,0],
            [4,3,0],
            [2,3,0],
        )

        assert self.f1.lage_fassade(f2) == "beruehrend"
    
    def test_interaktion_auf_kante_nur_inicio(self):
        f2 = Fassade(
            [2,-2,0],
            [4,-2,0],
            [4,0,0],
            [2,0,0],
        )

        assert self.f1.lage_fassade(f2) == "beruehrend"

    def test_schnitt_fassade_auf_kante(self):
        f2 = Fassade(
            [2,0,0],
            [4,0,0],
            [4,2,0],
            [2,2,0],
        )

        assert self.f1.lage_fassade(f2) == "auf_kante"
        assert self.f1.schnitt_fassade(f2) is None
        assert self.f1.abstand_fassade(f2) == 0.0
