# RK3568 SBC — Schematic Design Plan

## Overview

8-sheet hierarchical schematic for an 85x56mm, 8-layer RK3568 SBC with 8GB LPDDR4X,
3x USB-C (two with DP Alt Mode display), onboard WiFi/BT, GbE, and 40-pin GPIO.

Estimated complexity: ~600+ nets, ~150+ components, ~25 unique ICs.

---

## Phase 0 — Project Setup and Library Prep

**Goal**: Get all symbols and footprints ready before drawing anything.

### 0.1 Create Hierarchical Sheet Structure
- Create root sheet with 8 sub-sheet blocks
- Name sheets per the hierarchy in spec
- Add hierarchical labels between sheets for power rails and signal buses

### 0.2 Symbol Sourcing
Most parts are NOT in KiCad default libraries. Each needs sourcing:

| Part | Symbol Source | Priority |
|---|---|---|
| RK3568 (636-pin BGA) | Generate from datasheet / find community lib | CRITICAL |
| RK809-5 (68-pin QFN) | Generate from datasheet | CRITICAL |
| K4UBE3D4AM (LPDDR4X) | Generate from datasheet | CRITICAL |
| KLMBG2JETD (eMMC) | Standard eMMC symbol (generic) | MEDIUM |
| W25Q128JVSIQ (SPI NOR) | KiCad built-in (Memory_Flash:W25Q128JVS) | EASY |
| IT6505FN | Generate from datasheet | CRITICAL |
| LT8711HE | Generate from datasheet | CRITICAL |
| TUSB1064 | Search component DB / TI library | MEDIUM |
| FUSB302B | Search component DB / onsemi lib | MEDIUM |
| VL805 | Search component DB / generate | MEDIUM |
| RTL8211F-CG | Search component DB / community libs | MEDIUM |
| AP6256 | Generate from module datasheet | MEDIUM |
| USB-C connector | KiCad built-in | EASY |
| Passives (R, C, L) | KiCad built-in (Device:R, Device:C, etc.) | EASY |
| Power symbols | KiCad built-in (power:GND, etc.) | EASY |

**Strategy**: Search component databases (JLCPCB, Mouser, DigiKey) first. If a KiCad
symbol exists, import it. For critical ICs (RK3568, RK809-5, LPDDR4X), we will likely
need to generate symbols from datasheets using the generate_symbol tool.

### 0.3 Power Rail Inventory
Define all rails up front so hierarchical labels are consistent across sheets:

| Rail Name | Voltage | Source | Consumers |
|---|---|---|---|
| VCC_5V0 | 5.0V | USB-C PD input | VBUS switches, PMIC input |
| VCC_SYS | ~5V | After input protection/switch | RK809-5 PMIC input |
| VDD_CPU | 0.8-1.15V | RK809-5 DCDC_REG1 | RK3568 CPU core |
| VDD_GPU | 0.8-1.0V | RK809-5 DCDC_REG2 | RK3568 GPU core |
| VDD_LOGIC | 0.8-0.9V | RK809-5 DCDC_REG3 | RK3568 logic |
| VCC_DDR | 0.6V | RK809-5 DCDC_REG4 | LPDDR4X (VDDQ) |
| VCC_1V8 | 1.8V | RK809-5 LDO | SoC I/O, eMMC VCCQ, misc |
| VCC_3V3 | 3.3V | RK809-5 LDO or ext reg | SD card, ETH PHY, WiFi, GPIO |
| VCC_0V9 | 0.9V | RK809-5 LDO | USB3 PHY, HDMI PHY |
| VCCIO_1V8 | 1.8V | RK809-5 LDO | SoC VCCIO domains |
| VCCIO_3V3 | 3.3V | RK809-5 LDO | SoC VCCIO domains |
| VCC_1V0_VL805 | 1.0V | SY8088AAC buck | VL805 core |
| VCC_3V3_ETH | 3.3V | Filtered from VCC_3V3 | RTL8211F |
| VCC_3V3_WIFI | 3.3V | Filtered from VCC_3V3 | AP6256 |
| VBUS_1/2/3 | 5.0V | Load switches from VCC_5V0 | USB-C port VBUS output |

---

## Phase 1 — Root Sheet (Top-Level Block Diagram)

**Sheet**: test_board_20.kicad_sch

### Tasks
1. Place 8 hierarchical sheet symbols arranged logically
2. Add hierarchical pins on each sheet block for inter-sheet signals
3. Add title block, revision, notes

**Depends on**: Nothing (first sheet to build)
**Estimated effort**: Light (structural only)

---

## Phase 2 — PMIC and Power (Sheet 2)

**Sheet**: pmic_power.kicad_sch

### Why First
Everything depends on power. The RK809-5 generates all core rails.

### Tasks
1. Source the RK809-5 symbol (generate from datasheet if not available)
2. Input power path:
   - VCC_5V0 input (from USB-C sheet via hierarchical label)
   - Input protection (TVS diode, bulk caps)
   - Power path switch/ideal diode
3. RK809-5 PMIC circuit:
   - 4x DCDC converters with inductors and output caps
   - 9x LDO outputs with output caps
   - I2C connection to SoC (PMIC_SDA, PMIC_SCL)
   - Power sequencing: PWRON, RESET, INT signals
   - 32.768kHz crystal for RTC
4. Supplemental regulators:
   - SY8088AAC for VCC_1V0_VL805
   - AP2112K-3.3 for VCC_3V3_SD
   - AP2112K-1.8 for spare 1.8V
5. Power flags and labels for every rail
6. Decoupling: bulk + ceramic caps per rail

### Key Signals to Export (hierarchical labels)
VDD_CPU, VDD_GPU, VDD_LOGIC, VCC_DDR, VCC_1V8, VCC_3V3,
VCC_0V9, VCCIO_*, VCC_5V0, VCC_SYS, VCC_1V0_VL805,
PMIC_SDA, PMIC_SCL, PMIC_INT, SYS_RESET, PWRON

**Depends on**: Phase 0 (RK809-5 symbol)
**Estimated effort**: Heavy (most complex analog sheet)

---

## Phase 3 — RK3568 Core (Sheet 1)

**Sheet**: rk3568_core.kicad_sch

### Tasks
1. Source the RK3568 symbol (636-pin BGA, multi-unit):
   - Unit A: CPU/Power pins
   - Unit B: DDR interface
   - Unit C: HDMI/eDP/MIPI display
   - Unit D: USB/PCIe/SATA (multi-PHY)
   - Unit E: SDIO/eMMC/SPI
   - Unit F: GPIO/UART/I2C/SPI/misc
2. Clock circuits:
   - 24MHz crystal (main oscillator) with load caps
3. Reset circuit:
   - Reset button + RC filter
   - SYS_RESET from PMIC
4. Boot configuration:
   - Boot mode strapping resistors (eMMC/SD/SPI boot select)
5. JTAG/debug header:
   - 10-pin ARM JTAG/SWD header
6. Power pin decoupling:
   - ~50+ bypass caps (100nF) per VCC ball group
   - Bulk caps per power domain
7. Hierarchical labels for ALL bus interfaces going to other sheets

### Key Challenge
The RK3568 is a 636-pin BGA. The symbol will be large and split into
multiple units. This is the single most complex symbol on the board.

**Depends on**: Phase 0 (RK3568 symbol), Phase 2 (power rails)
**Estimated effort**: Very heavy (largest symbol, most bypass caps)

---

## Phase 4 — LPDDR4X Memory (Sheet 3)

**Sheet**: lpddr4x.kicad_sch

### Tasks
1. Source LPDDR4X symbol (Samsung K4UBE3D4AM-MGCL, FBGA-200)
2. Connect DDR bus:
   - 2x channels (CH_A, CH_B), each 16-bit data
   - CA (command/address) bus per channel
   - CK/CK# differential clocks per channel
   - DQS/DQS# strobes (2 per channel for x16)
   - CS#, CKE, ODT, RESET# control signals
3. Termination:
   - ZQ calibration resistors (240 ohm to GND per channel)
4. Decoupling:
   - VDD1 (1.8V core), VDD2 (1.1V), VDDQ (0.6V)
   - ~30+ bypass caps
5. Power filtering:
   - Ferrite beads on VDD1, VDD2, VDDQ supply entry

**Depends on**: Phase 3 (RK3568 DDR bus labels)
**Estimated effort**: Medium-heavy (dense but single IC)

---

## Phase 5 — Storage (Sheet 4)

**Sheet**: storage.kicad_sch

### Tasks
1. eMMC circuit:
   - Samsung KLMBG2JETD-B041 (32GB eMMC 5.1)
   - 8-bit data bus + CMD + CLK
   - VCCQ (1.8V), VCC (3.3V) with decoupling
   - Reset pin connection
2. Micro SD card slot:
   - SD 3.0 / UHS-I (4-bit mode)
   - Card detect pin
   - ESD protection
3. SPI NOR flash:
   - W25Q128JVSIQ on SPI bus
   - CS#, CLK, MOSI, MISO
   - Pull-up on CS#, decoupling caps

**Depends on**: Phase 3 (eMMC/SD/SPI bus labels)
**Estimated effort**: Medium (well-documented interfaces)

---

## Phase 6 — USB-C Ports (Sheet 5)

**Sheet**: usb_c_ports.kicad_sch

### Tasks
1. USB-C Port 1 (OTG + HDMI display + PD sink/source):
   - USB-C 24-pin receptacle
   - FUSB302B for CC logic and PD negotiation
   - TUSB1064 for DP Alt Mode lane muxing
   - USB3 OTG0 SS differential pairs to TUSB1064
   - HDMI-converted-to-DP lanes (from Sheet 6) to TUSB1064
   - USB2 D+/D- through USB-C
   - VBUS input path (this port powers the board)
   - NCP45520 VBUS load switch (for source mode)
   - ESD protection (USBLC6-2SC6)
2. USB-C Port 2 (HOST + eDP display + PD source):
   - Same topology as Port 1 but HOST + eDP display path
3. USB-C Port 3 (HOST via VL805 + PD source):
   - FUSB302B for CC logic
   - No display mux (data-only USB-C)
   - VL805 PCIe-to-USB3 controller
   - NCP45520 VBUS load switch
4. USB 2.0 HOST ports (x2):
   - Routed internally to WiFi module and spare header

### Key Challenge
Most complex peripheral sheet. Each USB-C port with DP Alt Mode
requires careful muxing of SS lanes between USB data and DP data.

**Depends on**: Phase 3 (USB3/PCIe bus labels), Phase 7 (DP lane inputs)
**Estimated effort**: Very heavy (3 ports, 2 mux ICs, 3 PD controllers, 1 hub IC)

---

## Phase 7 — Display (Sheet 6)

**Sheet**: display.kicad_sch

### Tasks
1. HDMI 2.0a TX path:
   - HDMI TMDS differential pairs (CLK + 3 data lanes) from RK3568
   - HDMI DDC (I2C) for EDID
   - HDMI CEC and HPD
   - LT8711HE HDMI-to-DP converter
   - DP output lanes to Sheet 5 (USB-C Port 1 mux)
2. eDP 1.3 TX path:
   - eDP differential pairs (CLK + 4 data lanes) from RK3568
   - eDP AUX channel and HPD
   - IT6505FN eDP-to-DP converter
   - DP output lanes to Sheet 5 (USB-C Port 2 mux)

**Depends on**: Phase 3 (HDMI/eDP bus labels)
**Estimated effort**: Heavy (two converter ICs, high-speed differential)

---

## Phase 8 — Ethernet and WiFi (Sheet 7)

**Sheet**: ethernet_wifi.kicad_sch

### Tasks
1. Gigabit Ethernet:
   - RTL8211F-CG PHY via RGMII to RK3568 GMAC0
   - 25MHz crystal
   - RJ45 jack with integrated magnetics
   - PHY address strapping resistors
   - LED indicators via RJ45 integrated LEDs
2. WiFi / Bluetooth:
   - AP6256 module via SDIO 3.0 (WiFi) + UART (BT)
   - Chip antenna or U.FL connector
   - Power filtering (ferrite bead + decoupling)
   - Enable/reset and wake GPIOs

**Depends on**: Phase 3 (RGMII/SDIO bus labels)
**Estimated effort**: Medium (well-documented ICs)

---

## Phase 9 — GPIO and Misc (Sheet 8)

**Sheet**: gpio_misc.kicad_sch

### Tasks
1. 40-pin GPIO header (Pi-compatible pinout)
   - ESD protection on GPIO lines
   - Series resistors (33 ohm) on select lines
   - Power pins: 5V (x2), 3.3V (x2), GND (x8)
2. Debug UART (3-pin header: TX, RX, GND)
3. Status LEDs (power green, activity blue)
4. Reset button with debounce RC
5. Optional user/recovery button

**Depends on**: Phase 3 (GPIO/UART labels)
**Estimated effort**: Light (simple passive circuits)

---

## Phase 10 — Integration and Verification

### Tasks
1. Cross-sheet connectivity audit:
   - Verify every hierarchical label has a matching pair
   - Verify every power rail reaches all sheets that need it
   - Run sch_get_nets to check net connectivity
2. Per-sheet review:
   - sch_get_summary + screenshot on every sheet
   - Fix orphaned labels, junctions, power symbols
3. ERC:
   - Run sch_run_erc on full hierarchy
   - Fix genuine errors (unconnected pins, conflicting drivers)
   - Document expected false positives (power pin warnings)
4. Final audit:
   - Every IC pin either connected or marked no-connect
   - Every power domain has bulk + ceramic decoupling
   - All bypass caps placed via sch_place_companions
   - Consistent net naming across all sheets

---

## Execution Order Summary

```
Phase 0: Library Prep (symbols/footprints)
    |
Phase 1: Root Sheet (hierarchy skeleton)
    |
Phase 2: PMIC & Power (RK809-5, all rails)
    |
Phase 3: RK3568 Core (SoC, clocks, reset, boot)
    |
    +---> Phase 4: LPDDR4X Memory
    +---> Phase 5: Storage (eMMC, SD, SPI NOR)
    +---> Phase 6: USB-C Ports (3x USB-C, PD, mux, VL805)
    +---> Phase 7: Display (HDMI->DP, eDP->DP converters)
    +---> Phase 8: Ethernet & WiFi (RTL8211F, AP6256)
    +---> Phase 9: GPIO & Misc (40-pin header, LEDs)
    |
Phase 10: Integration & Verification (ERC, audit, screenshots)
```

**Critical path**: Phase 0 -> 1 -> 2 -> 3 -> 4/5/6/7/8/9 (parallel) -> 10

Phase 0 (symbol sourcing) gates everything. The RK3568 636-pin symbol is the
single biggest blocker.

---

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| RK3568 symbol unavailable | Blocks all work | Generate from datasheet; split into 6+ units |
| RK809-5 symbol unavailable | Blocks power sheet | Generate from datasheet; ~68 pins |
| LPDDR4X pin mapping errors | Silent memory failure | Cross-reference Samsung datasheet ball map |
| Display converter pin mismatch | No display output | Verify IT6505/LT8711HE datasheets pin-for-pin |
| USB-C mux config complexity | Incorrect lane routing | Follow TI TUSB1064 reference design exactly |
| Board area too tight | Components dont fit | Flag early; may need to go to ~90x60mm |
| ERC noise from 636-pin BGA | Hard to find real errors | Methodical pin-by-pin NC marking on unused pins |
