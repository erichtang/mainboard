#include "shared-bindings/board/__init__.h"

STATIC const mp_rom_map_elem_t board_module_globals_table[] = {
    CIRCUITPYTHON_BOARD_DICT_STANDARD_ITEMS

    { MP_ROM_QSTR(MP_QSTR_SCK),      MP_ROM_PTR(&pin_PA13)  },
    { MP_ROM_QSTR(MP_QSTR_MOSI),     MP_ROM_PTR(&pin_PA12)  },
    { MP_ROM_QSTR(MP_QSTR_MISO),     MP_ROM_PTR(&pin_PA14)  },
    { MP_ROM_QSTR(MP_QSTR_SD_CS),    MP_ROM_PTR(&pin_PA27)  },

    { MP_ROM_QSTR(MP_QSTR_RELAY_A),  MP_ROM_PTR(&pin_PC26)  },
    { MP_ROM_QSTR(MP_QSTR_BURN1),    MP_ROM_PTR(&pin_PC27)  },
    { MP_ROM_QSTR(MP_QSTR_BURN2),    MP_ROM_PTR(&pin_PC28)  },

    { MP_ROM_QSTR(MP_QSTR_DAC0),     MP_ROM_PTR(&pin_PA02)  },
    { MP_ROM_QSTR(MP_QSTR_EN_RF),    MP_ROM_PTR(&pin_PA04)  },
    { MP_ROM_QSTR(MP_QSTR_AIN5),     MP_ROM_PTR(&pin_PA05)  },
    { MP_ROM_QSTR(MP_QSTR_BATTERY),  MP_ROM_PTR(&pin_PA06)  },
    //{ MP_ROM_QSTR(MP_QSTR_L1PROG),   MP_ROM_PTR(&pin_PA07)  },

    { MP_ROM_QSTR(MP_QSTR_CHRG),     MP_ROM_PTR(&pin_PB08)  },
    { MP_ROM_QSTR(MP_QSTR_PA16),     MP_ROM_PTR(&pin_PA16)  }, //Rx_2 rename later?
    { MP_ROM_QSTR(MP_QSTR_PA17),     MP_ROM_PTR(&pin_PA17)  }, //Tx_2 rename later?
    { MP_ROM_QSTR(MP_QSTR_VBUS_RST), MP_ROM_PTR(&pin_PA18)  },
    { MP_ROM_QSTR(MP_QSTR_PA19),     MP_ROM_PTR(&pin_PA19)  },
    { MP_ROM_QSTR(MP_QSTR_PA20),     MP_ROM_PTR(&pin_PA20)  },
    //{ MP_ROM_QSTR(MP_QSTR_PA22),     MP_ROM_PTR(&pin_PA22)  },
    { MP_ROM_QSTR(MP_QSTR_PB16),     MP_ROM_PTR(&pin_PB16)  },
    { MP_ROM_QSTR(MP_QSTR_PB17),     MP_ROM_PTR(&pin_PB17)  },
    { MP_ROM_QSTR(MP_QSTR_PB18),     MP_ROM_PTR(&pin_PB18)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PB19),     MP_ROM_PTR(&pin_PB19)  }, //added
    //{ MP_ROM_QSTR(MP_QSTR_PB22),     MP_ROM_PTR(&pin_PB22)  },
    //{ MP_ROM_QSTR(MP_QSTR_PB23),     MP_ROM_PTR(&pin_PB23)  },

    { MP_ROM_QSTR(MP_QSTR_RF1_RST),  MP_ROM_PTR(&pin_PB00)  },
    { MP_ROM_QSTR(MP_QSTR_RF1_CS),   MP_ROM_PTR(&pin_PB20)  },
    { MP_ROM_QSTR(MP_QSTR_RF1_IO4),  MP_ROM_PTR(&pin_PB04)  },
    { MP_ROM_QSTR(MP_QSTR_RF1_IO0),  MP_ROM_PTR(&pin_PB05)  },

    { MP_ROM_QSTR(MP_QSTR_RF2_IO0),   MP_ROM_PTR(&pin_PB06)  },
    { MP_ROM_QSTR(MP_QSTR_RF2_IO4),   MP_ROM_PTR(&pin_PB07)  },
    { MP_ROM_QSTR(MP_QSTR_RF2_CS),    MP_ROM_PTR(&pin_PB09)  },
    { MP_ROM_QSTR(MP_QSTR_RF2_RST),   MP_ROM_PTR(&pin_PB14)  },

    { MP_ROM_QSTR(MP_QSTR_EN_GPS),   MP_ROM_PTR(&pin_PB01)  },
    { MP_ROM_QSTR(MP_QSTR_TX),       MP_ROM_PTR(&pin_PB02)  },
    { MP_ROM_QSTR(MP_QSTR_RX),       MP_ROM_PTR(&pin_PB03)  },
    { MP_ROM_QSTR(MP_QSTR_TX2),      MP_ROM_PTR(&pin_PA17)  },
    { MP_ROM_QSTR(MP_QSTR_RX2),      MP_ROM_PTR(&pin_PA16)  },
    { MP_ROM_QSTR(MP_QSTR_TX3),      MP_ROM_PTR(&pin_PC13)  }, //added
    { MP_ROM_QSTR(MP_QSTR_RX3),      MP_ROM_PTR(&pin_PC12)  }, //added
    { MP_ROM_QSTR(MP_QSTR_TX4),      MP_ROM_PTR(&pin_PC17)  }, //added
    { MP_ROM_QSTR(MP_QSTR_RX4),      MP_ROM_PTR(&pin_PC16)  }, //added

//add rest of GPIO here
    { MP_ROM_QSTR(MP_QSTR_PC00),     MP_ROM_PTR(&pin_PC00)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC01),     MP_ROM_PTR(&pin_PC01)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC02),     MP_ROM_PTR(&pin_PC02)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC03),     MP_ROM_PTR(&pin_PC03)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC05),     MP_ROM_PTR(&pin_PC05)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC06),     MP_ROM_PTR(&pin_PC06)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC07),     MP_ROM_PTR(&pin_PC07)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC10),     MP_ROM_PTR(&pin_PC10)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC11),     MP_ROM_PTR(&pin_PC11)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC14),     MP_ROM_PTR(&pin_PC14)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC15),     MP_ROM_PTR(&pin_PC15)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC18),     MP_ROM_PTR(&pin_PC18)  }, //added
    { MP_ROM_QSTR(MP_QSTR_PC19),     MP_ROM_PTR(&pin_PC19)  }, //added

    { MP_ROM_QSTR(MP_QSTR_SDA),      MP_ROM_PTR(&pin_PB12)  },
    { MP_ROM_QSTR(MP_QSTR_SCL),      MP_ROM_PTR(&pin_PB13)  },
    //{ MP_ROM_QSTR(MP_QSTR_SCL2),     MP_ROM_PTR(&pin_PA16)  },
    //{ MP_ROM_QSTR(MP_QSTR_SDA2),     MP_ROM_PTR(&pin_PA17)  },

    { MP_ROM_QSTR(MP_QSTR_WDT_WDI),  MP_ROM_PTR(&pin_PA23)  },
    { MP_ROM_QSTR(MP_QSTR_NEOPIXEL), MP_ROM_PTR(&pin_PA21)  },

    { MP_ROM_QSTR(MP_QSTR_UART), MP_ROM_PTR(&board_uart_obj) },
    { MP_ROM_QSTR(MP_QSTR_I2C),  MP_ROM_PTR(&board_i2c_obj)  },
    { MP_ROM_QSTR(MP_QSTR_SPI),  MP_ROM_PTR(&board_spi_obj)  },

};
MP_DEFINE_CONST_DICT(board_module_globals, board_module_globals_table);
