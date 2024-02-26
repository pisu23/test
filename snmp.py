from pysnmp.hlapi import *

def snmp_request():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget(('127.0.0.1', 1024)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )

    if errorIndication:
        return str(errorIndication)
    elif errorStatus:
        return '%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
    else:
        return ', '.join([' = '.join([x.prettyPrint() for x in varBind]) for varBind in varBinds])