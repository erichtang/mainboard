# crc-8 for third byte in header using message
# crc = crc_poly(msg, 8, 0x07) # this gets crc
# crc.to_bytes(1, 'big') # converts crc from int to bytes
# test it works for crc-8 with https://crccalc.com/

def reflect_data(x, width):
    # See: https://stackoverflow.com/a/20918545
    if width == 8:
        x = ((x & 0x55) << 1) | ((x & 0xAA) >> 1)
        x = ((x & 0x33) << 2) | ((x & 0xCC) >> 2)
        x = ((x & 0x0F) << 4) | ((x & 0xF0) >> 4)
    else:
        raise ValueError('Unsupported width')
    return x

def crc_poly(data, n, poly, crc=0, ref_in=False, ref_out=False, xor_out=0):
    g = 1 << n | poly  # Generator polynomial

    # Loop over the data
    for d in data:
        # Reverse the input byte if the flag is true
        if ref_in:
            d = reflect_data(d, 8)

        # XOR the top byte in the CRC with the input byte
        crc ^= d << (n - 8)

        # Loop over all the bits in the byte
        for _ in range(8):
            # Start by shifting the CRC, so we can check for the top bit
            crc <<= 1

            # XOR the CRC if the top bit is 1
            if crc & (1 << n):
                crc ^= g

    # Reverse the output if the flag is true
    if ref_out:
        crc = reflect_data(crc, n)

    # Return the CRC value
    return crc ^ xor_out
