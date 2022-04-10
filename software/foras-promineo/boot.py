import usb_cdc
print("enabled data")
usb_cdc.enable(console=True, data=True)
usb_cdc.data.DtrEnable