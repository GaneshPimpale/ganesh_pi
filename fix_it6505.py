#!/usr/bin/env python3
"""Regenerate IT6505 symbol with proper 2.54mm pin spacing."""

# Pin definitions grouped by side
# Left side pins (48 pins) - facing right (angle 0)
left_pins = [
    # OD35-OD24 (upper parallel data)
    ("input", "OD35", "79"), ("input", "OD34", "80"), ("input", "OD33", "81"),
    ("input", "OD32", "82"), ("input", "OD31", "83"), ("input", "OD30", "84"),
    ("input", "OD29", "85"), ("input", "OD28", "86"), ("input", "OD27", "87"),
    ("input", "OD26", "88"), ("input", "OD25", "89"), ("input", "OD24", "90"),
    # OD23-OD12
    ("input", "OD23", "94"), ("input", "OD22", "95"), ("input", "OD21", "96"),
    ("input", "OD20", "97"), ("input", "OD19", "98"), ("input", "OD18", "99"),
    ("input", "OD17", "100"), ("input", "OD16", "101"), ("input", "OD15", "102"),
    ("input", "OD14", "103"), ("input", "OD13", "104"), ("input", "OD12", "105"),
    # OD11-OD0
    ("input", "OD11", "109"), ("input", "OD10", "110"), ("input", "OD9", "111"),
    ("input", "OD8", "112"), ("input", "OD7", "113"), ("input", "OD6", "114"),
    ("input", "OD5", "115"), ("input", "OD4", "116"), ("input", "OD3", "117"),
    ("input", "OD2", "118"), ("input", "OD1", "119"), ("input", "OD0", "120"),
    # Timing
    ("input", "DE", "121"), ("input", "PCLK", "123"),
    ("input", "HSYNC", "125"), ("input", "VSYNC", "126"),
    # Audio
    ("input", "SCK", "32"), ("input", "WS", "31"),
    ("input", "I2S0", "30"), ("input", "I2S1", "29"),
    ("input", "I2S2", "28"), ("input", "I2S3", "27"),
    ("input", "MCLK", "26"), ("input", "SPDIF", "25"),
]

# Right side pins (56 pins) - facing left (angle 180)
right_pins = [
    # Control/I2C
    ("input", "PCSCL", "73"), ("bidirectional", "PCSDA", "74"),
    ("input", "PCADR", "72"), ("open_collector", "~{INT}", "75"),
    ("input", "~{SYSRSTN}", "36"), ("input", "HPD", "37"),
    ("input", "ENTEST", "71"),
    # DP TX lanes
    ("output", "TX3P", "44"), ("output", "TX3N", "43"),
    ("output", "TX2P", "48"), ("output", "TX2N", "47"),
    ("output", "TX1P", "52"), ("output", "TX1N", "51"),
    ("output", "TX0P", "56"), ("output", "TX0N", "55"),
    # AUX
    ("bidirectional", "TXAUXP", "40"), ("bidirectional", "TXAUXN", "39"),
    # Crystal
    ("input", "XTALIN", "69"), ("output", "XTALOUT", "68"),
    # REXT
    ("passive", "REXT", "59"),
    # ED35-ED0 (36 even data pins)
    ("input", "ED35", "128"), ("input", "ED34", "129"), ("input", "ED33", "130"),
    ("input", "ED32", "131"), ("input", "ED31", "132"), ("input", "ED30", "133"),
    ("input", "ED29", "134"), ("input", "ED28", "135"), ("input", "ED27", "136"),
    ("input", "ED26", "137"), ("input", "ED25", "138"), ("input", "ED24", "139"),
    ("input", "ED23", "142"), ("input", "ED22", "143"), ("input", "ED21", "144"),
    ("input", "ED20", "1"), ("input", "ED19", "2"), ("input", "ED18", "3"),
    ("input", "ED17", "4"), ("input", "ED16", "5"), ("input", "ED15", "6"),
    ("input", "ED14", "7"), ("input", "ED13", "8"), ("input", "ED12", "9"),
    ("input", "ED11", "13"), ("input", "ED10", "14"), ("input", "ED9", "15"),
    ("input", "ED8", "16"), ("input", "ED7", "17"), ("input", "ED6", "18"),
    ("input", "ED5", "19"), ("input", "ED4", "20"), ("input", "ED3", "21"),
    ("input", "ED2", "22"), ("input", "ED1", "23"), ("input", "ED0", "24"),
]

# Top pins (22 VCC power pins) - facing down (angle 270)
top_pins = [
    ("power_in", "IVDD", "12"), ("power_in", "IVDD", "35"),
    ("power_in", "IVDD", "76"), ("power_in", "IVDD", "91"),
    ("power_in", "IVDD", "106"), ("power_in", "IVDD", "122"),
    ("power_in", "IVDD", "140"),
    ("power_in", "OVDD", "10"), ("power_in", "OVDD", "33"),
    ("power_in", "OVDD", "78"), ("power_in", "OVDD", "108"),
    ("power_in", "OVDD", "127"),
    ("power_in", "AVCC", "41"), ("power_in", "AVCC", "46"),
    ("power_in", "AVCC", "50"), ("power_in", "AVCC", "54"),
    ("power_in", "AVCC", "58"),
    ("power_in", "PVCC0", "65"), ("power_in", "PVCC1", "61"),
    ("power_in", "PVCC2", "63"),
    ("power_in", "XVCC18", "67"), ("power_in", "EMEM_VPP", "93"),
]

# Bottom pins (18 GND power pins) - facing up (angle 90)
bottom_pins = [
    ("power_in", "IOVSS", "11"), ("power_in", "IOVSS", "34"),
    ("power_in", "IOVSS", "77"), ("power_in", "IOVSS", "92"),
    ("power_in", "IOVSS", "107"), ("power_in", "IOVSS", "124"),
    ("power_in", "IOVSS", "141"),
    ("power_in", "AGND", "38"), ("power_in", "AGND", "42"),
    ("power_in", "AGND", "45"), ("power_in", "AGND", "49"),
    ("power_in", "AGND", "53"), ("power_in", "AGND", "57"),
    ("power_in", "AGND", "60"),
    ("power_in", "PGND0", "66"), ("power_in", "PGND0", "70"),
    ("power_in", "PGND1", "62"), ("power_in", "PGND2", "64"),
]

# Calculate dimensions
n_left = len(left_pins)    # 48
n_right = len(right_pins)  # 56
n_top = len(top_pins)      # 22
n_bottom = len(bottom_pins) # 18

pin_spacing = 2.54
pin_length = 2.54

# Vertical extent driven by right side (most pins)
max_side = max(n_left, n_right)
half_h = (max_side - 1) * pin_spacing / 2 + 1.27  # +1.27 margin
# Round up to nearest 2.54
import math
half_h = math.ceil(half_h / 2.54) * 2.54  # 71.12 -> 71.12

# Horizontal extent driven by top (most pins)  
max_tb = max(n_top, n_bottom)
half_w = (max_tb - 1) * pin_spacing / 2 + 1.27
half_w = math.ceil(half_w / 2.54) * 2.54  # 27.94 -> 27.94

print(f"Body: {half_w*2} x {half_h*2} mm")
print(f"Left: {n_left} pins, Right: {n_right} pins")
print(f"Top: {n_top} pins, Bottom: {n_bottom} pins")

# Generate pin lines
def pin_line(etype, name, number, x, y, angle):
    return f'      (pin {etype} line (at {x:.2f} {y:.2f} {angle}) (length {pin_length}) (name "{name}" (effects (font (size 0.762 0.762)))) (number "{number}" (effects (font (size 0.762 0.762)))))'

lines = []

# Left side: x = -(half_w + pin_length), angle = 0 (pointing right)
lx = -(half_w + pin_length)
ly_start = (n_left - 1) * pin_spacing / 2
for i, (etype, name, num) in enumerate(left_pins):
    y = ly_start - i * pin_spacing
    lines.append(pin_line(etype, name, num, lx, y, 0))

# Right side: x = (half_w + pin_length), angle = 180 (pointing left)
rx = half_w + pin_length
ry_start = (n_right - 1) * pin_spacing / 2
for i, (etype, name, num) in enumerate(right_pins):
    y = ry_start - i * pin_spacing
    lines.append(pin_line(etype, name, num, rx, y, 180))

# Top: y = (half_h + pin_length), angle = 270 (pointing down)
ty = half_h + pin_length
tx_start = -(n_top - 1) * pin_spacing / 2
for i, (etype, name, num) in enumerate(top_pins):
    x = tx_start + i * pin_spacing
    lines.append(pin_line(etype, name, num, x, ty, 270))

# Bottom: y = -(half_h + pin_length), angle = 90 (pointing up)
by = -(half_h + pin_length)
bx_start = -(n_bottom - 1) * pin_spacing / 2
for i, (etype, name, num) in enumerate(bottom_pins):
    x = bx_start + i * pin_spacing
    lines.append(pin_line(etype, name, num, x, by, 90))

# Verify pin count
total = n_left + n_right + n_top + n_bottom
print(f"Total pins: {total}")
assert total == 144, f"Expected 144, got {total}"

# Build symbol file
ref_y = half_h + pin_length + 2.54
val_y = -(half_h + pin_length + 2.54)

sym = f"""(kicad_symbol_lib
\t(version 20241209)
\t(generator "zeo_agent")
\t(generator_version "1.0")
(symbol "IT6505"
    (pin_names (offset 0.508))
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "U" (at 0 {ref_y:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "IT6505" (at 0 {val_y:.2f} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Package_QFP:LQFP-144_20x20mm_P0.5mm" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "https://www.ite.com.tw" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "IT6505_0_1"
      (rectangle (start {-half_w:.2f} {half_h:.2f}) (end {half_w:.2f} {-half_h:.2f})
        (stroke (width 0.254) (type default))
        (fill (type background))
      )
    )
    (symbol "IT6505_1_1"
{chr(10).join(lines)}
    )
  )

)"""

with open("/Users/gmp/workspaces/test_boards/test_board_20/libraries/IT6505/IT6505.kicad_sym", "w") as f:
    f.write(sym)

print("Symbol written successfully!")
print(f"Half width: {half_w}, Half height: {half_h}")
print(f"Left pin x: {lx}, Right pin x: {rx}")
print(f"Top pin y: {ty}, Bottom pin y: {by}")
