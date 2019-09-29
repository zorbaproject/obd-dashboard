#!/usr/bin/python3

import obd

connection = obd.OBD() # auto-connects to USB or RF port
#connection = obd.OBD("/dev/rfcomm0") 

#try:
#    print("Check speed")
#    cmd = obd.commands.SPEED # select an OBD command (sensor)
#    response = connection.query(cmd) # send the command, and parse the response
#    print(response.value.to("kph")) # returns unit-bearing values thanks to Pint
#except:
#    print("Unable to read. Engine not started?")

    
 #https://python-obd.readthedocs.io/en/latest/Command%20Tables/   
allcommands = [ "PIDS_A",
"STATUS",
"FREEZE_DTC",
"FUEL_STATUS",
"ENGINE_LOAD",
"COOLANT_TEMP",
"SHORT_FUEL_TRIM_1",
"LONG_FUEL_TRIM_1",
"SHORT_FUEL_TRIM_2",
"LONG_FUEL_TRIM_2",
"FUEL_PRESSURE",
"INTAKE_PRESSURE",
"RPM",
"SPEED",
"TIMING_ADVANCE",
"INTAKE_TEMP",
"MAF",
"THROTTLE_POS",
"AIR_STATUS",
"O2_SENSORS",
"O2_B1S1",
"O2_B1S2",
"O2_B1S3",
"O2_B1S4",
"O2_B2S1",
"O2_B2S2",
"O2_B2S3",
"O2_B2S4",
"OBD_COMPLIANCE",
"O2_SENSORS_ALT",
"AUX_INPUT_STATUS",
"RUN_TIME",
"PIDS_B",
"DISTANCE_W_MIL",
"FUEL_RAIL_PRESSURE_VAC",
"FUEL_RAIL_PRESSURE_DIRECT",
"O2_S1_WR_VOLTAGE",
"O2_S2_WR_VOLTAGE",
"O2_S3_WR_VOLTAGE",
"O2_S4_WR_VOLTAGE",
"O2_S5_WR_VOLTAGE",
"O2_S6_WR_VOLTAGE",
"O2_S7_WR_VOLTAGE",
"O2_S8_WR_VOLTAGE",
"COMMANDED_EGR",
"EGR_ERROR",
"EVAPORATIVE_PURGE",
"FUEL_LEVEL",
"WARMUPS_SINCE_DTC_CLEAR",
"DISTANCE_SINCE_DTC_CLEAR",
"EVAP_VAPOR_PRESSURE",
"BAROMETRIC_PRESSURE",
"O2_S1_WR_CURRENT",
"O2_S2_WR_CURRENT",
"O2_S3_WR_CURRENT",
"O2_S4_WR_CURRENT",
"O2_S5_WR_CURRENT",
"O2_S6_WR_CURRENT",
"O2_S7_WR_CURRENT",
"O2_S8_WR_CURRENT",
"CATALYST_TEMP_B1S1",
"CATALYST_TEMP_B2S1",
"CATALYST_TEMP_B1S2",
"CATALYST_TEMP_B2S2",
"PIDS_C",
"STATUS_DRIVE_CYCLE",
"CONTROL_MODULE_VOLTAGE",
"ABSOLUTE_LOAD",
"COMMANDED_EQUIV_RATIO",
"RELATIVE_THROTTLE_POS",
"AMBIANT_AIR_TEMP",
"THROTTLE_POS_B",
"THROTTLE_POS_C",
"ACCELERATOR_POS_D",
"ACCELERATOR_POS_E",
"ACCELERATOR_POS_F",
"THROTTLE_ACTUATOR",
"RUN_TIME_MIL",
"TIME_SINCE_DTC_CLEARED",
"unsupported",
"MAX_MAF",
"FUEL_TYPE",
"ETHANOL_PERCENT",
"EVAP_VAPOR_PRESSURE_ABS",
"EVAP_VAPOR_PRESSURE_ALT",
"SHORT_O2_TRIM_B1",
"LONG_O2_TRIM_B1",
"SHORT_O2_TRIM_B2",
"LONG_O2_TRIM_B2",
"FUEL_RAIL_PRESSURE_ABS",
"RELATIVE_ACCEL_POS",
"HYBRID_BATTERY_REMAINING",
"OIL_TEMP",
"FUEL_INJECT_TIMING",
"FUEL_RATE" ]

for key in allcommands:
    if obd.commands.has_name(key):
        try:
            print("Check "+key)
            cmd = obd.commands[key]
            response = connection.query(cmd)
            print(response.value)
        except:
            print("Unable to read. Engine not started?")
