import struct

# Message id constants
gps_v2_id = 16
gps_v3_id = 26
gps_v4_id = 34
gps_raw_v1_id = 48
imu_v3_id = 17
imu_v4_id = 35
imu_v5_id = 45
airdata_v5_id = 18
airdata_v6_id = 40
airdata_v7_id = 43
filter_v3_id = 31
filter_v4_id = 36
filter_v5_id = 47
actuator_v2_id = 21
actuator_v3_id = 37
pilot_v2_id = 20
pilot_v3_id = 38
ap_status_v4_id = 30
ap_status_v5_id = 32
ap_status_v6_id = 33
ap_status_v7_id = 39
system_health_v4_id = 19
system_health_v5_id = 41
system_health_v6_id = 46
payload_v2_id = 23
payload_v3_id = 42
event_v1_id = 27
event_v2_id = 44
command_v1_id = 28
stream_v1_id = 49

# Constants
max_raw_sats = 12  # maximum array size to store satellite raw data

# Message: gps_v2
# Id: 16
class gps_v2():
    id = 16
    _pack_string = "<BdddfhhhdBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.unixtime_sec = 0.0
        self.satellites = 0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  self.unixtime_sec,
                  self.satellites,
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.unixtime_sec,
         self.satellites,
         self.status) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100

# Message: gps_v3
# Id: 26
class gps_v3():
    id = 26
    _pack_string = "<BdddfhhhdBHHHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.unixtime_sec = 0.0
        self.satellites = 0
        self.horiz_accuracy_m = 0.0
        self.vert_accuracy_m = 0.0
        self.pdop = 0.0
        self.fix_type = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  self.unixtime_sec,
                  self.satellites,
                  int(round(self.horiz_accuracy_m * 100)),
                  int(round(self.vert_accuracy_m * 100)),
                  int(round(self.pdop * 100)),
                  self.fix_type)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.unixtime_sec,
         self.satellites,
         self.horiz_accuracy_m,
         self.vert_accuracy_m,
         self.pdop,
         self.fix_type) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100
        self.horiz_accuracy_m /= 100
        self.vert_accuracy_m /= 100
        self.pdop /= 100

# Message: gps_v4
# Id: 34
class gps_v4():
    id = 34
    _pack_string = "<BfddfhhhdBHHHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.unixtime_sec = 0.0
        self.satellites = 0
        self.horiz_accuracy_m = 0.0
        self.vert_accuracy_m = 0.0
        self.pdop = 0.0
        self.fix_type = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  self.unixtime_sec,
                  self.satellites,
                  int(round(self.horiz_accuracy_m * 100)),
                  int(round(self.vert_accuracy_m * 100)),
                  int(round(self.pdop * 100)),
                  self.fix_type)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.unixtime_sec,
         self.satellites,
         self.horiz_accuracy_m,
         self.vert_accuracy_m,
         self.pdop,
         self.fix_type) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100
        self.horiz_accuracy_m /= 100
        self.vert_accuracy_m /= 100
        self.pdop /= 100

# Message: gps_raw_v1
# Id: 48
class gps_raw_v1():
    id = 48
    _pack_string = "<BfdBBBBBBBBBBBBBdddddddddddddddddddddddd"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.receiver_tow = 0.0
        self.num_sats = 0
        self.svid = [0] * max_raw_sats
        self.pseudorange = [0.0] * max_raw_sats
        self.doppler = [0.0] * max_raw_sats
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.receiver_tow,
                  self.num_sats,
                  self.svid[0],
                  self.svid[1],
                  self.svid[2],
                  self.svid[3],
                  self.svid[4],
                  self.svid[5],
                  self.svid[6],
                  self.svid[7],
                  self.svid[8],
                  self.svid[9],
                  self.svid[10],
                  self.svid[11],
                  self.pseudorange[0],
                  self.pseudorange[1],
                  self.pseudorange[2],
                  self.pseudorange[3],
                  self.pseudorange[4],
                  self.pseudorange[5],
                  self.pseudorange[6],
                  self.pseudorange[7],
                  self.pseudorange[8],
                  self.pseudorange[9],
                  self.pseudorange[10],
                  self.pseudorange[11],
                  self.doppler[0],
                  self.doppler[1],
                  self.doppler[2],
                  self.doppler[3],
                  self.doppler[4],
                  self.doppler[5],
                  self.doppler[6],
                  self.doppler[7],
                  self.doppler[8],
                  self.doppler[9],
                  self.doppler[10],
                  self.doppler[11])
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.receiver_tow,
         self.num_sats,
         self.svid[0],
         self.svid[1],
         self.svid[2],
         self.svid[3],
         self.svid[4],
         self.svid[5],
         self.svid[6],
         self.svid[7],
         self.svid[8],
         self.svid[9],
         self.svid[10],
         self.svid[11],
         self.pseudorange[0],
         self.pseudorange[1],
         self.pseudorange[2],
         self.pseudorange[3],
         self.pseudorange[4],
         self.pseudorange[5],
         self.pseudorange[6],
         self.pseudorange[7],
         self.pseudorange[8],
         self.pseudorange[9],
         self.pseudorange[10],
         self.pseudorange[11],
         self.doppler[0],
         self.doppler[1],
         self.doppler[2],
         self.doppler[3],
         self.doppler[4],
         self.doppler[5],
         self.doppler[6],
         self.doppler[7],
         self.doppler[8],
         self.doppler[9],
         self.doppler[10],
         self.doppler[11]) = self._struct.unpack(msg)

# Message: imu_v3
# Id: 17
class imu_v3():
    id = 17
    _pack_string = "<BdfffffffffhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.p_rad_sec = 0.0
        self.q_rad_sec = 0.0
        self.r_rad_sec = 0.0
        self.ax_mps_sec = 0.0
        self.ay_mps_sec = 0.0
        self.az_mps_sec = 0.0
        self.hx = 0.0
        self.hy = 0.0
        self.hz = 0.0
        self.temp_C = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.p_rad_sec,
                  self.q_rad_sec,
                  self.r_rad_sec,
                  self.ax_mps_sec,
                  self.ay_mps_sec,
                  self.az_mps_sec,
                  self.hx,
                  self.hy,
                  self.hz,
                  int(round(self.temp_C * 10)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.p_rad_sec,
         self.q_rad_sec,
         self.r_rad_sec,
         self.ax_mps_sec,
         self.ay_mps_sec,
         self.az_mps_sec,
         self.hx,
         self.hy,
         self.hz,
         self.temp_C,
         self.status) = self._struct.unpack(msg)
        self.temp_C /= 10

# Message: imu_v4
# Id: 35
class imu_v4():
    id = 35
    _pack_string = "<BffffffffffhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.p_rad_sec = 0.0
        self.q_rad_sec = 0.0
        self.r_rad_sec = 0.0
        self.ax_mps_sec = 0.0
        self.ay_mps_sec = 0.0
        self.az_mps_sec = 0.0
        self.hx = 0.0
        self.hy = 0.0
        self.hz = 0.0
        self.temp_C = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.p_rad_sec,
                  self.q_rad_sec,
                  self.r_rad_sec,
                  self.ax_mps_sec,
                  self.ay_mps_sec,
                  self.az_mps_sec,
                  self.hx,
                  self.hy,
                  self.hz,
                  int(round(self.temp_C * 10)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.p_rad_sec,
         self.q_rad_sec,
         self.r_rad_sec,
         self.ax_mps_sec,
         self.ay_mps_sec,
         self.az_mps_sec,
         self.hx,
         self.hy,
         self.hz,
         self.temp_C,
         self.status) = self._struct.unpack(msg)
        self.temp_C /= 10

# Message: imu_v5
# Id: 45
class imu_v5():
    id = 45
    _pack_string = "<BffffffffffffffffhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.p_rad_sec = 0.0
        self.q_rad_sec = 0.0
        self.r_rad_sec = 0.0
        self.ax_mps_sec = 0.0
        self.ay_mps_sec = 0.0
        self.az_mps_sec = 0.0
        self.hx = 0.0
        self.hy = 0.0
        self.hz = 0.0
        self.ax_raw = 0.0
        self.ay_raw = 0.0
        self.az_raw = 0.0
        self.hx_raw = 0.0
        self.hy_raw = 0.0
        self.hz_raw = 0.0
        self.temp_C = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.p_rad_sec,
                  self.q_rad_sec,
                  self.r_rad_sec,
                  self.ax_mps_sec,
                  self.ay_mps_sec,
                  self.az_mps_sec,
                  self.hx,
                  self.hy,
                  self.hz,
                  self.ax_raw,
                  self.ay_raw,
                  self.az_raw,
                  self.hx_raw,
                  self.hy_raw,
                  self.hz_raw,
                  int(round(self.temp_C * 10)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.p_rad_sec,
         self.q_rad_sec,
         self.r_rad_sec,
         self.ax_mps_sec,
         self.ay_mps_sec,
         self.az_mps_sec,
         self.hx,
         self.hy,
         self.hz,
         self.ax_raw,
         self.ay_raw,
         self.az_raw,
         self.hx_raw,
         self.hy_raw,
         self.hz_raw,
         self.temp_C,
         self.status) = self._struct.unpack(msg)
        self.temp_C /= 10

# Message: airdata_v5
# Id: 18
class airdata_v5():
    id = 18
    _pack_string = "<BdHhhffhHBBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.pressure_mbar = 0.0
        self.temp_C = 0.0
        self.airspeed_smoothed_kt = 0.0
        self.altitude_smoothed_m = 0.0
        self.altitude_true_m = 0.0
        self.pressure_vertical_speed_fps = 0.0
        self.wind_dir_deg = 0.0
        self.wind_speed_kt = 0.0
        self.pitot_scale_factor = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.pressure_mbar * 10)),
                  int(round(self.temp_C * 100)),
                  int(round(self.airspeed_smoothed_kt * 100)),
                  self.altitude_smoothed_m,
                  self.altitude_true_m,
                  int(round(self.pressure_vertical_speed_fps * 600)),
                  int(round(self.wind_dir_deg * 100)),
                  int(round(self.wind_speed_kt * 4)),
                  int(round(self.pitot_scale_factor * 100)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.pressure_mbar,
         self.temp_C,
         self.airspeed_smoothed_kt,
         self.altitude_smoothed_m,
         self.altitude_true_m,
         self.pressure_vertical_speed_fps,
         self.wind_dir_deg,
         self.wind_speed_kt,
         self.pitot_scale_factor,
         self.status) = self._struct.unpack(msg)
        self.pressure_mbar /= 10
        self.temp_C /= 100
        self.airspeed_smoothed_kt /= 100
        self.pressure_vertical_speed_fps /= 600
        self.wind_dir_deg /= 100
        self.wind_speed_kt /= 4
        self.pitot_scale_factor /= 100

# Message: airdata_v6
# Id: 40
class airdata_v6():
    id = 40
    _pack_string = "<BfHhhffhHBBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.pressure_mbar = 0.0
        self.temp_C = 0.0
        self.airspeed_smoothed_kt = 0.0
        self.altitude_smoothed_m = 0.0
        self.altitude_true_m = 0.0
        self.pressure_vertical_speed_fps = 0.0
        self.wind_dir_deg = 0.0
        self.wind_speed_kt = 0.0
        self.pitot_scale_factor = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.pressure_mbar * 10)),
                  int(round(self.temp_C * 100)),
                  int(round(self.airspeed_smoothed_kt * 100)),
                  self.altitude_smoothed_m,
                  self.altitude_true_m,
                  int(round(self.pressure_vertical_speed_fps * 600)),
                  int(round(self.wind_dir_deg * 100)),
                  int(round(self.wind_speed_kt * 4)),
                  int(round(self.pitot_scale_factor * 100)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.pressure_mbar,
         self.temp_C,
         self.airspeed_smoothed_kt,
         self.altitude_smoothed_m,
         self.altitude_true_m,
         self.pressure_vertical_speed_fps,
         self.wind_dir_deg,
         self.wind_speed_kt,
         self.pitot_scale_factor,
         self.status) = self._struct.unpack(msg)
        self.pressure_mbar /= 10
        self.temp_C /= 100
        self.airspeed_smoothed_kt /= 100
        self.pressure_vertical_speed_fps /= 600
        self.wind_dir_deg /= 100
        self.wind_speed_kt /= 4
        self.pitot_scale_factor /= 100

# Message: airdata_v7
# Id: 43
class airdata_v7():
    id = 43
    _pack_string = "<BfHhhffhHBBHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.pressure_mbar = 0.0
        self.temp_C = 0.0
        self.airspeed_smoothed_kt = 0.0
        self.altitude_smoothed_m = 0.0
        self.altitude_true_m = 0.0
        self.pressure_vertical_speed_fps = 0.0
        self.wind_dir_deg = 0.0
        self.wind_speed_kt = 0.0
        self.pitot_scale_factor = 0.0
        self.error_count = 0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.pressure_mbar * 10)),
                  int(round(self.temp_C * 100)),
                  int(round(self.airspeed_smoothed_kt * 100)),
                  self.altitude_smoothed_m,
                  self.altitude_true_m,
                  int(round(self.pressure_vertical_speed_fps * 600)),
                  int(round(self.wind_dir_deg * 100)),
                  int(round(self.wind_speed_kt * 4)),
                  int(round(self.pitot_scale_factor * 100)),
                  self.error_count,
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.pressure_mbar,
         self.temp_C,
         self.airspeed_smoothed_kt,
         self.altitude_smoothed_m,
         self.altitude_true_m,
         self.pressure_vertical_speed_fps,
         self.wind_dir_deg,
         self.wind_speed_kt,
         self.pitot_scale_factor,
         self.error_count,
         self.status) = self._struct.unpack(msg)
        self.pressure_mbar /= 10
        self.temp_C /= 100
        self.airspeed_smoothed_kt /= 100
        self.pressure_vertical_speed_fps /= 600
        self.wind_dir_deg /= 100
        self.wind_speed_kt /= 4
        self.pitot_scale_factor /= 100

# Message: filter_v3
# Id: 31
class filter_v3():
    id = 31
    _pack_string = "<BdddfhhhhhhhhhhhhBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.roll_deg = 0.0
        self.pitch_deg = 0.0
        self.yaw_deg = 0.0
        self.p_bias = 0.0
        self.q_bias = 0.0
        self.r_bias = 0.0
        self.ax_bias = 0.0
        self.ay_bias = 0.0
        self.az_bias = 0.0
        self.sequence_num = 0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  int(round(self.roll_deg * 10)),
                  int(round(self.pitch_deg * 10)),
                  int(round(self.yaw_deg * 10)),
                  int(round(self.p_bias * 10000)),
                  int(round(self.q_bias * 10000)),
                  int(round(self.r_bias * 10000)),
                  int(round(self.ax_bias * 1000)),
                  int(round(self.ay_bias * 1000)),
                  int(round(self.az_bias * 1000)),
                  self.sequence_num,
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.roll_deg,
         self.pitch_deg,
         self.yaw_deg,
         self.p_bias,
         self.q_bias,
         self.r_bias,
         self.ax_bias,
         self.ay_bias,
         self.az_bias,
         self.sequence_num,
         self.status) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.yaw_deg /= 10
        self.p_bias /= 10000
        self.q_bias /= 10000
        self.r_bias /= 10000
        self.ax_bias /= 1000
        self.ay_bias /= 1000
        self.az_bias /= 1000

# Message: filter_v4
# Id: 36
class filter_v4():
    id = 36
    _pack_string = "<BfddfhhhhhhhhhhhhBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.roll_deg = 0.0
        self.pitch_deg = 0.0
        self.yaw_deg = 0.0
        self.p_bias = 0.0
        self.q_bias = 0.0
        self.r_bias = 0.0
        self.ax_bias = 0.0
        self.ay_bias = 0.0
        self.az_bias = 0.0
        self.sequence_num = 0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  int(round(self.roll_deg * 10)),
                  int(round(self.pitch_deg * 10)),
                  int(round(self.yaw_deg * 10)),
                  int(round(self.p_bias * 10000)),
                  int(round(self.q_bias * 10000)),
                  int(round(self.r_bias * 10000)),
                  int(round(self.ax_bias * 1000)),
                  int(round(self.ay_bias * 1000)),
                  int(round(self.az_bias * 1000)),
                  self.sequence_num,
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.roll_deg,
         self.pitch_deg,
         self.yaw_deg,
         self.p_bias,
         self.q_bias,
         self.r_bias,
         self.ax_bias,
         self.ay_bias,
         self.az_bias,
         self.sequence_num,
         self.status) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.yaw_deg /= 10
        self.p_bias /= 10000
        self.q_bias /= 10000
        self.r_bias /= 10000
        self.ax_bias /= 1000
        self.ay_bias /= 1000
        self.az_bias /= 1000

# Message: filter_v5
# Id: 47
class filter_v5():
    id = 47
    _pack_string = "<BfddfhhhhhhhhhhhhHHHBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.latitude_deg = 0.0
        self.longitude_deg = 0.0
        self.altitude_m = 0.0
        self.vn_ms = 0.0
        self.ve_ms = 0.0
        self.vd_ms = 0.0
        self.roll_deg = 0.0
        self.pitch_deg = 0.0
        self.yaw_deg = 0.0
        self.p_bias = 0.0
        self.q_bias = 0.0
        self.r_bias = 0.0
        self.ax_bias = 0.0
        self.ay_bias = 0.0
        self.az_bias = 0.0
        self.max_pos_cov = 0.0
        self.max_vel_cov = 0.0
        self.max_att_cov = 0.0
        self.sequence_num = 0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.latitude_deg,
                  self.longitude_deg,
                  self.altitude_m,
                  int(round(self.vn_ms * 100)),
                  int(round(self.ve_ms * 100)),
                  int(round(self.vd_ms * 100)),
                  int(round(self.roll_deg * 10)),
                  int(round(self.pitch_deg * 10)),
                  int(round(self.yaw_deg * 10)),
                  int(round(self.p_bias * 10000)),
                  int(round(self.q_bias * 10000)),
                  int(round(self.r_bias * 10000)),
                  int(round(self.ax_bias * 1000)),
                  int(round(self.ay_bias * 1000)),
                  int(round(self.az_bias * 1000)),
                  int(round(self.max_pos_cov * 100)),
                  int(round(self.max_vel_cov * 1000)),
                  int(round(self.max_att_cov * 10000)),
                  self.sequence_num,
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.latitude_deg,
         self.longitude_deg,
         self.altitude_m,
         self.vn_ms,
         self.ve_ms,
         self.vd_ms,
         self.roll_deg,
         self.pitch_deg,
         self.yaw_deg,
         self.p_bias,
         self.q_bias,
         self.r_bias,
         self.ax_bias,
         self.ay_bias,
         self.az_bias,
         self.max_pos_cov,
         self.max_vel_cov,
         self.max_att_cov,
         self.sequence_num,
         self.status) = self._struct.unpack(msg)
        self.vn_ms /= 100
        self.ve_ms /= 100
        self.vd_ms /= 100
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.yaw_deg /= 10
        self.p_bias /= 10000
        self.q_bias /= 10000
        self.r_bias /= 10000
        self.ax_bias /= 1000
        self.ay_bias /= 1000
        self.az_bias /= 1000
        self.max_pos_cov /= 100
        self.max_vel_cov /= 1000
        self.max_att_cov /= 10000

# Message: actuator_v2
# Id: 21
class actuator_v2():
    id = 21
    _pack_string = "<BdhhHhhhhhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.aileron = 0.0
        self.elevator = 0.0
        self.throttle = 0.0
        self.rudder = 0.0
        self.channel5 = 0.0
        self.flaps = 0.0
        self.channel7 = 0.0
        self.channel8 = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.aileron * 20000)),
                  int(round(self.elevator * 20000)),
                  int(round(self.throttle * 60000)),
                  int(round(self.rudder * 20000)),
                  int(round(self.channel5 * 20000)),
                  int(round(self.flaps * 20000)),
                  int(round(self.channel7 * 20000)),
                  int(round(self.channel8 * 20000)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.aileron,
         self.elevator,
         self.throttle,
         self.rudder,
         self.channel5,
         self.flaps,
         self.channel7,
         self.channel8,
         self.status) = self._struct.unpack(msg)
        self.aileron /= 20000
        self.elevator /= 20000
        self.throttle /= 60000
        self.rudder /= 20000
        self.channel5 /= 20000
        self.flaps /= 20000
        self.channel7 /= 20000
        self.channel8 /= 20000

# Message: actuator_v3
# Id: 37
class actuator_v3():
    id = 37
    _pack_string = "<BfhhHhhhhhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.aileron = 0.0
        self.elevator = 0.0
        self.throttle = 0.0
        self.rudder = 0.0
        self.channel5 = 0.0
        self.flaps = 0.0
        self.channel7 = 0.0
        self.channel8 = 0.0
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.aileron * 20000)),
                  int(round(self.elevator * 20000)),
                  int(round(self.throttle * 60000)),
                  int(round(self.rudder * 20000)),
                  int(round(self.channel5 * 20000)),
                  int(round(self.flaps * 20000)),
                  int(round(self.channel7 * 20000)),
                  int(round(self.channel8 * 20000)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.aileron,
         self.elevator,
         self.throttle,
         self.rudder,
         self.channel5,
         self.flaps,
         self.channel7,
         self.channel8,
         self.status) = self._struct.unpack(msg)
        self.aileron /= 20000
        self.elevator /= 20000
        self.throttle /= 60000
        self.rudder /= 20000
        self.channel5 /= 20000
        self.flaps /= 20000
        self.channel7 /= 20000
        self.channel8 /= 20000

# Message: pilot_v2
# Id: 20
class pilot_v2():
    id = 20
    _pack_string = "<BdhhhhhhhhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.channel = [0.0] * 8
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.channel[0] * 20000)),
                  int(round(self.channel[1] * 20000)),
                  int(round(self.channel[2] * 20000)),
                  int(round(self.channel[3] * 20000)),
                  int(round(self.channel[4] * 20000)),
                  int(round(self.channel[5] * 20000)),
                  int(round(self.channel[6] * 20000)),
                  int(round(self.channel[7] * 20000)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.channel[0],
         self.channel[1],
         self.channel[2],
         self.channel[3],
         self.channel[4],
         self.channel[5],
         self.channel[6],
         self.channel[7],
         self.status) = self._struct.unpack(msg)
        self.channel[0] /= 20000
        self.channel[1] /= 20000
        self.channel[2] /= 20000
        self.channel[3] /= 20000
        self.channel[4] /= 20000
        self.channel[5] /= 20000
        self.channel[6] /= 20000
        self.channel[7] /= 20000

# Message: pilot_v3
# Id: 38
class pilot_v3():
    id = 38
    _pack_string = "<BfhhhhhhhhB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.channel = [0.0] * 8
        self.status = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.channel[0] * 20000)),
                  int(round(self.channel[1] * 20000)),
                  int(round(self.channel[2] * 20000)),
                  int(round(self.channel[3] * 20000)),
                  int(round(self.channel[4] * 20000)),
                  int(round(self.channel[5] * 20000)),
                  int(round(self.channel[6] * 20000)),
                  int(round(self.channel[7] * 20000)),
                  self.status)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.channel[0],
         self.channel[1],
         self.channel[2],
         self.channel[3],
         self.channel[4],
         self.channel[5],
         self.channel[6],
         self.channel[7],
         self.status) = self._struct.unpack(msg)
        self.channel[0] /= 20000
        self.channel[1] /= 20000
        self.channel[2] /= 20000
        self.channel[3] /= 20000
        self.channel[4] /= 20000
        self.channel[5] /= 20000
        self.channel[6] /= 20000
        self.channel[7] /= 20000

# Message: ap_status_v4
# Id: 30
class ap_status_v4():
    id = 30
    _pack_string = "<BdhhHHhhHHddHHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.groundtrack_deg = 0.0
        self.roll_deg = 0.0
        self.altitude_msl_ft = 0
        self.altitude_ground_m = 0
        self.pitch_deg = 0.0
        self.airspeed_kt = 0.0
        self.flight_timer = 0
        self.target_waypoint_idx = 0
        self.wp_longitude_deg = 0.0
        self.wp_latitude_deg = 0.0
        self.wp_index = 0
        self.route_size = 0
        self.sequence_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.groundtrack_deg * 10)),
                  int(round(self.roll_deg * 10)),
                  self.altitude_msl_ft,
                  self.altitude_ground_m,
                  int(round(self.pitch_deg * 10)),
                  int(round(self.airspeed_kt * 10)),
                  self.flight_timer,
                  self.target_waypoint_idx,
                  self.wp_longitude_deg,
                  self.wp_latitude_deg,
                  self.wp_index,
                  self.route_size,
                  self.sequence_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.groundtrack_deg,
         self.roll_deg,
         self.altitude_msl_ft,
         self.altitude_ground_m,
         self.pitch_deg,
         self.airspeed_kt,
         self.flight_timer,
         self.target_waypoint_idx,
         self.wp_longitude_deg,
         self.wp_latitude_deg,
         self.wp_index,
         self.route_size,
         self.sequence_num) = self._struct.unpack(msg)
        self.groundtrack_deg /= 10
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.airspeed_kt /= 10

# Message: ap_status_v5
# Id: 32
class ap_status_v5():
    id = 32
    _pack_string = "<BdBhhHHhhHHddHHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.flags = 0
        self.groundtrack_deg = 0.0
        self.roll_deg = 0.0
        self.altitude_msl_ft = 0
        self.altitude_ground_m = 0
        self.pitch_deg = 0.0
        self.airspeed_kt = 0.0
        self.flight_timer = 0
        self.target_waypoint_idx = 0
        self.wp_longitude_deg = 0.0
        self.wp_latitude_deg = 0.0
        self.wp_index = 0
        self.route_size = 0
        self.sequence_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.flags,
                  int(round(self.groundtrack_deg * 10)),
                  int(round(self.roll_deg * 10)),
                  self.altitude_msl_ft,
                  self.altitude_ground_m,
                  int(round(self.pitch_deg * 10)),
                  int(round(self.airspeed_kt * 10)),
                  self.flight_timer,
                  self.target_waypoint_idx,
                  self.wp_longitude_deg,
                  self.wp_latitude_deg,
                  self.wp_index,
                  self.route_size,
                  self.sequence_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.flags,
         self.groundtrack_deg,
         self.roll_deg,
         self.altitude_msl_ft,
         self.altitude_ground_m,
         self.pitch_deg,
         self.airspeed_kt,
         self.flight_timer,
         self.target_waypoint_idx,
         self.wp_longitude_deg,
         self.wp_latitude_deg,
         self.wp_index,
         self.route_size,
         self.sequence_num) = self._struct.unpack(msg)
        self.groundtrack_deg /= 10
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.airspeed_kt /= 10

# Message: ap_status_v6
# Id: 33
class ap_status_v6():
    id = 33
    _pack_string = "<BdBhhHHhhHHddHHBHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.flags = 0
        self.groundtrack_deg = 0.0
        self.roll_deg = 0.0
        self.altitude_msl_ft = 0
        self.altitude_ground_m = 0
        self.pitch_deg = 0.0
        self.airspeed_kt = 0.0
        self.flight_timer = 0
        self.target_waypoint_idx = 0
        self.wp_longitude_deg = 0.0
        self.wp_latitude_deg = 0.0
        self.wp_index = 0
        self.route_size = 0
        self.task_id = 0
        self.task_attribute = 0
        self.sequence_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.flags,
                  int(round(self.groundtrack_deg * 10)),
                  int(round(self.roll_deg * 10)),
                  self.altitude_msl_ft,
                  self.altitude_ground_m,
                  int(round(self.pitch_deg * 10)),
                  int(round(self.airspeed_kt * 10)),
                  self.flight_timer,
                  self.target_waypoint_idx,
                  self.wp_longitude_deg,
                  self.wp_latitude_deg,
                  self.wp_index,
                  self.route_size,
                  self.task_id,
                  self.task_attribute,
                  self.sequence_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.flags,
         self.groundtrack_deg,
         self.roll_deg,
         self.altitude_msl_ft,
         self.altitude_ground_m,
         self.pitch_deg,
         self.airspeed_kt,
         self.flight_timer,
         self.target_waypoint_idx,
         self.wp_longitude_deg,
         self.wp_latitude_deg,
         self.wp_index,
         self.route_size,
         self.task_id,
         self.task_attribute,
         self.sequence_num) = self._struct.unpack(msg)
        self.groundtrack_deg /= 10
        self.roll_deg /= 10
        self.pitch_deg /= 10
        self.airspeed_kt /= 10

# Message: ap_status_v7
# Id: 39
class ap_status_v7():
    id = 39
    _pack_string = "<BfBhhHHhhHHddHHBHB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.flags = 0
        self.groundtrack_deg = 0.0
        self.roll_deg = 0.0
        self.altitude_msl_ft = 0.0
        self.altitude_ground_m = 0.0
        self.pitch_deg = 0.0
        self.airspeed_kt = 0.0
        self.flight_timer = 0.0
        self.target_waypoint_idx = 0
        self.wp_longitude_deg = 0.0
        self.wp_latitude_deg = 0.0
        self.wp_index = 0
        self.route_size = 0
        self.task_id = 0
        self.task_attribute = 0
        self.sequence_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.flags,
                  int(round(self.groundtrack_deg * 10)),
                  int(round(self.roll_deg * 10)),
                  int(round(self.altitude_msl_ft * 1)),
                  int(round(self.altitude_ground_m * 1)),
                  int(round(self.pitch_deg * 10)),
                  int(round(self.airspeed_kt * 10)),
                  int(round(self.flight_timer * 1)),
                  self.target_waypoint_idx,
                  self.wp_longitude_deg,
                  self.wp_latitude_deg,
                  self.wp_index,
                  self.route_size,
                  self.task_id,
                  self.task_attribute,
                  self.sequence_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.flags,
         self.groundtrack_deg,
         self.roll_deg,
         self.altitude_msl_ft,
         self.altitude_ground_m,
         self.pitch_deg,
         self.airspeed_kt,
         self.flight_timer,
         self.target_waypoint_idx,
         self.wp_longitude_deg,
         self.wp_latitude_deg,
         self.wp_index,
         self.route_size,
         self.task_id,
         self.task_attribute,
         self.sequence_num) = self._struct.unpack(msg)
        self.groundtrack_deg /= 10
        self.roll_deg /= 10
        self.altitude_msl_ft /= 1
        self.altitude_ground_m /= 1
        self.pitch_deg /= 10
        self.airspeed_kt /= 10
        self.flight_timer /= 1

# Message: system_health_v4
# Id: 19
class system_health_v4():
    id = 19
    _pack_string = "<BdHHHHHH"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.system_load_avg = 0.0
        self.avionics_vcc = 0.0
        self.main_vcc = 0.0
        self.cell_vcc = 0.0
        self.main_amps = 0.0
        self.total_mah = 0.0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.system_load_avg * 100)),
                  int(round(self.avionics_vcc * 1000)),
                  int(round(self.main_vcc * 1000)),
                  int(round(self.cell_vcc * 1000)),
                  int(round(self.main_amps * 1000)),
                  int(round(self.total_mah * 10)))
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.system_load_avg,
         self.avionics_vcc,
         self.main_vcc,
         self.cell_vcc,
         self.main_amps,
         self.total_mah) = self._struct.unpack(msg)
        self.system_load_avg /= 100
        self.avionics_vcc /= 1000
        self.main_vcc /= 1000
        self.cell_vcc /= 1000
        self.main_amps /= 1000
        self.total_mah /= 10

# Message: system_health_v5
# Id: 41
class system_health_v5():
    id = 41
    _pack_string = "<BfHHHHHH"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.system_load_avg = 0.0
        self.avionics_vcc = 0.0
        self.main_vcc = 0.0
        self.cell_vcc = 0.0
        self.main_amps = 0.0
        self.total_mah = 0.0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.system_load_avg * 100)),
                  int(round(self.avionics_vcc * 1000)),
                  int(round(self.main_vcc * 1000)),
                  int(round(self.cell_vcc * 1000)),
                  int(round(self.main_amps * 1000)),
                  int(round(self.total_mah * 0.1)))
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.system_load_avg,
         self.avionics_vcc,
         self.main_vcc,
         self.cell_vcc,
         self.main_amps,
         self.total_mah) = self._struct.unpack(msg)
        self.system_load_avg /= 100
        self.avionics_vcc /= 1000
        self.main_vcc /= 1000
        self.cell_vcc /= 1000
        self.main_amps /= 1000
        self.total_mah /= 0.1

# Message: system_health_v6
# Id: 46
class system_health_v6():
    id = 46
    _pack_string = "<BfHHHHHHH"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.system_load_avg = 0.0
        self.fmu_timer_misses = 0
        self.avionics_vcc = 0.0
        self.main_vcc = 0.0
        self.cell_vcc = 0.0
        self.main_amps = 0.0
        self.total_mah = 0.0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  int(round(self.system_load_avg * 100)),
                  self.fmu_timer_misses,
                  int(round(self.avionics_vcc * 1000)),
                  int(round(self.main_vcc * 1000)),
                  int(round(self.cell_vcc * 1000)),
                  int(round(self.main_amps * 1000)),
                  int(round(self.total_mah * 0.1)))
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.system_load_avg,
         self.fmu_timer_misses,
         self.avionics_vcc,
         self.main_vcc,
         self.cell_vcc,
         self.main_amps,
         self.total_mah) = self._struct.unpack(msg)
        self.system_load_avg /= 100
        self.avionics_vcc /= 1000
        self.main_vcc /= 1000
        self.cell_vcc /= 1000
        self.main_amps /= 1000
        self.total_mah /= 0.1

# Message: payload_v2
# Id: 23
class payload_v2():
    id = 23
    _pack_string = "<BdH"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.trigger_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.trigger_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.trigger_num) = self._struct.unpack(msg)

# Message: payload_v3
# Id: 42
class payload_v3():
    id = 42
    _pack_string = "<BfH"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.trigger_num = 0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  self.trigger_num)
        return msg

    def unpack(self, msg):
        (self.index,
         self.timestamp_sec,
         self.trigger_num) = self._struct.unpack(msg)

# Message: event_v1
# Id: 27
class event_v1():
    id = 27
    _pack_string = "<BdB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.index = 0
        self.timestamp_sec = 0.0
        self.message = ""
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.index,
                  self.timestamp_sec,
                  len(self.message))
        msg += str.encode(self.message)
        return msg

    def unpack(self, msg):
        base_len = struct.calcsize(self._pack_string)
        extra = msg[base_len:]
        msg = msg[:base_len]
        (self.index,
         self.timestamp_sec,
         self.message_len) = self._struct.unpack(msg)
        self.message = extra[:self.message_len].decode()
        extra = extra[self.message_len:]

# Message: event_v2
# Id: 44
class event_v2():
    id = 44
    _pack_string = "<fBB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.timestamp_sec = 0.0
        self.sequence_num = 0
        self.message = ""
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.timestamp_sec,
                  self.sequence_num,
                  len(self.message))
        msg += str.encode(self.message)
        return msg

    def unpack(self, msg):
        base_len = struct.calcsize(self._pack_string)
        extra = msg[base_len:]
        msg = msg[:base_len]
        (self.timestamp_sec,
         self.sequence_num,
         self.message_len) = self._struct.unpack(msg)
        self.message = extra[:self.message_len].decode()
        extra = extra[self.message_len:]

# Message: command_v1
# Id: 28
class command_v1():
    id = 28
    _pack_string = "<BB"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.sequence_num = 0
        self.message = ""
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.sequence_num,
                  len(self.message))
        msg += str.encode(self.message)
        return msg

    def unpack(self, msg):
        base_len = struct.calcsize(self._pack_string)
        extra = msg[base_len:]
        msg = msg[:base_len]
        (self.sequence_num,
         self.message_len) = self._struct.unpack(msg)
        self.message = extra[:self.message_len].decode()
        extra = extra[self.message_len:]

# Message: stream_v1
# Id: 49
class stream_v1():
    id = 49
    _pack_string = "<fff"
    _struct = struct.Struct(_pack_string)

    def __init__(self, msg=None):
        # public fields
        self.sigma1 = 0.0
        self.sigma2 = 0.0
        self.sigma3 = 0.0
        # unpack if requested
        if msg: self.unpack(msg)

    def pack(self):
        msg = self._struct.pack(
                  self.sigma1,
                  self.sigma2,
                  self.sigma3)
        return msg

    def unpack(self, msg):
        (self.sigma1,
         self.sigma2,
         self.sigma3) = self._struct.unpack(msg)

