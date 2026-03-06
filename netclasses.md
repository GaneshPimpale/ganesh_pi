
All net classes for the RK3568 SBC ("Open Pi") project. Impedance targets verified against the RK3568 V2.1 datasheet (Tables 3-7 through 3-13) and standard interface specs (JEDEC, MIPI, HDMI, USB-IF, PCI-SIG).

Trace widths marked stackup-dependent must be calculated with an impedance calculator once the PCB stackup is finalized. Values below are starting points for a typical 6-layer 1.6mm stackup.

High-Speed Differential Pairs

Net Class Z_diff Trace W Spacing Clearance Datasheet Ref Patterns
DDR4_DQS 80Ω stackup stackup 0.15mm Table 3-8: Rtt 20–60Ω DDR_DQS
DDR4_CLK 80Ω stackup stackup 0.15mm Table 3-8: Rtt 20–60Ω DDR_CLK, DDR_CK
HDMI_TMDS 100Ω stackup stackup 0.20mm Table 3-12: TMDS spec HDMI_TX, HDMI_CLK, HDMI_D
MIPI_DSI0 100Ω stackup stackup 0.20mm Table 3-10: ZOS 40–62.5Ω DSI0, MIPI_DSI0, LVDS_TX0
MIPI_DSI1 100Ω stackup stackup 0.20mm Table 3-10: ZOS 40–62.5Ω DSI1, MIPI_DSI1, LVDS_TX1
MIPI_CSI 100Ω stackup stackup 0.20mm Table 3-11: D-PHY receiver CSI, MIPI_CSI
EDP 100Ω stackup stackup 0.20mm eDP 1.4 spec EDP, eDP
PCIE30 100Ω stackup stackup 0.20mm Table 3-13: RTX-DIFF-DC 80–120Ω PCIE30
PCIE20 100Ω stackup stackup 0.20mm Table 3-13: RTX-DIFF-DC 80–120Ω PCIE20, SATA, QSGMII
USB3_SS 100Ω stackup stackup 0.20mm Table 3-13: Multi-PHY 80–120Ω USB3_SS, USB_SS, SSRX, SSTX
USB2 90Ω stackup stackup 0.20mm Table 3-7: Rout 40.5–49.5Ω USB_DP, USB_DM, USB_D+, USB_D-, USB2
MULTI_PHY_CLK 100Ω stackup stackup 0.20mm Table 3-13: shared ref clocks MULTI_PHYCLK, REFCLK

Multi-PHY AC Coupling Capacitors (Table 3-13)

Interface AC Cap Value Notes
USB 3.0 / PCIe 2.1 75–200nF Per lane, series on TX
SATA 3.0 6–12nF Per lane, series on TX
PCIe 3.0 75–200nF Per lane, series on TX

High-Speed Single-Ended

Net Class Z_SE Trace W Clearance Datasheet Ref Patterns
DDR4_DATA 40Ω stackup 0.15mm Table 3-8: Rtt 20–60Ω DDR_DQ[0-9], DDR_DM
DDR4_ADDR 40Ω stackup 0.15mm Table 3-8: Rtt 20–60Ω DDR_A[0-9], DDR_BA, DDR_BG, DDR_RAS, DDR_CAS, DDR_WE, DDR_CS, DDR_CKE, DDR_ODT, DDR_RESET, DDR_ACT

Medium-Speed Single-Ended

Net Class Z_SE Trace W Clearance Patterns
EMMC 50Ω 0.15mm 0.15mm EMMC, eMMC
SDMMC 50Ω 0.15mm 0.15mm SDMMC, SDIO, SD_
GMAC 50Ω 0.15mm 0.15mm GMAC, RGMII, ETH, MDC, MDIO

Power Rails

Net Class Trace W Clearance Sch Wire Patterns Notes
PWR_CORE 0.40mm 0.20mm 16 mil VDD_CPU, VDD_GPU, VDD_LOGIC, VDD_NPU High-current switching regs
PWR_DDR 0.30mm 0.20mm 14 mil VCC_DDR, VDDQ, DDRPHYVDD DDR power + PHY
PWR_IO 0.30mm 0.20mm 12 mil VCCIO, PMUIO, VCC3V3 I/O bank supplies
PWR_ANALOG 0.25mm 0.25mm 12 mil AVDD, _AVDD_ Analog — isolate from switching noise

Power Rail Notes

PWR_CORE rails carry the highest current (VDD_CPU can peak >3A during turbo). Use copper pours where possible.
PWR_ANALOG nets need extra clearance (0.25mm) and must be routed away from high-speed digital and switching regulator traces.
All power traces should be as short and wide as physically possible.
Place decoupling caps within 2mm of their associated power pin.

Default Class

Net Class Trace W Clearance Sch Wire Covers
Default 0.15mm 0.15mm 6 mil GPIO, I2C, SPI, UART, JTAG, reset, interrupts, misc control

Length Matching Guidelines

Signal Group Match Within Max Length Notes
DDR4 DQ byte lane (DQ + DQS) ±5 mil 5000 mil Match per byte lane to its DQS
DDR4 Address/Command ±25 mil 6000 mil Match to CLK
DDR4 CLK pair ±2 mil — Intra-pair
HDMI TMDS lanes ±5 mil 4000 mil Match all 4 pairs (3 data + clk)
MIPI DSI/CSI lanes ±5 mil 3000 mil Match per interface
PCIe 3.0 TX/RX ±5 mil 6000 mil Intra-pair ±2 mil
PCIe 2.0 TX/RX ±5 mil 8000 mil Intra-pair ±2 mil
USB 3.0 SS TX/RX ±5 mil 4000 mil Intra-pair ±2 mil
USB 2.0 D+/D- ±10 mil 3000 mil —
eMMC data ±25 mil 2000 mil Match to CLK
RGMII TX group ±50 mil 4000 mil Match to TX_CLK
RGMII RX group ±50 mil 4000 mil Match to RX_CLK

Typical 6-Layer Stackup (1.6mm)

Layer Name Type Thickness Dielectric (Er)
1 F.Cu Signal 35µm (1oz) —
— Prepreg — 0.2mm 4.2
2 In1.Cu GND plane 35µm —
— Core — 0.8mm 4.5
3 In2.Cu Power plane 35µm —
— Prepreg — 0.2mm 4.2
4 B.Cu Signal 35µm (1oz) —

Calculated Trace Widths (Approximate — verify with fab stackup)

Target Impedance Trace Width Spacing (diff) Layer
40Ω SE (DDR) ~5.5 mil — L1/L4 over GND plane
50Ω SE ~4.0 mil — L1/L4 over GND plane
80Ω diff (DDR) ~4.0 mil 5.0 mil L1/L4 over GND plane
90Ω diff (USB2) ~4.0 mil 6.0 mil L1/L4 over GND plane
100Ω diff ~4.0 mil 7.0 mil L1/L4 over GND plane

⚠️ These are estimates. Final trace geometry must be calculated using the actual fab house stackup data and a 2D field solver (Saturn PCB Toolkit, KiCad calculator, or Si9000). Request the fab's impedance-controlled stackup spec before finalizing.

Schematic Color Coding

Color Family Net Classes
🔵 Blues DDR4_DATA, DDR4_DQS, DDR4_ADDR, DDR4_CLK
🟣 Purples/Pinks HDMI_TMDS, MIPI_DSI0, MIPI_DSI1, MIPI_CSI
🟠 Orange EDP
🔴 Reds PCIE30, PCIE20, USB3_SS, MULTI_PHY_CLK
🩷 Light Pink USB2
🟢 Greens EMMC, SDMMC, GMAC
🔴🟠🟡 Warm PWR_CORE, PWR_DDR, PWR_IO, PWR_ANALOG
