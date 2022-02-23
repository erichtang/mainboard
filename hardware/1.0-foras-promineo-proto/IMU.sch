EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 12 13
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 7100 6900 0    100  ~ 20
SLI IMU Additions
$Comp
L mainboard_SLI:IAM-20380 U204
U 1 1 619F3E6C
P 2600 1450
F 0 "U204" H 2550 1615 50  0000 C CNN
F 1 "IAM-20380" H 2550 1524 50  0000 C CNN
F 2 "mainboard-SLI:IAM-20380" H 2600 1450 50  0001 C CNN
F 3 "" H 2600 1450 50  0001 C CNN
	1    2600 1450
	1    0    0    -1  
$EndComp
$Comp
L mainboard_SLI:MMC5983MA U205
U 1 1 619F3E9E
P 4800 1450
F 0 "U205" H 4800 1615 50  0000 C CNN
F 1 "MMC5983MA" H 4800 1524 50  0000 C CNN
F 2 "mainboard-SLI:MMC5983MA" H 4800 1450 50  0001 C CNN
F 3 "" H 4800 1450 50  0001 C CNN
	1    4800 1450
	1    0    0    -1  
$EndComp
$Comp
L mainboard_SLI:MXC6655XA U206
U 1 1 619F3EA8
P 6600 1500
F 0 "U206" H 6600 1665 50  0000 C CNN
F 1 "MXC6655XA" H 6600 1574 50  0000 C CNN
F 2 "mainboard-SLI:MXC6655XA" H 6600 1500 50  0001 C CNN
F 3 "" H 6600 1500 50  0001 C CNN
	1    6600 1500
	1    0    0    -1  
$EndComp
Text Notes 6350 2400 0    50   ~ 0
accelerometer\naddress 0x15
Text Notes 4500 2450 0    50   ~ 0
magnetometer\naddress 0x30
Text Notes 2450 2700 0    50   ~ 0
gyroscope\nadress 0x69\nsa0 = high
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R238
U 1 1 61ADF556
P 5700 6300
F 0 "R238" H 5768 6346 50  0000 L CNN
F 1 "10k" H 5768 6255 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5740 6290 50  0001 C CNN
F 3 "~" H 5700 6300 50  0001 C CNN
	1    5700 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 6450 5700 6500
Wire Wire Line
	5700 5900 5700 6150
Wire Wire Line
	5700 6500 5750 6500
Text Label 5750 6500 0    50   ~ 0
SDA_IMU2
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61BAF3BA
P 950 1650
AR Path="/61BAF3BA" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61BAF3BA" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61BAF3BA" Ref="#SUPPLY0105"  Part="1" 
F 0 "#SUPPLY0105" H 950 1650 50  0001 C CNN
F 1 "3.3V" H 850 1800 59  0000 L BNN
F 2 "" H 950 1650 50  0001 C CNN
F 3 "" H 950 1650 50  0001 C CNN
	1    950  1650
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C224
U 1 1 61BAF3CE
P 1400 1900
F 0 "C224" H 1515 1946 50  0000 L CNN
F 1 "0.1uF" H 1515 1855 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1438 1750 50  0001 C CNN
F 3 "~" H 1400 1900 50  0001 C CNN
	1    1400 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 1700 1400 1750
$Comp
L mainboard:GND #GND?
U 1 1 61BAF3DB
P 1400 2150
AR Path="/61BAF3DB" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61BAF3DB" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61BAF3DB" Ref="#GND0132"  Part="1" 
F 0 "#GND0132" H 1400 2150 50  0001 C CNN
F 1 "GND" H 1300 2050 59  0000 L BNN
F 2 "" H 1400 2150 50  0001 C CNN
F 3 "" H 1400 2150 50  0001 C CNN
	1    1400 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	950  1700 1400 1700
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C223
U 1 1 61BB7045
P 950 1900
F 0 "C223" H 1065 1946 50  0000 L CNN
F 1 "2.2uF" H 1065 1855 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 988 1750 50  0001 C CNN
F 3 "~" H 950 1900 50  0001 C CNN
	1    950  1900
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61BB705E
P 950 2150
AR Path="/61BB705E" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61BB705E" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61BB705E" Ref="#GND0133"  Part="1" 
F 0 "#GND0133" H 950 2150 50  0001 C CNN
F 1 "GND" H 850 2050 59  0000 L BNN
F 2 "" H 950 2150 50  0001 C CNN
F 3 "" H 950 2150 50  0001 C CNN
	1    950  2150
	1    0    0    -1  
$EndComp
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61BC3DCE
P 1750 1050
AR Path="/61BC3DCE" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61BC3DCE" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61BC3DCE" Ref="#SUPPLY0106"  Part="1" 
F 0 "#SUPPLY0106" H 1750 1050 50  0001 C CNN
F 1 "3.3V" H 1650 1200 59  0000 L BNN
F 2 "" H 1750 1050 50  0001 C CNN
F 3 "" H 1750 1050 50  0001 C CNN
	1    1750 1050
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61BC3E04
P 1750 1550
AR Path="/61BC3E04" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61BC3E04" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61BC3E04" Ref="#GND0134"  Part="1" 
F 0 "#GND0134" H 1750 1550 50  0001 C CNN
F 1 "GND" H 1650 1450 59  0000 L BNN
F 2 "" H 1750 1550 50  0001 C CNN
F 3 "" H 1750 1550 50  0001 C CNN
	1    1750 1550
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C220
U 1 1 61BC3DF9
P 1750 1300
F 0 "C220" H 1865 1346 50  0000 L CNN
F 1 "10nF" H 1865 1255 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1788 1150 50  0001 C CNN
F 3 "~" H 1750 1300 50  0001 C CNN
	1    1750 1300
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 1600 2100 1600
Connection ~ 1400 1700
Wire Wire Line
	2200 1800 2100 1800
Wire Wire Line
	2100 1800 2100 1600
$Comp
L mainboard:GND #GND?
U 1 1 61BDC938
P 1800 2300
AR Path="/61BDC938" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61BDC938" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61BDC938" Ref="#GND0135"  Part="1" 
F 0 "#GND0135" H 1800 2300 50  0001 C CNN
F 1 "GND" H 1700 2200 59  0000 L BNN
F 2 "" H 1800 2300 50  0001 C CNN
F 3 "" H 1800 2300 50  0001 C CNN
	1    1800 2300
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C226
U 1 1 61BDC942
P 1800 2050
F 0 "C226" H 1915 2096 50  0000 L CNN
F 1 "0.47uF" H 1915 2005 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1838 1900 50  0001 C CNN
F 3 "~" H 1800 2050 50  0001 C CNN
	1    1800 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 1900 1800 1900
$Comp
L mainboard:GND #GND?
U 1 1 61BE26DB
P 2100 2400
AR Path="/61BE26DB" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61BE26DB" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61BE26DB" Ref="#GND0136"  Part="1" 
F 0 "#GND0136" H 2100 2400 50  0001 C CNN
F 1 "GND" H 2000 2300 59  0000 L BNN
F 2 "" H 2100 2400 50  0001 C CNN
F 3 "" H 2100 2400 50  0001 C CNN
	1    2100 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	2200 2200 2100 2200
Wire Wire Line
	2100 2200 2100 2300
Text Label 3000 1600 0    50   ~ 0
SCL_IMU1
Wire Wire Line
	2200 1700 1400 1700
Wire Wire Line
	950  1650 950  1700
Connection ~ 950  1700
Wire Wire Line
	950  1700 950  1750
Wire Wire Line
	1750 1050 1750 1100
Wire Wire Line
	1750 1100 2100 1100
Wire Wire Line
	2100 1100 2100 1600
Connection ~ 1750 1100
Wire Wire Line
	1750 1100 1750 1150
Connection ~ 2100 1600
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61C062E5
P 3500 1900
AR Path="/61C062E5" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61C062E5" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61C062E5" Ref="#SUPPLY0107"  Part="1" 
F 0 "#SUPPLY0107" H 3500 1900 50  0001 C CNN
F 1 "3.3V" H 3400 2050 59  0000 L BNN
F 2 "" H 3500 1900 50  0001 C CNN
F 3 "" H 3500 1900 50  0001 C CNN
	1    3500 1900
	1    0    0    -1  
$EndComp
Text Label 3000 1700 0    50   ~ 0
SDA_IMU1
Wire Wire Line
	3000 1900 3500 1900
$Comp
L mainboard:GND #GND?
U 1 1 61C2A6B9
P 3150 2200
AR Path="/61C2A6B9" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61C2A6B9" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61C2A6B9" Ref="#GND0137"  Part="1" 
F 0 "#GND0137" H 3150 2200 50  0001 C CNN
F 1 "GND" H 3050 2100 59  0000 L BNN
F 2 "" H 3150 2200 50  0001 C CNN
F 3 "" H 3150 2200 50  0001 C CNN
	1    3150 2200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 2100 3000 2100
Wire Wire Line
	3000 2000 3150 2000
Wire Wire Line
	3150 2000 3150 2100
Connection ~ 3150 2100
Text Label 5200 1600 0    50   ~ 0
SDA_IMU1
Text Label 5200 1700 0    50   ~ 0
SCL_IMU1
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61C4DE6E
P 3750 1550
AR Path="/61C4DE6E" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61C4DE6E" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61C4DE6E" Ref="#SUPPLY0108"  Part="1" 
F 0 "#SUPPLY0108" H 3750 1550 50  0001 C CNN
F 1 "3.3V" H 3650 1700 59  0000 L BNN
F 2 "" H 3750 1550 50  0001 C CNN
F 3 "" H 3750 1550 50  0001 C CNN
	1    3750 1550
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C221
U 1 1 61C51053
P 3750 1700
F 0 "C221" H 3865 1746 50  0000 L CNN
F 1 "1uF" H 3865 1655 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3788 1550 50  0001 C CNN
F 3 "~" H 3750 1700 50  0001 C CNN
	1    3750 1700
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61C5105D
P 3750 1950
AR Path="/61C5105D" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61C5105D" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61C5105D" Ref="#GND0138"  Part="1" 
F 0 "#GND0138" H 3750 1950 50  0001 C CNN
F 1 "GND" H 3650 1850 59  0000 L BNN
F 2 "" H 3750 1950 50  0001 C CNN
F 3 "" H 3750 1950 50  0001 C CNN
	1    3750 1950
	1    0    0    -1  
$EndComp
Connection ~ 3750 1550
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61C5A90D
P 5400 2000
AR Path="/61C5A90D" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61C5A90D" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61C5A90D" Ref="#SUPPLY0112"  Part="1" 
F 0 "#SUPPLY0112" H 5400 2000 50  0001 C CNN
F 1 "3.3V" H 5300 2150 59  0000 L BNN
F 2 "" H 5400 2000 50  0001 C CNN
F 3 "" H 5400 2000 50  0001 C CNN
	1    5400 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5200 2000 5400 2000
$Comp
L mainboard:GND #GND?
U 1 1 61C60C0D
P 4150 2350
AR Path="/61C60C0D" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61C60C0D" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61C60C0D" Ref="#GND0139"  Part="1" 
F 0 "#GND0139" H 4150 2350 50  0001 C CNN
F 1 "GND" H 4050 2250 59  0000 L BNN
F 2 "" H 4150 2350 50  0001 C CNN
F 3 "" H 4150 2350 50  0001 C CNN
	1    4150 2350
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C225
U 1 1 61C60C1F
P 4150 1950
F 0 "C225" H 4265 1996 50  0000 L CNN
F 1 "10uF" H 4265 1905 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4188 1800 50  0001 C CNN
F 3 "~" H 4150 1950 50  0001 C CNN
	1    4150 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 2100 4400 2100
Wire Wire Line
	4150 2100 4150 2250
Connection ~ 4150 2100
Wire Wire Line
	4150 1800 4150 1750
Wire Wire Line
	4150 1750 4400 1750
Wire Wire Line
	3750 1550 4350 1550
Wire Wire Line
	4400 1650 4350 1650
Wire Wire Line
	4350 1650 4350 1550
Connection ~ 4350 1550
Wire Wire Line
	4350 1550 4400 1550
NoConn ~ 5200 1900
NoConn ~ 5200 2100
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61CB3A6E
P 5850 1650
AR Path="/61CB3A6E" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61CB3A6E" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61CB3A6E" Ref="#SUPPLY0113"  Part="1" 
F 0 "#SUPPLY0113" H 5850 1650 50  0001 C CNN
F 1 "3.3V" H 5750 1800 59  0000 L BNN
F 2 "" H 5850 1650 50  0001 C CNN
F 3 "" H 5850 1650 50  0001 C CNN
	1    5850 1650
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61CB3A82
P 5850 2050
AR Path="/61CB3A82" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61CB3A82" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61CB3A82" Ref="#GND0140"  Part="1" 
F 0 "#GND0140" H 5850 2050 50  0001 C CNN
F 1 "GND" H 5750 1950 59  0000 L BNN
F 2 "" H 5850 2050 50  0001 C CNN
F 3 "" H 5850 2050 50  0001 C CNN
	1    5850 2050
	1    0    0    -1  
$EndComp
Connection ~ 5850 1650
Wire Wire Line
	5850 1650 6200 1650
Wire Wire Line
	6200 1900 6200 1950
Wire Wire Line
	6200 1950 5850 1950
Connection ~ 5850 1950
Text Label 7000 1750 0    50   ~ 0
SDA_IMU1
Text Label 7000 1650 0    50   ~ 0
SCL_IMU1
NoConn ~ 7000 1900
Text Notes 2400 900  0    100  ~ 20
IMU Block #1
$Comp
L mainboard_SLI:IAM-20380 U207
U 1 1 61D51E7C
P 2550 3750
F 0 "U207" H 2500 3915 50  0000 C CNN
F 1 "IAM-20380" H 2500 3824 50  0000 C CNN
F 2 "mainboard-SLI:IAM-20380" H 2550 3750 50  0001 C CNN
F 3 "" H 2550 3750 50  0001 C CNN
	1    2550 3750
	1    0    0    -1  
$EndComp
$Comp
L mainboard_SLI:MMC5983MA U208
U 1 1 61D51E86
P 4750 3750
F 0 "U208" H 4750 3915 50  0000 C CNN
F 1 "MMC5983MA" H 4750 3824 50  0000 C CNN
F 2 "mainboard-SLI:MMC5983MA" H 4750 3750 50  0001 C CNN
F 3 "" H 4750 3750 50  0001 C CNN
	1    4750 3750
	1    0    0    -1  
$EndComp
$Comp
L mainboard_SLI:MXC6655XA U209
U 1 1 61D51E90
P 6550 3800
F 0 "U209" H 6550 3965 50  0000 C CNN
F 1 "MXC6655XA" H 6550 3874 50  0000 C CNN
F 2 "mainboard-SLI:MXC6655XA" H 6550 3800 50  0001 C CNN
F 3 "" H 6550 3800 50  0001 C CNN
	1    6550 3800
	1    0    0    -1  
$EndComp
Text Notes 6250 4550 0    50   ~ 0
accelerometer\naddress 0x15
Text Notes 4450 4750 0    50   ~ 0
magnetometer\naddress 0x30
Text Notes 2400 5000 0    50   ~ 0
gyroscope\nadress 0x69\nsa0 = high
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51E9D
P 900 3950
AR Path="/61D51E9D" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51E9D" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51E9D" Ref="#SUPPLY0114"  Part="1" 
F 0 "#SUPPLY0114" H 900 3950 50  0001 C CNN
F 1 "3.3V" H 800 4100 59  0000 L BNN
F 2 "" H 900 3950 50  0001 C CNN
F 3 "" H 900 3950 50  0001 C CNN
	1    900  3950
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C231
U 1 1 61D51EA7
P 1350 4200
F 0 "C231" H 1465 4246 50  0000 L CNN
F 1 "0.1uF" H 1465 4155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1388 4050 50  0001 C CNN
F 3 "~" H 1350 4200 50  0001 C CNN
	1    1350 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 4000 1350 4050
$Comp
L mainboard:GND #GND?
U 1 1 61D51EB2
P 1350 4450
AR Path="/61D51EB2" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51EB2" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51EB2" Ref="#GND0141"  Part="1" 
F 0 "#GND0141" H 1350 4450 50  0001 C CNN
F 1 "GND" H 1250 4350 59  0000 L BNN
F 2 "" H 1350 4450 50  0001 C CNN
F 3 "" H 1350 4450 50  0001 C CNN
	1    1350 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	900  4000 1350 4000
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C230
U 1 1 61D51EBD
P 900 4200
F 0 "C230" H 1015 4246 50  0000 L CNN
F 1 "2.2uF" H 1015 4155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 938 4050 50  0001 C CNN
F 3 "~" H 900 4200 50  0001 C CNN
	1    900  4200
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61D51EC7
P 900 4450
AR Path="/61D51EC7" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51EC7" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51EC7" Ref="#GND0142"  Part="1" 
F 0 "#GND0142" H 900 4450 50  0001 C CNN
F 1 "GND" H 800 4350 59  0000 L BNN
F 2 "" H 900 4450 50  0001 C CNN
F 3 "" H 900 4450 50  0001 C CNN
	1    900  4450
	1    0    0    -1  
$EndComp
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51ED1
P 1700 3350
AR Path="/61D51ED1" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51ED1" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51ED1" Ref="#SUPPLY0119"  Part="1" 
F 0 "#SUPPLY0119" H 1700 3350 50  0001 C CNN
F 1 "3.3V" H 1600 3500 59  0000 L BNN
F 2 "" H 1700 3350 50  0001 C CNN
F 3 "" H 1700 3350 50  0001 C CNN
	1    1700 3350
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61D51EDB
P 1700 3850
AR Path="/61D51EDB" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51EDB" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51EDB" Ref="#GND0143"  Part="1" 
F 0 "#GND0143" H 1700 3850 50  0001 C CNN
F 1 "GND" H 1600 3750 59  0000 L BNN
F 2 "" H 1700 3850 50  0001 C CNN
F 3 "" H 1700 3850 50  0001 C CNN
	1    1700 3850
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C227
U 1 1 61D51EE5
P 1700 3600
F 0 "C227" H 1815 3646 50  0000 L CNN
F 1 "10nF" H 1815 3555 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1738 3450 50  0001 C CNN
F 3 "~" H 1700 3600 50  0001 C CNN
	1    1700 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 3900 2050 3900
Connection ~ 1350 4000
Wire Wire Line
	2150 4100 2050 4100
Wire Wire Line
	2050 4100 2050 3900
$Comp
L mainboard:GND #GND?
U 1 1 61D51EF3
P 1750 4600
AR Path="/61D51EF3" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51EF3" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51EF3" Ref="#GND0144"  Part="1" 
F 0 "#GND0144" H 1750 4600 50  0001 C CNN
F 1 "GND" H 1650 4500 59  0000 L BNN
F 2 "" H 1750 4600 50  0001 C CNN
F 3 "" H 1750 4600 50  0001 C CNN
	1    1750 4600
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C233
U 1 1 61D51EFD
P 1750 4350
F 0 "C233" H 1865 4396 50  0000 L CNN
F 1 "0.47uF" H 1865 4305 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1788 4200 50  0001 C CNN
F 3 "~" H 1750 4350 50  0001 C CNN
	1    1750 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 4200 1750 4200
$Comp
L mainboard:GND #GND?
U 1 1 61D51F08
P 2050 4700
AR Path="/61D51F08" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51F08" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51F08" Ref="#GND0145"  Part="1" 
F 0 "#GND0145" H 2050 4700 50  0001 C CNN
F 1 "GND" H 1950 4600 59  0000 L BNN
F 2 "" H 2050 4700 50  0001 C CNN
F 3 "" H 2050 4700 50  0001 C CNN
	1    2050 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 4500 2050 4500
Wire Wire Line
	2050 4500 2050 4600
Text Label 2950 3900 0    50   ~ 0
SCL_IMU2
Wire Wire Line
	2150 4000 1350 4000
Wire Wire Line
	900  3950 900  4000
Connection ~ 900  4000
Wire Wire Line
	900  4000 900  4050
Wire Wire Line
	1700 3350 1700 3400
Wire Wire Line
	1700 3400 2050 3400
Wire Wire Line
	2050 3400 2050 3900
Connection ~ 1700 3400
Wire Wire Line
	1700 3400 1700 3450
Connection ~ 2050 3900
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51F1F
P 3450 4200
AR Path="/61D51F1F" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51F1F" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51F1F" Ref="#SUPPLY0120"  Part="1" 
F 0 "#SUPPLY0120" H 3450 4200 50  0001 C CNN
F 1 "3.3V" H 3350 4350 59  0000 L BNN
F 2 "" H 3450 4200 50  0001 C CNN
F 3 "" H 3450 4200 50  0001 C CNN
	1    3450 4200
	1    0    0    -1  
$EndComp
Text Label 2950 4000 0    50   ~ 0
SDA_IMU2
Wire Wire Line
	2950 4200 3450 4200
$Comp
L mainboard:GND #GND?
U 1 1 61D51F2B
P 3100 4500
AR Path="/61D51F2B" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51F2B" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51F2B" Ref="#GND0146"  Part="1" 
F 0 "#GND0146" H 3100 4500 50  0001 C CNN
F 1 "GND" H 3000 4400 59  0000 L BNN
F 2 "" H 3100 4500 50  0001 C CNN
F 3 "" H 3100 4500 50  0001 C CNN
	1    3100 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 4400 2950 4400
Wire Wire Line
	2950 4300 3100 4300
Wire Wire Line
	3100 4300 3100 4400
Connection ~ 3100 4400
Text Label 5150 3900 0    50   ~ 0
SDA_IMU2
Text Label 5150 4000 0    50   ~ 0
SCL_IMU2
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51F3B
P 3700 3850
AR Path="/61D51F3B" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51F3B" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51F3B" Ref="#SUPPLY0121"  Part="1" 
F 0 "#SUPPLY0121" H 3700 3850 50  0001 C CNN
F 1 "3.3V" H 3600 4000 59  0000 L BNN
F 2 "" H 3700 3850 50  0001 C CNN
F 3 "" H 3700 3850 50  0001 C CNN
	1    3700 3850
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C228
U 1 1 61D51F45
P 3700 4000
F 0 "C228" H 3815 4046 50  0000 L CNN
F 1 "1uF" H 3815 3955 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3738 3850 50  0001 C CNN
F 3 "~" H 3700 4000 50  0001 C CNN
	1    3700 4000
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61D51F4F
P 3700 4250
AR Path="/61D51F4F" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51F4F" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51F4F" Ref="#GND0147"  Part="1" 
F 0 "#GND0147" H 3700 4250 50  0001 C CNN
F 1 "GND" H 3600 4150 59  0000 L BNN
F 2 "" H 3700 4250 50  0001 C CNN
F 3 "" H 3700 4250 50  0001 C CNN
	1    3700 4250
	1    0    0    -1  
$EndComp
Connection ~ 3700 3850
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51F5A
P 5350 4300
AR Path="/61D51F5A" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51F5A" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51F5A" Ref="#SUPPLY0122"  Part="1" 
F 0 "#SUPPLY0122" H 5350 4300 50  0001 C CNN
F 1 "3.3V" H 5250 4450 59  0000 L BNN
F 2 "" H 5350 4300 50  0001 C CNN
F 3 "" H 5350 4300 50  0001 C CNN
	1    5350 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5150 4300 5350 4300
$Comp
L mainboard:GND #GND?
U 1 1 61D51F65
P 4100 4650
AR Path="/61D51F65" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51F65" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51F65" Ref="#GND0148"  Part="1" 
F 0 "#GND0148" H 4100 4650 50  0001 C CNN
F 1 "GND" H 4000 4550 59  0000 L BNN
F 2 "" H 4100 4650 50  0001 C CNN
F 3 "" H 4100 4650 50  0001 C CNN
	1    4100 4650
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C232
U 1 1 61D51F6F
P 4100 4250
F 0 "C232" H 4215 4296 50  0000 L CNN
F 1 "10uF" H 4215 4205 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4138 4100 50  0001 C CNN
F 3 "~" H 4100 4250 50  0001 C CNN
	1    4100 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 4400 4350 4400
Wire Wire Line
	4100 4400 4100 4550
Connection ~ 4100 4400
Wire Wire Line
	4100 4100 4100 4050
Wire Wire Line
	4100 4050 4350 4050
Wire Wire Line
	3700 3850 4300 3850
Wire Wire Line
	4350 3950 4300 3950
Wire Wire Line
	4300 3950 4300 3850
Connection ~ 4300 3850
Wire Wire Line
	4300 3850 4350 3850
NoConn ~ 5150 4200
NoConn ~ 5150 4400
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61D51F85
P 5800 3950
AR Path="/61D51F85" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61D51F85" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61D51F85" Ref="#SUPPLY0123"  Part="1" 
F 0 "#SUPPLY0123" H 5800 3950 50  0001 C CNN
F 1 "3.3V" H 5700 4100 59  0000 L BNN
F 2 "" H 5800 3950 50  0001 C CNN
F 3 "" H 5800 3950 50  0001 C CNN
	1    5800 3950
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C229
U 1 1 61D51F8F
P 5800 4100
F 0 "C229" H 5915 4146 50  0000 L CNN
F 1 "1uF" H 5915 4055 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5838 3950 50  0001 C CNN
F 3 "~" H 5800 4100 50  0001 C CNN
	1    5800 4100
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61D51F99
P 5800 4350
AR Path="/61D51F99" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61D51F99" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61D51F99" Ref="#GND0149"  Part="1" 
F 0 "#GND0149" H 5800 4350 50  0001 C CNN
F 1 "GND" H 5700 4250 59  0000 L BNN
F 2 "" H 5800 4350 50  0001 C CNN
F 3 "" H 5800 4350 50  0001 C CNN
	1    5800 4350
	1    0    0    -1  
$EndComp
Connection ~ 5800 3950
Wire Wire Line
	5800 3950 6150 3950
Wire Wire Line
	6150 4200 6150 4250
Wire Wire Line
	6150 4250 5800 4250
Connection ~ 5800 4250
Text Label 6950 4050 0    50   ~ 0
SDA_IMU2
Text Label 6950 3950 0    50   ~ 0
SCL_IMU2
NoConn ~ 6950 4200
Text Notes 2350 3200 0    100  ~ 20
IMU Block #2
Connection ~ 5700 6500
Wire Wire Line
	1250 6100 1850 6100
Connection ~ 1250 6100
Wire Wire Line
	1850 6700 2900 6700
Wire Wire Line
	1850 6100 2050 6100
Connection ~ 1850 6100
Text Notes 1750 5850 0    100  ~ 20
I2C MUX
Wire Wire Line
	5700 6500 3900 6500
Connection ~ 5400 6600
Wire Wire Line
	3900 6600 5400 6600
Wire Wire Line
	3900 6700 5100 6700
Text Label 4650 6100 0    50   ~ 0
SDA_IMU1
Wire Wire Line
	3900 6200 4300 6200
Wire Wire Line
	3900 6100 4600 6100
Text Label 5450 6600 0    50   ~ 0
SCL_IMU2
Text Label 4350 6200 0    50   ~ 0
SCL_IMU1
Wire Wire Line
	5400 6600 5450 6600
Wire Wire Line
	5400 5900 5400 5850
Wire Wire Line
	5400 5900 5100 5900
Connection ~ 5400 5900
Wire Wire Line
	5400 6050 5400 5900
Wire Wire Line
	5100 5900 5100 5950
Wire Wire Line
	5700 5900 5400 5900
$Comp
L mainboard:3.3V #P+?
U 1 1 61B34D4B
P 5400 5850
AR Path="/5EDE7915/61B34D4B" Ref="#P+?"  Part="1" 
AR Path="/61A43B3F/61B34D4B" Ref="#P+0107"  Part="1" 
F 0 "#P+0107" H 5400 5850 50  0001 C CNN
F 1 "3.3V" H 5400 6000 59  0000 C CNN
F 2 "" H 5400 5850 50  0001 C CNN
F 3 "" H 5400 5850 50  0001 C CNN
	1    5400 5850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 6350 5400 6600
Wire Wire Line
	5100 6250 5100 6700
Connection ~ 4600 6100
Wire Wire Line
	4600 6100 4650 6100
Connection ~ 4300 6200
Wire Wire Line
	4300 6200 4350 6200
Wire Wire Line
	4600 6100 4600 6050
Wire Wire Line
	4300 6200 4300 5950
Wire Wire Line
	4000 6300 4000 5850
Wire Wire Line
	4600 5500 4600 5750
Wire Wire Line
	4000 6300 3900 6300
Wire Wire Line
	4300 5500 4300 5450
Wire Wire Line
	4300 5500 4000 5500
Connection ~ 4300 5500
Wire Wire Line
	4300 5650 4300 5500
Wire Wire Line
	4000 5500 4000 5550
Wire Wire Line
	4600 5500 4300 5500
$Comp
L mainboard:3.3V #P+?
U 1 1 61AF1A8C
P 4300 5450
AR Path="/5EDE7915/61AF1A8C" Ref="#P+?"  Part="1" 
AR Path="/61A43B3F/61AF1A8C" Ref="#P+0108"  Part="1" 
F 0 "#P+0108" H 4300 5450 50  0001 C CNN
F 1 "3.3V" H 4300 5600 59  0000 C CNN
F 2 "" H 4300 5450 50  0001 C CNN
F 3 "" H 4300 5450 50  0001 C CNN
	1    4300 5450
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R235
U 1 1 61ADF54B
P 5400 6200
F 0 "R235" H 5468 6246 50  0000 L CNN
F 1 "10k" H 5468 6155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5440 6190 50  0001 C CNN
F 3 "~" H 5400 6200 50  0001 C CNN
	1    5400 6200
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R234
U 1 1 61ADF52C
P 5100 6100
F 0 "R234" H 5168 6146 50  0000 L CNN
F 1 "100k" H 5168 6055 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5140 6090 50  0001 C CNN
F 3 "~" H 5100 6100 50  0001 C CNN
	1    5100 6100
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R231
U 1 1 61ADCB43
P 4600 5900
F 0 "R231" H 4668 5946 50  0000 L CNN
F 1 "10k" H 4668 5855 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4640 5890 50  0001 C CNN
F 3 "~" H 4600 5900 50  0001 C CNN
	1    4600 5900
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R230
U 1 1 61ADB40C
P 4300 5800
F 0 "R230" H 4368 5846 50  0000 L CNN
F 1 "10k" H 4368 5755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4340 5790 50  0001 C CNN
F 3 "~" H 4300 5800 50  0001 C CNN
	1    4300 5800
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R229
U 1 1 61AD8E9B
P 4000 5700
F 0 "R229" H 4068 5746 50  0000 L CNN
F 1 "100k" H 4068 5655 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4040 5690 50  0001 C CNN
F 3 "~" H 4000 5700 50  0001 C CNN
	1    4000 5700
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 6500 1850 6700
Wire Wire Line
	1850 6200 1850 6100
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R239
U 1 1 61A2CEE1
P 1850 6350
F 0 "R239" H 1600 6400 50  0000 L CNN
F 1 "100k" H 1600 6300 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1890 6340 50  0001 C CNN
F 3 "~" H 1850 6350 50  0001 C CNN
	1    1850 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 6600 2050 6500
Wire Wire Line
	2050 6200 2050 6100
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R240
U 1 1 61A2609B
P 2050 6350
F 0 "R240" H 2118 6396 50  0000 L CNN
F 1 "100k" H 2118 6305 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2090 6340 50  0001 C CNN
F 3 "~" H 2050 6350 50  0001 C CNN
	1    2050 6350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 6500 2900 6500
Wire Wire Line
	2900 6400 2800 6400
Wire Wire Line
	2900 7000 2800 7000
Wire Wire Line
	2800 7000 2800 7100
$Comp
L mainboard:GND #GND?
U 1 1 61A0FB3A
P 2800 7200
AR Path="/61A0FB3A" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61A0FB3A" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61A0FB3A" Ref="#GND0152"  Part="1" 
F 0 "#GND0152" H 2800 7200 50  0001 C CNN
F 1 "GND" H 2700 7100 59  0000 L BNN
F 2 "" H 2800 7200 50  0001 C CNN
F 3 "" H 2800 7200 50  0001 C CNN
	1    2800 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 7000 4050 7100
Connection ~ 4050 7000
Wire Wire Line
	4050 7000 3900 7000
Wire Wire Line
	4050 6900 4050 7000
Wire Wire Line
	3900 6900 4050 6900
$Comp
L mainboard:GND #GND?
U 1 1 61A0EB9F
P 4050 7200
AR Path="/61A0EB9F" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61A0EB9F" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61A0EB9F" Ref="#GND0153"  Part="1" 
F 0 "#GND0153" H 4050 7200 50  0001 C CNN
F 1 "GND" H 3950 7100 59  0000 L BNN
F 2 "" H 4050 7200 50  0001 C CNN
F 3 "" H 4050 7200 50  0001 C CNN
	1    4050 7200
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND?
U 1 1 61A0E7F3
P 1250 6500
AR Path="/61A0E7F3" Ref="#GND?"  Part="1" 
AR Path="/5CEC5A72/61A0E7F3" Ref="#GND?"  Part="1" 
AR Path="/61A43B3F/61A0E7F3" Ref="#GND0154"  Part="1" 
F 0 "#GND0154" H 1250 6500 50  0001 C CNN
F 1 "GND" H 1150 6400 59  0000 L BNN
F 2 "" H 1250 6500 50  0001 C CNN
F 3 "" H 1250 6500 50  0001 C CNN
	1    1250 6500
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C217
U 1 1 61A09170
P 1250 6250
F 0 "C217" H 1365 6296 50  0000 L CNN
F 1 "0.1uF" H 1365 6205 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1288 6100 50  0001 C CNN
F 3 "~" H 1250 6250 50  0001 C CNN
	1    1250 6250
	1    0    0    -1  
$EndComp
$Comp
L mainboard:3.3V #SUPPLY?
U 1 1 61A09054
P 1250 6100
AR Path="/61A09054" Ref="#SUPPLY?"  Part="1" 
AR Path="/5CEC5A72/61A09054" Ref="#SUPPLY?"  Part="1" 
AR Path="/61A43B3F/61A09054" Ref="#SUPPLY0124"  Part="1" 
F 0 "#SUPPLY0124" H 1250 6100 50  0001 C CNN
F 1 "3.3V" H 1150 6250 59  0000 L BNN
F 2 "" H 1250 6100 50  0001 C CNN
F 3 "" H 1250 6100 50  0001 C CNN
	1    1250 6100
	1    0    0    -1  
$EndComp
$Comp
L mainboard_SLI:PCA9543APW,118 U201
U 1 1 61A9C131
P 3450 6000
F 0 "U201" H 3400 6167 50  0000 C CNN
F 1 "PCA9543APW,118" H 3400 6076 50  0000 C CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 4400 4350 50  0001 C CNN
F 3 "http://www.nxp.com/documents/data_sheet/PCA9544A.pdf" H 3200 4100 50  0001 C CNN
	1    3450 6000
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C222
U 1 1 61CB3A78
P 5850 1800
F 0 "C222" H 5965 1846 50  0000 L CNN
F 1 "1uF" H 5965 1755 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5888 1650 50  0001 C CNN
F 3 "~" H 5850 1800 50  0001 C CNN
	1    5850 1800
	1    0    0    -1  
$EndComp
Text Notes 3000 7350 0    50   ~ 0
i2c mux addr = 0x70
Connection ~ 2050 6100
Wire Wire Line
	2050 6100 2900 6100
Wire Wire Line
	2050 6600 2900 6600
Text GLabel 2800 6500 0    50   Output ~ 0
SCL_IMU
Text GLabel 2800 6400 0    50   BiDi ~ 0
SDA_IMU
Text Notes 6050 3500 0    50   ~ 0
DNI U209\nOnly one accel is needed
$EndSCHEMATC
