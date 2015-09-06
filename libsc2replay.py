#!/usr/bin/env python

from mpyq import mpyq
import protocol15405

class ReplayInfo:
    def __init__(self):
        self._stuff = {}
        self.map = ""
        self.players = {}
        self.rawdetails = {}
        self.ts = 0
        self.tzhrs = 0
        
    def log(self, output):
        self._stuff[len(self._stuff)] = output
        
    def getMap(self):
        return self.map
        
    def getPlayers(self):
        return self.players
        
    def getRawDetails(self):
        return self.rawdetails
        
    def getTS(self):
        return self.ts

    def getTZ(self):
        return self.tzhrs
        
    def loadreplay(self, replay_file):
        archive = mpyq.MPQArchive(replay_file)
        
        # Read the protocol header, this can be read with any protocol
        contents = archive.header['user_data_header']['content']
        header = protocol15405.decode_replay_header(contents)
        self.log(header)
        
        # The header's baseBuild determines which protocol to use
        baseBuild = header['m_version']['m_baseBuild']
        try:
            protocol = __import__('protocol%s' % (baseBuild,))
        except:
            return baseBuild
            
        # Print protocol details
        contents = archive.read_file('replay.details')
        details = protocol.decode_replay_details(contents)
        self.log(details)
        self.rawdetails = details
        # http://dev.esl.eu/blog/category/s2protocol/
        # divide it by 10,000,000 and subtract 11,644,473,600
        self.ts = (details['m_timeUTC'] / 10000000) - 11644473600
        self.tzhrs = details['m_timeLocalOffset'] / 36000000000
        self.map = details['m_title']
        self.players = details['m_playerList']
        
        return 0
