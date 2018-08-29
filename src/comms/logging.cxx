#include "python/pyprops.hxx"
#include "util/sg_path.hxx"

#include "logging.hxx"


pyModuleLogging::pyModuleLogging()
{
}

bool pyModuleLogging::open(const char *path)
{
    if (pModuleObj == NULL) {
	printf("ERROR: events.init() failed\n");
	return false;
    }
    PyObject *pFuncOpen = PyObject_GetAttrString(pModuleObj, "open");
    if ( pFuncOpen == NULL || ! PyCallable_Check(pFuncOpen) ) {
	if ( PyErr_Occurred() ) PyErr_Print();
	printf("ERROR: cannot find function 'open()'\n");
	return false;
    }

    // FIXME decref pFuncOpen
    
    PyObject *pValue = PyObject_CallFunction(pFuncOpen, (char *)"s", path);
    if (pValue != NULL) {
	bool result = PyObject_IsTrue(pValue);
	Py_DECREF(pValue);
	return result;
    } else {
	PyErr_Print();
	printf("ERROR: call failed\n");
	return false;
    }
    return false;
}

void pyModuleLogging::update() {
    if (pModuleObj == NULL) {
	printf("ERROR: import logging module failed\n");
	return;
    }
    PyObject *pFuncLog = PyObject_GetAttrString(pModuleObj, "update");
    if ( pFuncLog == NULL || ! PyCallable_Check(pFuncLog) ) {
	if ( PyErr_Occurred() ) PyErr_Print();
	printf("ERROR: cannot find function 'update_configs()'\n");
	return;
    }
    PyObject *pResult = PyObject_CallFunction(pFuncLog, NULL);
    if (pResult != NULL) {
	Py_DECREF(pResult);
	return;
    } else {
	PyErr_Print();
	printf("ERROR: call failed\n");
	return;
    }
}


// FIXME: close log file!
bool pyModuleLogging::close()
{
    return true;
}

void pyModuleLogging::log_message( uint8_t *buf, int size ) {
    if (pModuleObj == NULL) {
	printf("ERROR: import logging module failed\n");
	return;
    }
    PyObject *pFuncLog = PyObject_GetAttrString(pModuleObj, "log_message");
    if ( pFuncLog == NULL || ! PyCallable_Check(pFuncLog) ) {
	if ( PyErr_Occurred() ) PyErr_Print();
	printf("ERROR: cannot find function 'log_message()'\n");
	return;
    }
    PyObject *pResult = PyObject_CallFunction(pFuncLog, (char *)"y#", buf, size);
    if (pResult != NULL) {
	Py_DECREF(pResult);
	return;
    } else {
	PyErr_Print();
	printf("ERROR: call failed\n");
	return;
    }
}

void pyModuleLogging::write_configs() {
    if (pModuleObj == NULL) {
	printf("ERROR: import logging module failed\n");
	return;
    }
    PyObject *pFuncLog = PyObject_GetAttrString(pModuleObj, "write_configs");
    if ( pFuncLog == NULL || ! PyCallable_Check(pFuncLog) ) {
	if ( PyErr_Occurred() ) PyErr_Print();
	printf("ERROR: cannot find function 'write_configs()'\n");
	return;
    }
    PyObject *pResult = PyObject_CallFunction(pFuncLog, NULL);
    if (pResult != NULL) {
	Py_DECREF(pResult);
	return;
    } else {
	PyErr_Print();
	printf("ERROR: call failed\n");
	return;
    }
}


// write out the imu calibration parameters associated with this data
// (this allows us to later rederive the original raw sensor values.)
bool write_imu_calibration( pyPropertyNode *config ) {
    pyPropertyNode logging_node = pyGetNode( "/config/logging", true );
    SGPath jsonfile = logging_node.getString("flight_dir");
    jsonfile.append( "imucal.json" );
    writeJSON( jsonfile.str(), config );
    return true;
}
