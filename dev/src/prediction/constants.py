from enum import Enum


class ActivityFactor(str, Enum):
    MUY_LIGERA= 1.2
    LIGERA= 1.375
    MODERADA= 1.55
    INTENSA= 1.725
    MUY_INTENSA= 1.9

class Gender(str, Enum):
    FEMENINO= "F"
    MASCULINO= "M"

# Factor de ajuste calorico, se tomara como limite inferior el equivalente al 50% del valor mostrado
class Objectives(str, Enum):
    PERDER_PESO= 1000
    GANAR_MASA_MUSCULAR= 500 
    MANTENER_PESO= 0

