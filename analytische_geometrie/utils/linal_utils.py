from ..geometrie.vektor import Vektor

def linsys_solve(A, b, tol=1e-10):
    """
    Löst ein lineares Gleichungssystem mit dem Gauß-Jordan-Verfahren.

    Das Verfahren unterstützt quadratische, überbestimmte und
    unterbestimmte lineare Gleichungssysteme.

    Parameters
    ----------
    A : list[list[float]]
        Koeffizientenmatrix.
    b : list[float]
        Rechte Seite des linearen Gleichungssystems.
    tol : float, optional
        Toleranz für numerische Vergleiche.

    Returns
    -------
    list[float] or None
        Eine Lösung des linearen Gleichungssystems.
        Existieren unendlich viele Lösungen, werden freie Variablen
        auf 0 gesetzt.
        Existiert keine Lösung, wird None zurückgegeben.
    """

    # Erweiterte Matrix erzeugen
    matrix = [
        list(map(float, zeile)) + [float(wert)]
        for zeile, wert in zip(A, b)
    ]

    m = len(matrix)
    n = len(A[0])

    pivot_zeile = 0
    pivot_spalten = []

    # Gauß-Jordan
    for spalte in range(n):

        # Pivot suchen
        pivot = None
        max_wert = tol

        for zeile in range(pivot_zeile, m):
            if abs(matrix[zeile][spalte]) > max_wert:
                max_wert = abs(matrix[zeile][spalte])
                pivot = zeile

        if pivot is None:
            continue

        # Zeilen tauschen
        matrix[pivot_zeile], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_zeile]
        )

        # Pivot normieren
        pivot_wert = matrix[pivot_zeile][spalte]

        for j in range(spalte, n + 1):
            matrix[pivot_zeile][j] /= pivot_wert

        # Alle anderen Zeilen eliminieren
        for zeile in range(m):

            if zeile == pivot_zeile:
                continue

            faktor = matrix[zeile][spalte]

            if abs(faktor) < tol:
                continue

            for j in range(spalte, n + 1):
                matrix[zeile][j] -= faktor * matrix[pivot_zeile][j]

        pivot_spalten.append(spalte)
        pivot_zeile += 1

        if pivot_zeile == m:
            break

    # Numerisches Rauschen entfernen
    for i in range(m):
        for j in range(n + 1):
            if abs(matrix[i][j]) < tol:
                matrix[i][j] = 0.0

    # Widerspruch prüfen
    for zeile in matrix:
        if all(abs(zeile[j]) < tol for j in range(n)) and abs(zeile[-1]) > tol:
            return None

    # Eine Lösung konstruieren
    loesung = [0.0] * n

    for i in range(m):

        pivot = None

        for j in range(n):
            if abs(matrix[i][j] - 1.0) < tol:
                pivot = j
                break

        if pivot is not None:
            loesung[pivot] = matrix[i][-1]

    return loesung

def close(a, b, tol=1e-8):
    if isinstance(a, Vektor):
        if isinstance(b, Vektor):
            return abs((a - b).mod()) < tol
        
        elif isinstance(b, (int, float)):
            return abs(a.mod() - b) < tol
        
    elif isinstance(b, Vektor):
        if isinstance(a, (int, float)):
            return abs(a - b.mod()) < tol
        
    elif isinstance(a, list):
        if isinstance(b, (int, float)):
            return all(abs(x - b) < tol for x in a)
        
        elif isinstance(b, list):
            if len(a) != len(b):
                return False
            return all(abs(a[i] - b[i]) < tol for i in range(len(a)))
        
    return abs(a - b) < tol