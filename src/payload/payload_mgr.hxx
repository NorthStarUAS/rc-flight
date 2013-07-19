/**
 * \file: payload_mgr.h
 *
 * Top level payload manager
 *
 * Copyright (C) 2013 - Curtis L. Olson curtolson@gmail.com
 */


#ifndef _UGEAR_PAYLOAD_MGR_H
#define _UGEAR_PAYLOAD_MGR_H


#include "props/props.hxx"


class UGPayloadMgr {

private:

    // payload configuration tree
    // SGPropertyNode *config_props;

public:

    UGPayloadMgr();
    ~UGPayloadMgr();

    void bind();
    void init();
    bool update();
    void close();

};


// global reference to payload mgr (move to globals?)
extern UGPayloadMgr payload_mgr;


#endif // _UGEAR_PAYLOAD_MGR_H