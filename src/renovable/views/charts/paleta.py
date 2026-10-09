"""Paleta institucional compartida por todas las gráficas."""

AZUL = "#0B3C5D"
TEAL = "#1B7F79"
AMBAR = "#F2A900"
CELESTE = "#2E9CCA"
GRIS = "#6B7280"
VERDE = "#7CB342"
ROJO = "#C0392B"
FONDO = "#FFFFFF"
REJILLA = "#E5E7EB"

POR_FUENTE = {
    "AGUA": TEAL,
    "GAS": GRIS,
    "CARBON": "#4B5563",
    "ACPM": "#9CA3AF",
    "COMBUSTOLEO": "#9CA3AF",
    "GLP": "#9CA3AF",
    "JET-A1": "#9CA3AF",
    "RAD SOLAR": AMBAR,
    "VIENTO": CELESTE,
    "BAGAZO": VERDE,
    "BIOMASA": VERDE,
    "BIOGAS": VERDE,
}


def color(fuente: str) -> str:
    return POR_FUENTE.get(fuente.upper(), GRIS)
