/**
 * \file: gps_ublox9.h
 *
 * u-blox 7 protocol driver
 *
 * Copyright Curt Olson curtolson@flightgear.org
 *
 */

#pragma once

#include <props2.h>

#include "drivers/driver.h"

class ublox9_t: public driver_t {
    
public:
    ublox9_t() {}
    ~ublox9_t() {}
    void init( PropertyNode *config );
    float read();
    void process() {}
    void write() {};
    void close();
    void command( const char *cmd ) {}

private:
    PropertyNode gps_node;
    int gps_fix_value = 0;
    int fd = -1;
    static const int max_payload = 2048;
    uint8_t payload[max_payload];
    int state = 0;
    int msg_class = 0, msg_id = 0;
    int length_lo = 0, length_hi = 0, payload_length = 0;
    int counter = 0;
    uint8_t cksum_A = 0, cksum_B = 0, cksum_lo = 0, cksum_hi = 0;
    bool open( const char *device_name, const int baud );
    bool read_ublox9();
    bool parse_msg();
};
