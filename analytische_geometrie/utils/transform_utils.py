import math

class Transformation:

    @staticmethod
    def skalieren(v, faktor):
        return type(v)(v.x * faktor, v.y * faktor, v.z * faktor)
    
    @staticmethod
    def _drehen_x(v, winkel):
        wkl_rad = math.radians(winkel)
        c = math.cos(wkl_rad)
        s = math.sin(wkl_rad)

        x_prime = v.x
        y_prime = v.x * 0 + v.y * c - v.z * s
        z_prime = v.x * 0 + v.y * s + v.z * c

        return type(v)(x_prime, y_prime, z_prime)

    @staticmethod
    def _drehen_y(v, winkel):
        wkl_rad = math.radians(winkel)
        c = math.cos(wkl_rad)
        s = math.sin(wkl_rad)

        x_prime = v.x * c + v.y * 0 + v.z * s
        y_prime = v.y
        z_prime = - v.x * s + v.y * 0 + v.z * c

        return type(v)(x_prime, y_prime, z_prime)

    @staticmethod
    def _drehen_z(v, winkel):
        wkl_rad = math.radians(winkel)
        c = math.cos(wkl_rad)
        s = math.sin(wkl_rad)

        x_prime = v.x * c - v.y * s + v.z * 0
        y_prime = v.x * s + v.y * c + v.z * 0
        z_prime = v.z
        
        return type(v)(x_prime, y_prime, z_prime)

    @staticmethod
    def drehen(objekt, winkel, achse):
        if achse == "x":
            return Transformation._drehen_x(objekt, winkel)
        if achse == "y":
            return Transformation._drehen_y(objekt, winkel)

        if achse == "z":
            return Transformation._drehen_z(objekt, winkel)

    @staticmethod
    def verschieben(objekt, v):
        return type(v)(objekt.x + v.x, objekt.y + v.y, objekt.z + v.z)

    @staticmethod
    def spiegeln_an_punkt(objekt, P):
        return type(objekt)(P + P - objekt)

    @staticmethod
    def spiegeln_an_gerade(objekt, g):
        L = g.lotfusspunkt(objekt)

        return Transformation.spiegeln_an_punkt(objekt, L)

    @staticmethod
    def spiegeln_an_ebene(objekt, E):
        AP = objekt - E.punkt
        r = AP.dot(E.norm_vektor) / E.norm_vektor.dot(E.norm_vektor)

        L = objekt - r * E.norm_vektor

        return Transformation.spiegeln_an_punkt(objekt, L)