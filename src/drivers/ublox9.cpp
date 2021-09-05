/**
 * \file: gps_ublox9.cpp
 *
 * u-blox 9 protocol driver
 *
 * Copyright (C) 2012 - 2020 Curtis L. Olson - curtolson@flightgear.org
 *
 */

#include <pyprops.h>

#include <errno.h>		// errno
#include <sys/types.h>		// open()
#include <sys/stat.h>		// open()
#include <fcntl.h>		// open()
#include <stdio.h>		// printf() et. al.
#include <termios.h>		// tcgetattr() et. al.
#include <unistd.h>		// tcgetattr() et. al.
#include <string.h>		// memset()
#include <sys/time.h>		// gettimeofday()
#include <time.h>
#include <string>
using std::string;

#include "include/globaldefs.h"

#include "util/props_helper.h"
#include "util/strutils.h"
#include "util/timing.h"

#include "ublox9.h"

#pragma pack(push, 1)           // set alignment to 1 byte boundary
struct nav_pvt_t {
    uint32_t iTOW;
    int16_t year;
    uint8_t month;
    uint8_t day;
    uint8_t hour;
    uint8_t min;
    uint8_t sec;
    uint8_t valid;
    uint32_t tAcc;
    int32_t nano;
    uint8_t fixType;
    uint8_t flags;
    uint8_t flags2;
    uint8_t numSV;
    int32_t lon;
    int32_t lat;
    int32_t height;
    int32_t hMSL;
    uint32_t hAcc;
    uint32_t vAcc;
    int32_t velN;
    int32_t velE;
    int32_t velD;
    uint32_t gSpeed;
    int32_t heading;
    uint32_t sAcc;
    uint32_t headingAcc;
    uint16_t pDOP;
    uint8_t reserved[6];
    int32_t headVeh;
    int16_t magDec;
    uint16_t magAcc;
};
struct rxm_raw_head_t {
    double rcvTow;
    uint16_t week;
    int8_t leapS;
    uint8_t numMeas;
    uint8_t recStat;
    uint8_t version;
    uint8_t reserved1_1;
    uint8_t reserved1_2;
};
struct rxm_raw_record_t {
    double prMes;
    double cpMes;
    float doMes;
    uint8_t gnssId;
    uint8_t svId;
    uint8_t sigId;
    uint8_t freqId;
    uint16_t locktime;
    uint8_t cno;
    uint8_t prStdev;
    uint8_t cpStdev;
    uint8_t doStdev;
    uint8_t trkStat;
    uint8_t reserved2;
};
struct rxm_sfrbx_head_t {
    uint8_t gnssId;
    uint8_t svId;
    uint8_t reserved1;
    uint8_t freqId;
    uint8_t numWords;
    uint8_t chn;
    uint8_t version;
    uint8_t reserve2;
};
# pragma pack(pop)              // restore original alignment

bool ublox9_t::open( const char *device_name, const int baud ) {
    if ( verbose ) {
	printf("ublox9 on %s (%d baud)\n", device_name, baud);
    }

    fd = ::open( device_name, O_RDWR | O_NOCTTY | O_NONBLOCK );
    if ( fd < 0 ) {
        fprintf( stderr, "open serial: unable to open %s - %s\n",
                 device_name, strerror(errno) );
	return false;
    }

    struct termios config; 	// Serial port settings
    memset(&config, 0, sizeof(config));

    // Save Current Serial Port Settings
    // tcgetattr(fd,&oldTio); 

    int config_baud = B115200;
    if ( baud == 115200 ) {
	config_baud = B115200;
    } else if ( baud == 57600 ) {
	config_baud = B57600;
    } else if ( baud == 9600 ) {
	config_baud = B9600;
    } else {
	fprintf( stderr, "ublox9 baud rate (%d) unsupported by driver, using back to 115200.\n", baud);
    }

    // Configure New Serial Port Settings
    config.c_cflag     = config_baud | // bps rate
                         CS8	 | // 8n1
                         CLOCAL	 | // local connection, no modem
                         CREAD;	   // enable receiving chars
    config.c_iflag     = IGNPAR;   // ignore parity bits
    config.c_oflag     = 0;
    config.c_lflag     = 0;
    config.c_cc[VTIME] = 0;
    config.c_cc[VMIN]  = 0;	   // block 'read' from returning until at
                                   // least 0 character is received

    // Flush Serial Port I/O buffer
    tcflush(fd, TCIOFLUSH);

    // Set New Serial Port Settings
    int ret = tcsetattr( fd, TCSANOW, &config );
    if ( ret > 0 ) {
        fprintf( stderr, "error configuring device: %s - %s\n",
                 device_name, strerror(errno) );
	return false;
    }

    // Enable non-blocking IO (one more time for good measure)
    fcntl(fd, F_SETFL, O_NONBLOCK);

    return true;
}

void ublox9_t::init( PropertyNode *config ) {
    string output_path = get_next_path("/sensors", "gps", false);
    gps_node = PropertyNode( output_path.c_str() );
    if ( config->hasChild("device") ) {
        string device = config->getString("device");
        int baud = config->getInt("baud");
        if ( open(device.c_str(), baud) ) {
            printf("ublox9 device opened: %s\n", device.c_str());
        } else {
            printf("unable to open ublox9 device: %s\n", device.c_str());
        }
    } else {
        printf("no ublox9 device specified\n");
    }
}

bool ublox9_t::parse_msg() {
    bool new_position = false;

    if ( msg_class == 0x01 && msg_id == 0x02 ) {
	// NAV-POSLLH: Please refer to the ublox6 driver (here or in the
	// code history) for a nav-posllh parser
    } else if ( msg_class == 0x01 && msg_id == 0x06 ) {
	// NAV-SOL: Please refer to the ublox6 driver (here or in the
	// code history) for a nav-sol parser that transforms eced
	// pos/vel to lla pos/ned vel.
    } else if ( msg_class == 0x01 && msg_id == 0x07 ) {
        // NAV-PVT
        if ( payload_length == sizeof(nav_pvt_t) )  {
            nav_pvt_t data;
            memcpy( &data, payload, payload_length );

            gps_fix_value = data.fixType;
            if ( gps_fix_value == 0 ) {
                gps_node.setInt( "status", 0 );
            } else if ( gps_fix_value == 1 || gps_fix_value == 2 ) {
                gps_node.setInt( "status", 1 );
            } else if ( gps_fix_value == 3 ) {
                gps_node.setInt( "status", 2 );
            }
            // printf("fix: %d lon: %.8f lat: %.8f\n", fixType, (double)lon, (double)lat);

            if ( data.fixType == 3 ) {
                // gps thinks we have a good 3d fix so flag our data good.
                new_position = true;
            }

            gps_node.setDouble( "timestamp", get_Time() );

            struct tm gps_time;
            gps_time.tm_sec = data.sec;
            gps_time.tm_min = data.min;
            gps_time.tm_hour = data.hour;
            gps_time.tm_mday = data.day;
            gps_time.tm_mon = data.month - 1;
            gps_time.tm_year = data.year - 1900;
            double unix_sec = (double)mktime( &gps_time ) - timezone;
            unix_sec += data.nano / 1000000000.0;
            gps_node.setDouble( "unix_time_sec", unix_sec );
            gps_node.setDouble( "time_accuracy_ns", data.tAcc );
	    
            gps_node.setInt( "num_sats", data.numSV );
	    
            gps_node.setDouble( "latitude_deg", (double)data.lat / 10000000.0);
            gps_node.setDouble( "longitude_deg", (double)data.lon / 10000000.0);
            gps_node.setDouble( "altitude_m", (float)data.hMSL / 1000.0 );
            gps_node.setDouble( "vn_mps", (float)data.velN / 1000.0 );
            gps_node.setDouble( "ve_mps", (float)data.velE / 1000.0 );
            gps_node.setDouble( "vd_mps", (float)data.velD / 1000.0 );
            gps_node.setDouble( "horiz_accuracy_m", data.hAcc / 1000.0 );
            gps_node.setDouble( "vert_accuracy_m", data.vAcc / 1000.0 );
            gps_node.setDouble( "groundspeed_ms", data.gSpeed / 1000.0 );
            gps_node.setDouble( "groundtrack_deg", data.heading / 100000.0 );
            gps_node.setDouble( "heading_accuracy_deg", data.headingAcc / 100000.0 );
            gps_node.setDouble( "pdop", data.pDOP / 100.0 );
            gps_node.setInt( "fixType", data.fixType);
        } else {
            printf("NAV-PVT message size mismatch!\n");
        }
    } else if ( msg_class == 0x01 && msg_id == 0x12 ) {
	// NAV-VELNED: Please refer to the ublox6 driver (here or in the
	// code history) for a nav-velned parser
    } else if ( msg_class == 0x01 && msg_id == 0x21 ) {
	// NAV-TIMEUTC: Please refer to the ublox6 driver (here or in the
	// code history) for a nav-timeutc parser
    } else if ( msg_class == 0x01 && msg_id == 0x30 ) {
	// NAV-SVINFO (partial parse)
	uint8_t *p = payload;
	// uint32_t iTOW = *((uint32_t *)(p+0));
	uint8_t numCh = p[4];
	// uint8_t globalFlags = p[5];
	int satUsed = 0;
	for ( int i = 0; i < numCh; i++ ) {
	    // uint8_t satid = p[9 + 12*i];
	    // uint8_t flags = p[10 + 12*i];
	    uint8_t quality = p[11 + 12*i];
	    // printf(" chn=%d satid=%d flags=%d quality=%d\n", i, satid, flags, quality);
	    if ( quality > 3 ) {
		satUsed++;
	    }
	}
 	// gps_satellites_node.setInt( satUsed );
	if ( verbose && 0 ) {
	    if ( gps_fix_value < 3 ) {
		printf("Satellite count = %d/%d\n", satUsed, numCh);
	    }
	}
    } else if ( msg_class == 0x02 && msg_id == 0x13 ) {
        // RXM-SFRBX (Broadcast Navigation Data Subframe)
        // Ref (page 55): https://www.u-blox.com/sites/default/files/ZED-F9P_IntegrationManual_%28UBX-18010802%29.pdf
        // https://berthub.eu/articles/posts/galileo-notes/
        printf("RXM-SFRBX\n");
        rxm_sfrbx_head_t *p = (rxm_sfrbx_head_t *)payload;
        printf("gnssId: %d  svId: %d  numWords: %d  chn: %d  version: %d\n",
               p->gnssId, p->svId, p->numWords, p->chn, p->version);
        int size = sizeof(rxm_sfrbx_head_t) + p->numWords * 4;
        printf("Message size: %d (actual: %d)\n", size, payload_length);
    } else if ( msg_class == 0x02 && msg_id == 0x15 ) {
        // RXM-RAWX (Multi-GNSS Raw Measurement Data)
        // (for now just show that we can decode the message)
        // printf("RXM-RAWX\n");
        rxm_raw_head_t *p = (rxm_raw_head_t *)payload;
        // printf("rcvTow: %f\n", p->rcvTow);
        // printf("numMeas: %d\n", p->numMeas);
        int size = sizeof(rxm_raw_head_t) + p->numMeas * sizeof(rxm_raw_record_t);
        // printf("Message size: %d (actual: %d)\n", size, payload_length);
        if ( size == payload_length ) {
            for ( int i = 0; i < p->numMeas; i++ ) {
                uint8_t *base = (uint8_t *)p + sizeof(rxm_raw_head_t) + i*sizeof(rxm_raw_record_t);
                rxm_raw_record_t *r = (rxm_raw_record_t *)base;
                // printf("  id: %d pr: %f\n", r->svId, r->prMes);
            }
        } else {
            printf("RXM-RAWX problem decoding message or message length: %d %d %d\n", p->numMeas, size, payload_length);
}

        
    } else {
        printf("ublox9: unknown - msg class = %d  msg id = %d\n",
               msg_class, msg_id);
    }

    return new_position;
}

bool ublox9_t::read_ublox9() {
    int len;
    uint8_t input[500];

    // printf("read ublox9, entry state = %d\n", state);

    bool new_position = false;

    if ( state == 0 ) {
	counter = 0;
	cksum_A = cksum_B = 0;
	len = ::read( fd, input, 1 );
	while ( len > 0 && input[0] != 0xB5 ) {
	    // fprintf( stderr, "state0: len = %d val = %2X\n", len, input[0] );
	    len = ::read( fd, input, 1 );
	}
	if ( len > 0 && input[0] == 0xB5 ) {
	    // fprintf( stderr, "read 0xB5\n");
	    state++;
	}
    }
    if ( state == 1 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    if ( input[0] == 0x62 ) {
		// fprintf( stderr, "read 0x62\n");
		state++;
	    } else if ( input[0] == 0xB5 ) {
		// fprintf( stderr, "read 0xB5\n");
	    } else {
		state = 0;
	    }
	}
    }
    if ( state == 2 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    msg_class = input[0];
	    cksum_A += input[0];
	    cksum_B += cksum_A;
	    // fprintf( stderr, "msg class = %d\n", msg_class );
	    state++;
	}
    }
    if ( state == 3 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    msg_id = input[0];
	    cksum_A += input[0];
	    cksum_B += cksum_A;
	    // fprintf( stderr, "msg id = %d\n", msg_id );
	    state++;
	}
    }
    if ( state == 4 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    length_lo = input[0];
	    cksum_A += input[0];
	    cksum_B += cksum_A;
	    state++;
	}
    }
    if ( state == 5 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    length_hi = input[0];
	    cksum_A += input[0];
	    cksum_B += cksum_A;
	    payload_length = length_hi*256 + length_lo;
	    // fprintf( stderr, "payload len = %d\n", payload_length );
	    if ( payload_length > max_payload ) {
		state = 0;
	    } else {
		state++;
	    }
	}
    }
    if ( state == 6 ) {
	len = ::read( fd, input, 1 );
	while ( len > 0 ) {
	    payload[counter++] = input[0];
	    //fprintf( stderr, "%02X ", input[0] );
	    cksum_A += input[0];
	    cksum_B += cksum_A;
	    if ( counter >= payload_length ) {
		break;
	    }
	    len = ::read( fd, input, 1 );
	}

	if ( counter >= payload_length ) {
	    state++;
	    //fprintf( stderr, "\n" );
	}
    }
    if ( state == 7 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    cksum_lo = input[0];
	    state++;
	}
    }
    if ( state == 8 ) {
	len = ::read( fd, input, 1 );
	if ( len > 0 ) {
	    cksum_hi = input[0];
	    if ( cksum_A == cksum_lo && cksum_B == cksum_hi ) {
		// fprintf( stderr, "checksum passes (%d)!\n", msg_id );
		new_position = parse_msg();
		state++;
	    } else {
		if ( verbose && 0 ) {
		    printf("checksum failed %d %d (computed) != %d %d (message)\n",
			   cksum_A, cksum_B, cksum_lo, cksum_hi );
		}
	    }
	    // this is the end of a record, reset state to 0 to start
	    // looking for next record
	    state = 0;
	}
    }

    return new_position;
}

float ublox9_t::read() {
    // run an iteration of the ublox scanner/parser
    read_ublox9();
    return 0.0;
}

void ublox9_t::close() {
    ::close(fd);
}
