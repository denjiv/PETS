import obd
import serial
from datetime import datetime
import time
import json
from nmea_parse import parse_gngga

# Subaru Impreza 2015 Sport max torque (Nm)
MAX_ENGINE_TORQUE = 196.6

# for gps connection setup
port = "COM15"
baud = 9600

# for vehicle OBD II setup
connection = obd.OBD()
print connection.interface.port_name()

# command list for OBD II
spd_cmd = obd.commands.SPEED  # km/h
acc_pdl_cmd = obd.commands.RELATIVE_ACCEL_POS  # %
rpm_cmd = obd.commands.RPM  # rpm
eng_load_cmd = obd.commands.ENGINE_LOAD # %
temp_cmd = obd.commands.AMBIANT_AIR_TEMP  # C


# query both gps and vehicle data
def data_query(f, spd_cmd, acc_pdl_cmd, rpm_cmd, eng_load_cmd, temp_cmd, ser):
    # parse serial data stream from gps module
    line = ser.readline()
    line = line.strip()
    parts = line.split(",")

    while parts[0] != "$GNGGA":
        line = ser.readline()
        line = line.strip()
        parts = line.split(",")

    time = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

    lat, lon = parse_gngga(parts)

    # sending OBD II PID command to vehicle and obtain data
    spd = connection.query(spd_cmd, force=True)
    spd2num = float(str(spd).split()[0])
    # spd2num = 999

    acc_pdl = connection.query(acc_pdl_cmd, force=True)
    acc_pdl2num = float(str(acc_pdl).split()[0])
    # acc_pdl2num = 999

    rpm = connection.query(rpm_cmd, force=True)
    rpm2num = float(str(rpm).split()[0])
    # rpm2num = 999

    eng_load = connection.query(eng_load_cmd, force=True)
    load2num = float(str(eng_load).split()[0])
    load_nm = load2num/100*MAX_ENGINE_TORQUE
    # load_nm = 999

    pwr = rpm2num*load_nm/9.5488/1000
    # pwr = 999

    temp = connection.query(temp_cmd, force=True)
    temp2num = float(str(temp).split()[0])

    # store data into dictionary
    data = { 'Speed':               spd2num, 
             'Accel_Pedal_Pos':     acc_pdl2num, 
             'RPM':                 rpm2num, 
             'Torque':              load_nm, 
             'Power':               pwr,
             'Latitude':            lat,
             'Longitude':           lon,
             'Temperature':         temp2num,
             'Time':                time
           }

    # convet dict to json
    json.dump( data,
               f,
               indent=4,
               ensure_ascii=False )

    print "Time: " + time
    print "Vehicle Speed: " + str(spd.value)
    print "Accelerator Pedal Position: " + str(acc_pdl)
    print "Engine RPM: " + str(rpm.value)
    print "Engine Load: " + str(load_nm) + " Nm"
    print "Power to Wheels: " + str(pwr) + " kW"
    print "Ambient Air Temperature: " + str(temp.value)


if __name__ == "__main__":
    try:
        ser = serial.Serial(port, baud)
        f = open('back1.json', 'w') # change filename for each trip
        f.write("[\n")
        data_query(f, spd_cmd, acc_pdl_cmd, rpm_cmd, eng_load_cmd, temp_cmd, ser)
        time.sleep(1)

        while 1:
            f.write(",\n")
            data_query(f, spd_cmd, acc_pdl_cmd, rpm_cmd, eng_load_cmd, temp_cmd, ser)

            print '\n'
            time.sleep(1)
    finally:
        f.write("\n")
        ser.close()
        f.close()
