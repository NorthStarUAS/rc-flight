//
// globals.cxx - global references
//
// Written by Curtis Olson, curtolson <at> gmail <dot> com.
// Started Fall 2009.
// This code is released into the public domain.
// 

#include "globals.hxx"


UGPacketizer *packetizer = NULL;
UGTelnet *telnet = NULL;
AuraCircleMgr *circle_mgr = NULL;
FGRouteMgr *route_mgr = NULL;
pyModuleBase *mission_mgr = NULL;


bool AuraCoreInit() {
    packetizer = new UGPacketizer;
    circle_mgr = new AuraCircleMgr;
    route_mgr = new FGRouteMgr;
    mission_mgr = new pyModuleBase;

    return true;
}
