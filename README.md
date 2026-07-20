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

## Beispiel

```python
from analytische_geometrie import Punkt, Gerade

A = Punkt([0, 0, 0])
B = Punkt([2, 2, 2])

g = Gerade(A.punkt, B.punkt)

print(A.abstand_punkt(B))
print(g.punkt(0.5))
```

## Abhängigkeiten

* Python ≥ 3.10
* NumPy

## Lizenz

MIT License.
