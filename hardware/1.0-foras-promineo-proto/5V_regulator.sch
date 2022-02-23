EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 11 13
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L mainboard_SLI:TPS63070 U203
U 1 1 61ABDC6E
P 6150 2300
AR Path="/6186D6EC/62382E1E/61ABDC6E" Ref="U203"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ABDC6E" Ref="U210"  Part="1" 
AR Path="/63E462C7/62382E1E/61ABDC6E" Ref="U?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ABDC6E" Ref="U?"  Part="1" 
F 0 "U210" H 6150 2967 50  0000 C CNN
F 1 "TPS63070" H 6150 2876 50  0000 C CNN
F 2 "mainboard-SLI:TPS63070RNMR" H 6200 1250 50  0001 C CNN
F 3 "" H 6150 2300 50  0001 C CNN
	1    6150 2300
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R228
U 1 1 61ABE86A
P 3850 3500
AR Path="/6186D6EC/62382E1E/61ABE86A" Ref="R228"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ABE86A" Ref="R255"  Part="1" 
AR Path="/63E462C7/62382E1E/61ABE86A" Ref="R?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ABE86A" Ref="R?"  Part="1" 
F 0 "R255" H 3918 3546 50  0000 L CNN
F 1 "330k" H 3918 3455 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3890 3490 50  0001 C CNN
F 3 "~" H 3850 3500 50  0001 C CNN
	1    3850 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 1900 5650 1900
Wire Wire Line
	5750 2650 5650 2650
Connection ~ 5650 1900
$Comp
L mainboard:GND #GND0118
U 1 1 61AC091D
P 5000 2900
AR Path="/6186D6EC/62382E1E/61AC091D" Ref="#GND0118"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AC091D" Ref="#GND0159"  Part="1" 
AR Path="/63E462C7/62382E1E/61AC091D" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AC091D" Ref="#GND?"  Part="1" 
F 0 "#GND0159" H 5000 2900 50  0001 C CNN
F 1 "GND" H 5000 2779 59  0000 C CNN
F 2 "" H 5000 2900 50  0001 C CNN
F 3 "" H 5000 2900 50  0001 C CNN
	1    5000 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	5650 1900 5650 2650
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C216
U 1 1 61AC7EDC
P 5000 2650
AR Path="/6186D6EC/62382E1E/61AC7EDC" Ref="C216"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AC7EDC" Ref="C241"  Part="1" 
AR Path="/63E462C7/62382E1E/61AC7EDC" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AC7EDC" Ref="C?"  Part="1" 
F 0 "C241" H 4885 2604 50  0000 R CNN
F 1 "0.1uF" H 4885 2695 50  0000 R CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5038 2500 50  0001 C CNN
F 3 "~" H 5000 2650 50  0001 C CNN
	1    5000 2650
	-1   0    0    1   
$EndComp
Wire Wire Line
	5000 2500 5750 2500
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C212
U 1 1 61ACB128
P 4550 2100
AR Path="/6186D6EC/62382E1E/61ACB128" Ref="C212"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ACB128" Ref="C237"  Part="1" 
AR Path="/63E462C7/62382E1E/61ACB128" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ACB128" Ref="C?"  Part="1" 
F 0 "C237" H 4665 2146 50  0000 L CNN
F 1 "10uF" H 4665 2055 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4588 1950 50  0001 C CNN
F 3 "~" H 4550 2100 50  0001 C CNN
	1    4550 2100
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C211
U 1 1 61ACCF47
P 4100 2100
AR Path="/6186D6EC/62382E1E/61ACCF47" Ref="C211"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ACCF47" Ref="C236"  Part="1" 
AR Path="/63E462C7/62382E1E/61ACCF47" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ACCF47" Ref="C?"  Part="1" 
F 0 "C236" H 4215 2146 50  0000 L CNN
F 1 "10uF" H 4215 2055 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4138 1950 50  0001 C CNN
F 3 "~" H 4100 2100 50  0001 C CNN
	1    4100 2100
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C210
U 1 1 61ACD407
P 3650 2100
AR Path="/6186D6EC/62382E1E/61ACD407" Ref="C210"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ACD407" Ref="C235"  Part="1" 
AR Path="/63E462C7/62382E1E/61ACD407" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ACD407" Ref="C?"  Part="1" 
F 0 "C235" H 3765 2146 50  0000 L CNN
F 1 "10uF" H 3765 2055 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 3688 1950 50  0001 C CNN
F 3 "~" H 3650 2100 50  0001 C CNN
	1    3650 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 1950 3650 1900
Wire Wire Line
	4100 1950 4100 1900
Connection ~ 4100 1900
Wire Wire Line
	4100 1900 3650 1900
Wire Wire Line
	4550 1950 4550 1900
Connection ~ 4550 1900
Wire Wire Line
	4550 1900 4100 1900
Wire Wire Line
	4550 2300 4550 2250
Wire Wire Line
	4100 2250 4100 2300
Connection ~ 4100 2300
Wire Wire Line
	4100 2300 4550 2300
Wire Wire Line
	3650 2250 3650 2300
Wire Wire Line
	3650 2300 3900 2300
$Comp
L mainboard:GND #GND0119
U 1 1 61ACF6A4
P 3900 2400
AR Path="/6186D6EC/62382E1E/61ACF6A4" Ref="#GND0119"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ACF6A4" Ref="#GND0160"  Part="1" 
AR Path="/63E462C7/62382E1E/61ACF6A4" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ACF6A4" Ref="#GND?"  Part="1" 
F 0 "#GND0160" H 3900 2400 50  0001 C CNN
F 1 "GND" H 3900 2279 59  0000 C CNN
F 2 "" H 3900 2400 50  0001 C CNN
F 3 "" H 3900 2400 50  0001 C CNN
	1    3900 2400
	1    0    0    -1  
$EndComp
Connection ~ 3900 2300
Wire Wire Line
	3900 2300 4100 2300
$Comp
L mainboard:GND #GND0125
U 1 1 61AD08E2
P 4700 2500
AR Path="/6186D6EC/62382E1E/61AD08E2" Ref="#GND0125"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AD08E2" Ref="#GND0161"  Part="1" 
AR Path="/63E462C7/62382E1E/61AD08E2" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AD08E2" Ref="#GND?"  Part="1" 
F 0 "#GND0161" H 4700 2500 50  0001 C CNN
F 1 "GND" H 4700 2379 59  0000 C CNN
F 2 "" H 4700 2500 50  0001 C CNN
F 3 "" H 4700 2500 50  0001 C CNN
	1    4700 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 2350 4700 2400
Wire Wire Line
	4700 2350 5750 2350
$Comp
L mainboard-rescue:L-Device-mainboard-rescue L201
U 1 1 61ADA38D
P 6700 2050
AR Path="/6186D6EC/62382E1E/61ADA38D" Ref="L201"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ADA38D" Ref="L202"  Part="1" 
AR Path="/63E462C7/62382E1E/61ADA38D" Ref="L?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ADA38D" Ref="L?"  Part="1" 
F 0 "L202" H 6753 2096 50  0000 L CNN
F 1 "1.5uH" H 6753 2005 50  0000 L CNN
F 2 "Inductor_SMD:L_Bourns_SRN8040TA" H 6700 2050 50  0001 C CNN
F 3 "SRN8040TA-1R5Y" H 6700 2050 50  0001 C CNN
	1    6700 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6550 1900 6700 1900
Wire Wire Line
	6700 2200 6700 2250
Wire Wire Line
	6700 2250 6550 2250
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R224
U 1 1 61ADD72F
P 7100 2550
AR Path="/6186D6EC/62382E1E/61ADD72F" Ref="R224"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ADD72F" Ref="R251"  Part="1" 
AR Path="/63E462C7/62382E1E/61ADD72F" Ref="R?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ADD72F" Ref="R?"  Part="1" 
F 0 "R251" H 7168 2596 50  0000 L CNN
F 1 "523k" H 7168 2505 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7140 2540 50  0001 C CNN
F 3 "~" H 7100 2550 50  0001 C CNN
	1    7100 2550
	1    0    0    -1  
$EndComp
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R227
U 1 1 61ADF154
P 7100 3150
AR Path="/6186D6EC/62382E1E/61ADF154" Ref="R227"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61ADF154" Ref="R254"  Part="1" 
AR Path="/63E462C7/62382E1E/61ADF154" Ref="R?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61ADF154" Ref="R?"  Part="1" 
F 0 "R254" H 7168 3196 50  0000 L CNN
F 1 "100k" H 7168 3105 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7140 3140 50  0001 C CNN
F 3 "~" H 7100 3150 50  0001 C CNN
	1    7100 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7100 2700 7100 2750
Wire Wire Line
	7100 2750 6800 2750
Wire Wire Line
	6800 2750 6800 2650
Wire Wire Line
	6800 2650 6550 2650
Connection ~ 7100 2750
Wire Wire Line
	6550 2400 7100 2400
$Comp
L mainboard:GND #GND0128
U 1 1 61AE1599
P 7100 3400
AR Path="/6186D6EC/62382E1E/61AE1599" Ref="#GND0128"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AE1599" Ref="#GND0162"  Part="1" 
AR Path="/63E462C7/62382E1E/61AE1599" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AE1599" Ref="#GND?"  Part="1" 
F 0 "#GND0162" H 7100 3400 50  0001 C CNN
F 1 "GND" H 7100 3279 59  0000 C CNN
F 2 "" H 7100 3400 50  0001 C CNN
F 3 "" H 7100 3400 50  0001 C CNN
	1    7100 3400
	1    0    0    -1  
$EndComp
$Comp
L mainboard:GND #GND0129
U 1 1 61AE24D1
P 6700 3300
AR Path="/6186D6EC/62382E1E/61AE24D1" Ref="#GND0129"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AE24D1" Ref="#GND0163"  Part="1" 
AR Path="/63E462C7/62382E1E/61AE24D1" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AE24D1" Ref="#GND?"  Part="1" 
F 0 "#GND0163" H 6700 3300 50  0001 C CNN
F 1 "GND" H 6700 3179 59  0000 C CNN
F 2 "" H 6700 3300 50  0001 C CNN
F 3 "" H 6700 3300 50  0001 C CNN
	1    6700 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6550 3200 6700 3200
Wire Wire Line
	6550 3100 6550 3200
Connection ~ 6550 3200
Wire Wire Line
	6550 2800 6700 2800
Wire Wire Line
	6700 2800 6700 3200
Connection ~ 6700 3200
Wire Wire Line
	7100 2750 7100 3000
Wire Wire Line
	6550 2950 7550 2950
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R225
U 1 1 61AE6F46
P 7550 2700
AR Path="/6186D6EC/62382E1E/61AE6F46" Ref="R225"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AE6F46" Ref="R252"  Part="1" 
AR Path="/63E462C7/62382E1E/61AE6F46" Ref="R?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AE6F46" Ref="R?"  Part="1" 
F 0 "R252" H 7618 2746 50  0000 L CNN
F 1 "100k" H 7618 2655 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7590 2690 50  0001 C CNN
F 3 "~" H 7550 2700 50  0001 C CNN
	1    7550 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7100 2400 7550 2400
Wire Wire Line
	7550 2400 7550 2550
Connection ~ 7100 2400
Wire Wire Line
	7550 2850 7550 2950
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C213
U 1 1 61AEE122
P 7950 2550
AR Path="/6186D6EC/62382E1E/61AEE122" Ref="C213"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AEE122" Ref="C238"  Part="1" 
AR Path="/63E462C7/62382E1E/61AEE122" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AEE122" Ref="C?"  Part="1" 
F 0 "C238" H 8065 2596 50  0000 L CNN
F 1 "22uF" H 8065 2505 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 7988 2400 50  0001 C CNN
F 3 "~" H 7950 2550 50  0001 C CNN
	1    7950 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3500 1900 3650 1900
Connection ~ 3650 1900
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C214
U 1 1 61AF2082
P 8400 2550
AR Path="/6186D6EC/62382E1E/61AF2082" Ref="C214"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AF2082" Ref="C239"  Part="1" 
AR Path="/63E462C7/62382E1E/61AF2082" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AF2082" Ref="C?"  Part="1" 
F 0 "C239" H 8515 2596 50  0000 L CNN
F 1 "22uF" H 8515 2505 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 8438 2400 50  0001 C CNN
F 3 "~" H 8400 2550 50  0001 C CNN
	1    8400 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	7550 2400 7950 2400
Connection ~ 7550 2400
Connection ~ 7950 2400
Wire Wire Line
	7950 2400 8400 2400
Wire Wire Line
	7950 2700 7950 2800
Wire Wire Line
	7950 2800 8150 2800
Wire Wire Line
	8400 2800 8400 2700
$Comp
L mainboard:GND #GND0130
U 1 1 61AF7D47
P 8150 2900
AR Path="/6186D6EC/62382E1E/61AF7D47" Ref="#GND0130"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61AF7D47" Ref="#GND0164"  Part="1" 
AR Path="/63E462C7/62382E1E/61AF7D47" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61AF7D47" Ref="#GND?"  Part="1" 
F 0 "#GND0164" H 8150 2900 50  0001 C CNN
F 1 "GND" H 8150 2779 59  0000 C CNN
F 2 "" H 8150 2900 50  0001 C CNN
F 3 "" H 8150 2900 50  0001 C CNN
	1    8150 2900
	1    0    0    -1  
$EndComp
Connection ~ 8150 2800
Wire Wire Line
	8150 2800 8400 2800
Connection ~ 8400 2400
$Comp
L mainboard-rescue:C-Device-mainboard-rescue C215
U 1 1 61B0DBA6
P 8800 2550
AR Path="/6186D6EC/62382E1E/61B0DBA6" Ref="C215"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61B0DBA6" Ref="C240"  Part="1" 
AR Path="/63E462C7/62382E1E/61B0DBA6" Ref="C?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61B0DBA6" Ref="C?"  Part="1" 
F 0 "C240" H 8915 2596 50  0000 L CNN
F 1 "22uF" H 8915 2505 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 8838 2400 50  0001 C CNN
F 3 "~" H 8800 2550 50  0001 C CNN
	1    8800 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8800 2800 8800 2700
Wire Wire Line
	8400 2400 8800 2400
Wire Wire Line
	8950 2400 8800 2400
Connection ~ 8800 2400
Wire Wire Line
	8800 2800 8400 2800
Connection ~ 8400 2800
Text Notes 8500 2300 0    50   ~ 0
5V 2A MAX\nlarge amt of headroom here
Wire Wire Line
	4550 1900 5650 1900
Text Label 5450 2200 2    50   ~ 0
EN
Wire Wire Line
	5450 2200 5750 2200
$Comp
L mainboard-rescue:Q_PNP_BEC-Device-mainboard-rescue Q?
U 1 1 61B1E399
P 3750 3050
AR Path="/6186D6EC/61B1E399" Ref="Q?"  Part="1" 
AR Path="/6186D6EC/62382E1E/61B1E399" Ref="Q215"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61B1E399" Ref="Q222"  Part="1" 
AR Path="/63E462C7/62382E1E/61B1E399" Ref="Q?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61B1E399" Ref="Q?"  Part="1" 
F 0 "Q222" H 3941 3004 50  0000 L CNN
F 1 "MMBT3906-7-F" H 3941 3095 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 3950 3150 50  0001 C CNN
F 3 "MMBT3906-7-F" H 3750 3050 50  0001 C CNN
	1    3750 3050
	1    0    0    1   
$EndComp
Text Notes 2200 3250 0    50   ~ 0
active low in this case
$Comp
L mainboard:GND #GND0131
U 1 1 61B23CD9
P 3850 3800
AR Path="/6186D6EC/62382E1E/61B23CD9" Ref="#GND0131"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61B23CD9" Ref="#GND0165"  Part="1" 
AR Path="/63E462C7/62382E1E/61B23CD9" Ref="#GND?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61B23CD9" Ref="#GND?"  Part="1" 
F 0 "#GND0165" H 3850 3800 50  0001 C CNN
F 1 "GND" H 3850 3679 59  0000 C CNN
F 2 "" H 3850 3800 50  0001 C CNN
F 3 "" H 3850 3800 50  0001 C CNN
	1    3850 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 3700 3850 3650
Wire Wire Line
	3850 3300 3850 3250
$Comp
L mainboard-rescue:R_US-Device-mainboard-rescue R226
U 1 1 61B26414
P 3350 3050
AR Path="/6186D6EC/62382E1E/61B26414" Ref="R226"  Part="1" 
AR Path="/6186D6EC/63C1E7A2/61B26414" Ref="R253"  Part="1" 
AR Path="/63E462C7/62382E1E/61B26414" Ref="R?"  Part="1" 
AR Path="/63E462C7/63C1E7A2/61B26414" Ref="R?"  Part="1" 
F 0 "R253" V 3145 3050 50  0000 C CNN
F 1 "3.3k" V 3236 3050 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3390 3040 50  0001 C CNN
F 3 "~" H 3350 3050 50  0001 C CNN
	1    3350 3050
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 3050 3550 3050
Wire Wire Line
	3200 3050 3150 3050
Text Label 4250 3300 0    50   ~ 0
EN
Wire Wire Line
	4250 3300 3850 3300
Wire Wire Line
	3850 3300 3850 3350
Connection ~ 3850 3300
Wire Wire Line
	3850 2700 3850 2850
Wire Wire Line
	3600 2700 3850 2700
Text GLabel 3500 1900 0    50   BiDi ~ 0
VBUS
Text GLabel 3600 2700 0    50   BiDi ~ 0
VBUS
Text HLabel 8950 2400 2    50   Input ~ 0
Vout
Text HLabel 3150 3050 0    50   Input ~ 0
~EN
Text Notes 5500 1450 0    50   ~ 0
payload / rf regulator\nbased from TI WebBench Design
Text Notes 7800 3400 0    50   ~ 0
could possibly adjust inductor / caps in future to boost low current eff\nif power req. decreases
$EndSCHEMATC
