#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "mcgredo"
__date__ = "$Jun 23, 2015 10:27:29 AM$"

import socket
import time
import sys
import binascii
import struct

sys.path.append("../dis_io")
sys.path.append("../distributed_interactive_simulation")

from DataInputStream import DataInputStream
from DataOutputStream import DataOutputStream

from dis7 import ElectronicEmissionsPdu
from dis7 import EmitterSystem
from dis7 import BeamData
from io import BytesIO

    
UDP_PORT = 3000
DESTINATION_ADDRESS = "192.168.0.255"

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:  
    pdu1 = ElectronicEmissionsPdu()
    pdu1.protocolVersion = 6
    pdu1.exerciseID = 1
    pdu1.emittingEntityID.entityID = 1
    pdu1.emittingEntityID.siteID = 1
    pdu1.emittingEntityID.applicationID = 11031
    
    systemNav = EmitterSystem()
    systemNav.emitterName = 25696
    systemNav.emitterIDNumber = 8
    
    beamNav = BeamData()
    beamNav.beamNumber = 7
    beamNav.fundamentalParameterData.frequency = 1450000
    beamNav.beamParameterIndex = 555
    systemNav.beams.append(beamNav)
    
    beamNav2 = BeamData()
    beamNav2.beamNumber = 8
    beamNav2.fundamentalParameterData.frequency = 1450000
    beamNav2.beamParameterIndex = 555
    systemNav.beams.append(beamNav2)

    pdu1.systems.append(systemNav)
    
    pdu2 = ElectronicEmissionsPdu()
    pdu2.protocolVersion = 6
    pdu2.exerciseID = 1
    pdu2.emittingEntityID.entityID = 1
    pdu2.emittingEntityID.siteID = 1
    pdu2.emittingEntityID.applicationID = 11031
    
    system2D = EmitterSystem()
    system2D.emitterName = 6975
    system2D.emitterIDNumber = 5
    
    beam2D = BeamData()
    beam2D.beamNumber = 7
    beam2D.fundamentalParameterData.frequency = 1450000
    beam2D.beamParameterIndex = 555
    system2D.beams.append(beam2D)
    beam2D2 = BeamData()
    beam2D2.beamNumber = 8
    beam2D2.fundamentalParameterData.frequency = 1450000
    beam2D2.beamParameterIndex = 555
    system2D.beams.append(beam2D2)

    pdu2.systems.append(system2D)   

    #members = [attr for attr in dir(pdu) if not callable(attr) and not attr.startswith("__")]
    #print members
    
    memoryStream = BytesIO()
    outputStream = DataOutputStream(memoryStream)
    pdu1.serialize(outputStream)
    data = memoryStream.getvalue()
    udpSocket.sendto(data, (DESTINATION_ADDRESS, UDP_PORT))
    time.sleep(0.01)
    memoryStream = BytesIO()
    outputStream = DataOutputStream(memoryStream)
    pdu2.serialize(outputStream)
    data = memoryStream.getvalue()
    udpSocket.sendto(data, (DESTINATION_ADDRESS, UDP_PORT))

    time.sleep(1)
    print "sent message"

if __name__ == "__main__":
    print "Hello World";
