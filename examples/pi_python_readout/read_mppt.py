from smbus2 import SMBus, i2c_msg
import struct
import json

# address of the mppt charger
MPPT_CHG_ADDR = 0x12

# mppt status messages
MPPT_STATUS = [ "NIGHT",
                "IDLE",
                "VSRCV",
                "SCAN",
                "BULK",
                "ABSORPTION",
                "FLOAT",
                "ILLEGAL",
                "I2C FAIL"]


MPPT_STAUS_REGISTERS = {

    "MPPT_CHG_REG_ID"   :0,
    "MPPT_CHG_STATUS"   :2,
    "MPPT_CHG_BUCK"     :4
}

MPPT_MEASURED_REGISTERS = {
    "MPPT_CHG_VS"       :6,
    "MPPT_CHG_IS"       :8,
    "MPPT_CHG_VB"       :10,
    "MPPT_CHG_IB"       :12,
    "MPPT_CHG_IC"       :14,
    "MPPT_CHG_INT_T"    :16,
    "MPPT_CHG_EXT_T"    :18,
    "MPPT_CHG_VM"       :20,
    "MPPT_CHG_TH"       :22
}

MPPT_REGISTERS = MPPT_STAUS_REGISTERS | MPPT_MEASURED_REGISTERS

def read_16(reg, bus):
    regwrite = i2c_msg.write(MPPT_CHG_ADDR, [reg]) #write register address first
    regread = i2c_msg.read(MPPT_CHG_ADDR, 2) # read back two bytes
    bus.i2c_rdwr(regwrite, regread)
    buf = list(regread)
    return (buf[0] << 8 ) + buf[1]

registervalues = {}
with SMBus(1) as bus:
    for register in MPPT_REGISTERS:
        readregister =  read_16(MPPT_REGISTERS[register], bus)
        #make signed int out of the data read if necessary
        if register not in MPPT_STAUS_REGISTERS:
            readregister = readregister - (readregister >> 15 << 16)
        registervalues[register] =readregister
        
#decode status

registervalues["STATUS"] = MPPT_STATUS[registervalues["MPPT_CHG_STATUS"]&0x07]


#print(f"read register values from MPPT:")
print(json.dumps(registervalues, indent=2))

