# Parts Inventory — Library Status

## In Project Libraries (ready to place)

| # | Part | lib_id | Pins | Function |
|---|---|---|---|---|
| 1 | RK3568 | RK3568:RK3568 | 636 | SoC |
| 2 | RK809-5 | RK809-5:RK809-5 | 69 | PMIC |
| 3 | K4UBE3D4AA-MGCL | K4UBE3D4AA-MGCL:K4UBE3D4AA-MGCL | 200 | 8GB LPDDR4X |
| 4 | KLMBG2JETD-B041 | KLMBG2JETD-B041:KLMBG2JETD-B041 | 153 | 32GB eMMC |
| 5 | LT8711HE | LT8711HE:LT8711HE | 65 | HDMI -> DP converter |
| 6 | LT6711A | LT6711A:LT6711A | 65 | Display converter (alt) |
| 7 | TUSB1064RNQT | TUSB1064RNQT:TUSB1064RNQT | 41 | USB-C DP Alt Mode mux |
| 8 | FUSB302BUCX | FUSB302BUCX:FUSB302BUCX | 9 | USB PD controller |
| 9 | VL805 | VL805:VL805 | 69 | PCIe -> USB3 hub |
| 10 | AP6256 | AP6256:AP6256 | 47 | WiFi 5 + BT 5.0 |
| 11 | HD3SS215RTQR | HD3SS215RTQR:HD3SS215RTQR | 57 | USB SS switch (bonus) |
| 12 | NCP380HMU05AATBG | NCP380HMU05AATBG:NCP380HMU05AATBG | 7 | USB VBUS load switch |

### Also in libraries but NOT usable:
- K4UBE3D4AB-MGCL — broken symbol (0 pins, empty)
- K4FBE3D4HM-MGCJ — EasyEDA format (.elibz), not native KiCad
- K4UCE3Q4AB-MGCL — 16GB LPDDR4X, 200 pins (usable but not needed for 8GB)

## In KiCad Built-in Libraries (ready to place)

| # | Part | lib_id | Pins | Function |
|---|---|---|---|---|
| 13 | W25Q128JVS | Memory_Flash:W25Q128JVS | 8 | 16MB SPI NOR (bootloader) |
| 14 | USB-C connector | Connector:USB_C_Receptacle | 25 | USB Type-C full-featured |
| 15 | 40-pin GPIO header | Connector_Generic:Conn_02x20_Odd_Even | 40 | Pi-compatible GPIO |
| 16 | USBLC6-2SC6 | Power_Protection:USBLC6-2SC6 | 6 | USB ESD protection |
| 17 | Crystal | Device:Crystal | 2 | Oscillator crystals |
| 18 | Passives | Device:R, Device:C, Device:L | 2 | Resistors, caps, inductors |
| 19 | Power symbols | power:GND, power:+3V3, etc. | 1 | Power rails |
| 20 | RTL8211EG | Interface_Ethernet:RTL8211EG-VB-CG | 65 | GbE PHY (alt to RTL8211F) |

## Still Needs Importing

| Part | Needed For | Action |
|---|---|---|
| IT6505FN | eDP -> DP converter | Search JLCPCB/Mouser, import or generate |
| RTL8211F-CG | GbE PHY (preferred) | Search JLCPCB; fallback: use RTL8211EG from KiCad |
| SY8088AAC | 1.0V buck for VL805 | Search JLCPCB/Mouser |
| AP2112K-3.3 | LDO 3.3V | Search JLCPCB/Mouser |
| PRTR5V0U2X | ESD for display lines | Search KiCad built-in or JLCPCB |
| Micro SD connector | SD card slot | Search KiCad built-in (Connector:) |

## Notes
- NCP380HMU05AATBG replaces the NCP45520 in original spec (same function, available)
- HD3SS215RTQR is an extra USB SS switch — may be useful for USB-C muxing
- K4UBE3D4AA-MGCL is confirmed 8GB LPDDR4X with working 200-pin symbol
- spec_and_bom.md updated to match actual available part numbers
