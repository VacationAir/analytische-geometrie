# Analytische Geometrie

**Analytische Geometrie** ist eine Python-Bibliothek für Berechnungen der analytischen Geometrie im dreidimensionalen Raum. Sie bietet eine einfache und konsistente API für Punkte, Geraden, Ebenen und ebene Vierecke (*Fassaden*) sowie umfangreiche Funktionen zur Bestimmung von Abständen, Schnittpunkten und Lagebeziehungen.

Die Bibliothek basiert auf **NumPy** und verwendet numerische Toleranzen, um stabile Ergebnisse bei Gleitkommaoperationen zu gewährleisten.

## Funktionen

### Punkte (`Punkt`)

* Erstellung von Punkten im ℝ³
* Abstand zwischen Punkten
* Richtungsvektor zwischen zwei Punkten

### Geraden (`Gerade`)

* Erstellung aus

  * zwei Punkten
  * Stütz- und Richtungsvektor
* Berechnung beliebiger Punkte auf der Geraden
* Lotfußpunkt eines Punktes auf der Geraden
* Abstände zu

  * Punkten
  * Geraden
* Schnittpunkt mit Geraden
* Lagebeziehungen

  * identisch
  * parallel
  * schneidend
  * windschief

### Ebenen (`Ebene`)

* Erstellung aus

  * Punkt und Normalenvektor
  * Punkt und zwei Spannvektoren
* Schnittgerade zweier Ebenen
* Schnittpunkt mit Geraden
* Abstände zu

  * Punkten
  * Geraden
  * Ebenen
* Schnittwinkel
* Lagebeziehungen

  * identisch
  * parallel
  * schneidend

### Fassaden (`Fassade`)

Darstellung begrenzter ebener Vierecke.

Unterstützt unter anderem:

* Mittelpunkt
* Flächeninhalt
* Normalenvektor
* Punkt-in-Fassade-Test
* Lagebeziehungen zwischen Fassaden

  * identisch
  * parallel
  * schneidend
  * außerhalb
  * koplanar schneidend
  * koplanar außerhalb
  * auf Kante
  * berührend
  * kanten schneidend
* Abstand zwischen Fassaden
* Schnittpunkt (falls eindeutig)

## Eigenschaften

* Saubere objektorientierte API
* Numerisch robuste Berechnungen mit `numpy`
* Automatische Behandlung von Rundungsfehlern mittels Toleranzen (`numpy.allclose`)
* Umfangreiche Testabdeckung mit **83 Unit-Tests**
* Für Lehre, Studium und geometrische Anwendungen geeignet

## Installation

```bash
pip install analytische_geometrie
```

# 📚 Beispiele

Nachfolgend finden Sie einige Beispiele für die wichtigsten Funktionen von **`analytische_geometrie`**.

## Grundlegende Geometrie

```python
from analytische_geometrie import Punkt, Gerade

A = Punkt([0, 0, 0])
B = Punkt([2, 2, 2])
C = Punkt([1, 0, 0])

g = Gerade.from_punkte(A.punkt, B.punkt)

print(A.abstand_zu_punkt(B.punkt))
print(g.gerade(0.5))
print(g.enthaelt_punkt(C.punkt))
```

## Ebenen

```python
from analytische_geometrie import Punkt, Ebene

E = Ebene([1, 2, 3], [1, 1, 1])
P = Punkt([4, 5, 6])

print(E.abstand_punkt(P.punkt))
print(E.enthaelt_punkt(P.punkt))
print(E.spurpunkte())
```

## Fassade

```python
from analytische_geometrie import Punkt, Fassade

fassade = Fassade(
    [0, 0, 0],
    [10, 0, 0],
    [10, 8, 0],
    [0, 8, 0]
)

print(fassade.flaecheninhalt())
print(fassade.umfang())
print(fassade.mittelpunkt)

P = Punkt([5, 4, 0])
print(fassade.enthaelt_punkt(P.punkt))
```

## Schnittpunkt zwischen Gerade und Ebene

```python
from analytische_geometrie import Gerade, Ebene

g = Gerade([0, 0, 0], [1, 1, 1])
E = Ebene([1, 0, 0], [0, 1, 0])

print(E.lage_gerade(g))
print(E.schnittpunkt_gerade(g))
```

## Winkelberechnungen

```python
from analytische_geometrie import Gerade, Ebene

g1 = Gerade([0, 0, 0], [1, 0, 0])
g2 = Gerade([0, 0, 0], [1, 1, 0])

print(g1.winkel_zwei_geraden(g2, deg=True))

E = Ebene([0, 0, 0], [0, 0, 1])
print(E.schnittwinkel_gerade(g1, deg=True))

E2 = Ebene([0, 0, 0], [1, 1, 0])
print(E.schnittwinkel_ebene(E2, deg=True))
```


## Abhängigkeiten

* Python ≥ 3.10
* NumPy

## Lizenz

MIT License.
