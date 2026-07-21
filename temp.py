from analytische_geometrie import Punkt, Gerade

A = Punkt([0, 0, 0])
B = Punkt([2, 2, 2])

g = Gerade.from_punkte(A.punkt, B.punkt)

print(A.abstand_zu_punkt(B.punkt))
