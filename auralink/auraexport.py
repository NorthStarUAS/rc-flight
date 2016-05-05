#!/usr/bin/python

import argparse
import os
import sys
import tempfile

from props import root, getNode

sys.path.append("../src")
import comms.packer

import commands
import current
import parser

def logical_category(id):
    if id == parser.GPS_PACKET_V1 or id == parser.GPS_PACKET_V2:
        return 'gps'
    elif id == parser.IMU_PACKET_V1 or id == parser.IMU_PACKET_V2 \
         or id == parser.IMU_PACKET_V3:
        return 'imu'
    elif id == parser.AIRDATA_PACKET_V3 or id == parser.AIRDATA_PACKET_V4 \
         or id == parser.AIRDATA_PACKET_V5:
        return 'air'
    elif id == parser.FILTER_PACKET_V1 or id == parser.FILTER_PACKET_V2:
        return 'filter'
    elif id == parser.ACTUATOR_PACKET_V1 or id == parser.ACTUATOR_PACKET_V2:
        return 'act'
    elif id == parser.PILOT_INPUT_PACKET_V1 \
         or id == parser.PILOT_INPUT_PACKET_V2:
        return 'pilot'
    elif id == parser.AP_STATUS_PACKET_V1 or id == parser.AP_STATUS_PACKET_V2 \
         or id == parser.AP_STATUS_PACKET_V3:
        return 'ap'
    elif id == parser.SYSTEM_HEALTH_PACKET_V2 \
         or id == parser.SYSTEM_HEALTH_PACKET_V3 \
         or id == parser.SYSTEM_HEALTH_PACKET_V4:
        return 'health'
    elif id == parser.PAYLOAD_PACKET_V1 or id == parser.PAYLOAD_PACKET_V2:
        return 'payload'

# When a binary record of some id is read, it gets parsed into the
# property tree structure.  The following code simple calls the
# appropriate text packer function for the given id to extract the
# same data back out of the property tree and format it as a text
# record.
def generate_record(category, index, delim=','):
    if category == 'gps':
        record = comms.packer.pack_gps_text(index, delim)
        return record
    elif category == 'imu':
        record = comms.packer.pack_imu_text(index, delim)
        return record
    elif category == 'air':
        record = comms.packer.pack_airdata_text(index, delim)
        return record
    elif category == 'filter':
        record = comms.packer.pack_filter_text(index, delim)
        return record
    elif category == 'act':
        record = comms.packer.pack_act_text(index, delim)
        return record
    elif category == 'pilot':
        record = comms.packer.pack_pilot_text(index, delim)
        return record
    elif category == 'ap':
        record = comms.packer.pack_ap_status_text(index, delim)
        return record
    elif category == 'health':
        record = comms.packer.pack_system_health_text(index, delim)
        return record
    elif category == 'payload':
        record = comms.packer.pack_payload_text(index, delim)
        return record
    # remote_link_node.setInt('sequence_num', result[14]) # include in system health....


argparser = argparse.ArgumentParser(description='aura export')
argparser.add_argument('--flight', help='load specified flight log')
argparser.add_argument('--skip-seconds', help='seconds to skip when processing flight log')

args = argparser.parse_args()

data = {}

if args.flight:
    filename = args.flight
    if args.flight.endswith('.gz'):
        (fd, filename) = tempfile.mkstemp()
        command = 'zcat ' + args.flight + ' > ' + filename
        print command
        os.system(command)
    try:
        fd = open(filename, 'r')
        full = fd.read()
        if args.flight.endswith('.gz'):
            # remove temporary file name
            os.remove(filename)
    except:
        # eat the expected error
        print 'we should be able to ignore the zcat error'

    print 'len of decompressed file:', len(full)

    while True:
        try:
            (id, index) = parser.file_read(full)
            category = logical_category(id)
            record = generate_record(category, index)
            key = '%s-%d' % (category, index)
            if key in data:
                data[key].append(record)
            else:
                data[key] = [ record ]
        except:
            print 'end of file'
            break
else:
    print 'A flight log file must be provided'

for key in sorted(data):
    print key, ':', len(data[key])
