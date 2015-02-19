import serial
import struct
import time

feedback = serial.Serial('/dev/ttyACM0', 9600) # Arduino serial
ssc32 = serial.Serial('/dev/ttyUSB0', 115200) # SSC-32 serial

BURST = 32 # Samples sent by Arduino in one burst

def getBurst():
    """
    Request BURST samples of arduino analog
    Return a list of samples
    """
    feedback.write(chr(BURST))
    
    while feedback.inWaiting() < 4*BURST:
        pass
    line = feedback.readline()

    return line.split(',')

if __name__ == "__main__":
    # reset the arduino
    feedback.setDTR(level=False)
    time.sleep(0.5)
    # ensure there is no stale data in the buffer
    feedback.flushInput()
    feedback.setDTR()
    time.sleep(0.5)

    print "waiting for arduino..."

    # initial handshake w/ arduino
    print 'handshake: ' + str(struct.unpack("c", feedback.read())[0])
    feedback.flushInput()
    feedback.write('\x10')
    print "connected to arduino..."

    ssc32.write("#0 P0\r")
    max_vol = 0 # potentiometer max received voltage
    min_vol = 1024 # potentiometer min received voltage
    min_pos = 900 # servo min position
    max_pos = 2000 # servo max position

    # find max_vol
    ssc32.write("#0 P{0}\r".format(max_pos))
    time.sleep(1)
    list_line = getBurst()
    for l in list_line:
        if len(l) == 4:
            vol = int(l)
            if vol > max_vol:
                max_vol = vol
            elif vol < min_vol:
                min_vol = vol

    # find min_vol
    ssc32.write("#0 P{0}\r".format(min_pos))
    time.sleep(1)
    list_line = getBurst()
    for l in list_line:
        if len(l) == 4:
            vol = int(l)
            if vol > max_vol:
                max_vol = vol
            elif vol < min_vol:
                min_vol = vol

    mid_vol = (max_vol + min_vol)/2                
    print min_vol, max_vol, mid_vol
    
    # After find max_ and min_vol
    # This part find servo position for a found max_ and min_vol
    vol = mid_vol
    ssc32.write("#0 P1500\r")
    pos = 1500
    while min_vol <= vol:
        list_line = getBurst()
        for l in list_line:
            if len(l) == 4:
                vol = int(l)
        ssc32.write("#0 P{0}\r".format(pos))
        pos = pos - 5
    print "min_vol", min_vol
    print "vol", vol
    print "min_pos", min_pos
    print "pos min", pos
    ssc32.write("#0 P0\r")
    print
    
    vol = (max_vol + min_vol)/2
    ssc32.write("#0 P1500\r")
    pos = 1500
    while max_vol >= vol:
        list_line = getBurst()
        for l in list_line:
            if len(l) == 4:
                vol = int(l)
        ssc32.write("#0 P{0}\r".format(pos))
        pos = pos + 5
    print "max_vol", max_vol
    print "vol", vol
    print "max_pos", max_pos
    print "pos max", pos
    ssc32.write("#0 P0\r")
    print
    
    vol = min_vol
    print vol
    print
    ssc32.write("#0 P900\r")
    time.sleep(.5)
    pos = 900
    while mid_vol >= vol:
        list_line = getBurst()
        for l in list_line:
            if len(l) == 4:
                vol = int(l)
        ssc32.write("#0 P{0}\r".format(pos))
        pos = pos + 5
    print "mid_vol", mid_vol
    print "vol", vol
    print "mid_pos", str(1500)
    print "pos mid", pos
    ssc32.write("#0 P0\r")
    print

