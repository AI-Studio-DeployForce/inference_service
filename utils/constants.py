# --------------------------------------------------------------------------- #
# 1.  Cost constants (USD per pixel) – tune as needed                         #
# --------------------------------------------------------------------------- #
COST_PER_PIXEL = {
    "no_damage":      0,     # inspection only
    "minor_damage":   0.12,  # ~ $120 / m² if 1 px ≈ 0.22 m²
    "major_damage":   0.35,  # ~ $350 / m²
    "destroyed":      0.75,  # ~ $750 / m²
}
# --------------------------------------------------------------------------- #

DAMAGE_CLASSES = {
    "no_damage":   {"bgr": (0, 255,   0), "count_key": "num_no_damage"},
    "minor_damage":{"bgr": (0, 255, 255), "count_key": "num_minor_damage"},
    "major_damage":{"bgr": (0, 165, 255), "count_key": "num_major_damage"},
    "destroyed":   {"bgr": (0,   0, 255), "count_key": "num_destroyed"},
}