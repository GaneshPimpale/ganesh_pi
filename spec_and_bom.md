# RK3568 SBC — "Open Pi" — Parts List & Spec Summary

## Board Overview
- **Form Factor**: 85 x 56 mm (Raspberry Pi 4 footprint)
- **PCB Layers**: 8 (SIG-GND-SIG-PWR | PWR-SIG-GND-SIG)
- **Mounting**: 4x M2.5 holes, Pi-compatible 58x49mm pattern
- **Power Input**: USB-C Port 1 (PD sink, 5V-15V) or 5V/4A pin header

---

## Key Components

### 1. SoC
| Part | Description | Package | Qty |
|---|---|---|---|
| Rockchip RK3568 | Quad Cortex-A55 @ 2.0GHz, Mali G52, 0.8T NPU | FCBGA636L (19x19mm) | 1 |

### 2. PMIC
| Part | Description | Package | Qty |
|---|---|---|---|
| Rockchip RK809-5 | Companion PMIC — 4x DCDC, 9x LDO, RTC | QFN-68 | 1 |

### 3. Memory — 8GB LPDDR4X
| Part | Description | Package | Qty |
|---|---|---|---|
| Samsung K4UBE3D4AM-MGCL | 8GB LPDDR4X, 4266MT/s, dual-ch x16 (x32) | FBGA-200 | 1 |

### 4. Storage
| Part | Description | Package | Qty |
|---|---|---|---|
| Samsung KLMBG2JETD-B041 | 32GB eMMC 5.1 | FBGA-153 | 1 |
| Winbond W25Q128JVSIQ | 16MB SPI NOR flash (bootloader) | SOIC-8 | 1 |
| Micro SD connector | SD 3.0 / UHS-I push-push slot | — | 1 |

### 5. Display Converters
| Part | Description | Package | Qty |
|---|---|---|---|
| ITE IT6505FN | eDP 1.3 -> DisplayPort 1.2 converter | QFN-56 | 1 |
| Lontium LT8711HE | HDMI 2.0 -> DisplayPort 1.2 converter | QFN-48 | 1 |

### 6. USB-C Port ICs
| Part | Description | Package | Qty |
|---|---|---|---|
| TI TUSB1064 | USB-C DP Alt Mode 10Gbps redriver/mux | QFN-32 | 2 |
| ON Semi FUSB302B | USB PD PHY + CC logic | WLCSP-9 | 3 |
| VIA VL805 | PCIe 3.0 x1 -> 4-port USB 3.0 host ctrl | QFN-68 | 1 |
| USB-C receptacle | 24-pin USB Type-C (e.g. GCT USB4125) | SMD | 3 |

### 7. Ethernet
| Part | Description | Package | Qty |
|---|---|---|---|
| Realtek RTL8211F-CG | GbE PHY (RGMII) | QFN-48 (6x6mm) | 1 |
| RJ45 w/ magnetics | Integrated magnetics jack (e.g. HFJ11-2450E) | TH | 1 |

### 8. WiFi / Bluetooth
| Part | Description | Package | Qty |
|---|---|---|---|
| Ampak AP6256 | WiFi 5 (ac) + BT 5.0 module, SDIO + UART | LGA (12x12mm) | 1 |
| Chip antenna or U.FL | 2.4/5GHz dual-band | SMD | 1 |

### 9. Supplemental Power
| Part | Description | Package | Qty |
|---|---|---|---|
| SY8088AAC | 3.3V -> 1.0V buck for VL805 core | SOT-23-5 | 1 |
| AP2112K-3.3 | LDO 3.3V for SD card / misc | SOT-23-5 | 1 |
| AP2112K-1.8 | LDO 1.8V for eMMC VCCQ / misc | SOT-23-5 | 1 |
| NCP45520 | USB VBUS load switch 5V (per port) | SOT-23-5 | 3 |

### 10. Clocks & Passives
| Part | Description | Package | Qty |
|---|---|---|---|
| 24MHz crystal | Main SoC oscillator | 2520 SMD | 1 |
| 25MHz crystal | Ethernet PHY oscillator | 2520 SMD | 1 |
| 32.768kHz crystal | RTC crystal for RK809-5 | 2012 SMD | 1 |
| USBLC6-2SC6 | ESD protection (USB-C ports) | SOT-23-6 | 3 |
| PRTR5V0U2X | ESD protection (display lines) | SOT-143B | 2 |
| 2x20 pin header | 40-pin GPIO (Pi-compatible) | 2.54mm TH | 1 |
| Status LEDs | Power (green), activity (blue) | 0402 | 2 |
| Tactile switch | Reset button | SMD 3x4mm | 1 |

---

## SerDes / Multi-PHY Lane Allocation

```
Combo PHY 0 --> USB3 OTG0 SS  --> USB-C Port 1 (+ HDMI display via DP Alt Mode)
Combo PHY 1 --> USB3 HOST1 SS --> USB-C Port 2 (+ eDP display via DP Alt Mode)
Combo PHY 2 --> PCIe 2.1 x1   --> VL805 --> USB-C Port 3 (data only)
PCIe 3.0    --> 2 lanes FREE   (dedicated PHY, not shared — future NVMe/expansion)
```

## Display Signal Paths

```
RK3568 HDMI 2.0a TX --> LT8711HE --> DP lanes --> TUSB1064 mux --> USB-C Port 1
RK3568 eDP 1.3 TX   --> IT6505FN  --> DP lanes --> TUSB1064 mux --> USB-C Port 2
```

## USB-C Port Summary

```
Port 1: USB3 OTG + HDMI->DP Alt Mode + PD sink (board power input) / PD source
Port 2: USB3 HOST + eDP->DP Alt Mode + PD source (5V/1.5A)
Port 3: USB3 HOST (via VL805 on PCIe 2.1) + PD source (5V/1.5A)
```

## Power Rail Inventory

| Rail | Voltage | Source | Key Consumers |
|---|---|---|---|
| VCC_5V0 | 5.0V | USB-C PD input | VBUS switches, PMIC input |
| VCC_SYS | ~5V | After input protection | RK809-5 input |
| VDD_CPU | 0.8-1.15V | RK809-5 DCDC1 | RK3568 CPU core |
| VDD_GPU | 0.8-1.0V | RK809-5 DCDC2 | RK3568 GPU core |
| VDD_LOGIC | 0.8-0.9V | RK809-5 DCDC3 | RK3568 logic |
| VCC_DDR | 0.6V | RK809-5 DCDC4 | LPDDR4X VDDQ |
| VCC_1V8 | 1.8V | RK809-5 LDO | SoC I/O, eMMC VCCQ |
| VCC_3V3 | 3.3V | RK809-5 LDO | SD, ETH, WiFi, GPIO |
| VCC_0V9 | 0.9V | RK809-5 LDO | USB3 PHY, HDMI PHY |
| VCC_1V0_VL805 | 1.0V | SY8088AAC buck | VL805 core |
| VCC_3V3_ETH | 3.3V | Filtered VCC_3V3 | RTL8211F |
| VCC_3V3_WIFI | 3.3V | Filtered VCC_3V3 | AP6256 |
| VBUS_1/2/3 | 5.0V | NCP45520 switches | USB-C port VBUS |

## 40-Pin GPIO Header (Pi-Compatible Target)

```
Pin  Signal              Pin  Signal
 1   3V3                  2   5V
 3   I2C1_SDA             4   5V
 5   I2C1_SCL             6   GND
 7   GPIO3_C4             8   UART2_TX
 9   GND                 10   UART2_RX
11   GPIO3_A1            12   I2S1_SCLK
13   GPIO3_A2            14   GND
15   GPIO3_A3            16   GPIO3_A4
17   3V3                 18   GPIO3_A5
19   SPI1_MOSI           20   GND
21   SPI1_MISO           22   GPIO3_A6
23   SPI1_CLK            24   SPI1_CS0
25   GND                 26   SPI1_CS1
27   I2C5_SDA            28   I2C5_SCL
29   GPIO3_B5            30   GND
31   GPIO3_B6            32   PWM0
33   PWM1                34   GND
35   I2S1_LRCK           36   UART4_TX
37   GPIO3_C2            38   UART4_RX
39   GND                 40   GPIO3_C3
```

## Schematic Hierarchy

```
Root: test_board_20.kicad_sch
  |-- Sheet 1: rk3568_core.kicad_sch      (SoC, clocks, reset, boot, JTAG)
  |-- Sheet 2: pmic_power.kicad_sch       (RK809-5, all rails, sequencing)
  |-- Sheet 3: lpddr4x.kicad_sch          (8GB LPDDR4X + decoupling)
  |-- Sheet 4: storage.kicad_sch          (eMMC, Micro SD, SPI NOR)
  |-- Sheet 5: usb_c_ports.kicad_sch      (3x USB-C, PD, mux, VL805)
  |-- Sheet 6: display.kicad_sch          (HDMI TX, eDP TX, IT6505, LT8711HE)
  |-- Sheet 7: ethernet_wifi.kicad_sch    (RTL8211F, RJ45, AP6256)
  |-- Sheet 8: gpio_misc.kicad_sch        (40-pin header, LEDs, buttons, debug)
```

## PCB Stackup (8-layer)

```
Layer 1: F.Cu    — Signal (top components, short traces)
Layer 2: In1.Cu  — GND plane (reference for L1)
Layer 3: In2.Cu  — Signal (DDR routing, inner traces)
Layer 4: In3.Cu  — Power plane (split: VCC_DDR, VDD_LOGIC, VCC_1V8)
Layer 5: In4.Cu  — Power plane (split: VCC_3V3, VCC_0V9, VCC_5V0)
Layer 6: In5.Cu  — Signal (DDR routing, inner traces)
Layer 7: In6.Cu  — GND plane (reference for L8)
Layer 8: B.Cu    — Signal (bottom components, short traces)
```

## Impedance Targets

| Type | Target | Used For |
|---|---|---|
| Single-ended | 50 ohm | GPIO, UART, SPI, I2C, misc |
| Differential 100 ohm | 100 ohm | USB3 SS, PCIe, eDP |
| Differential 85 ohm | 85 ohm | HDMI TMDS |
| Differential 80 ohm | 80 ohm | LPDDR4X DQ/CA (varies by stackup) |
