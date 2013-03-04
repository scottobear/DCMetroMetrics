from utils import *
from datetime import date, datetime, time
import utils

###################################################################
# Class represents an incident
class Incident(object):

    def __init__(self, data):

        keys = [u'SymptomDescription',
         u'LocationDescription',
         u'UnitName',
         u'UnitType',
         u'SymptomCode',
         u'TimeOutOfService',
         u'DateOutOfServ',
         u'StationName',
         u'StationCode',
         u'DateUpdated',
         u'UnitStatus',
         u'DisplayOrder']

        for k in keys:
            if k not in data:
                raise RuntimeError('Key missing in incident data: %s'%k)

        self.data = data # Store a copy of the original data from this object was constructed

        self.__dict__.update(data.iteritems())
        self.addAttr()

    def addAttr(self):
        self.UnitId = self.UnitName + self.UnitType

        # Clean up the out of service and update times
        outOfServiceDate = utils.parseMetroDate(self.DateOutOfServ)
        outOfServiceTime = utils.parseMetroTime(self.TimeOutOfService)
        self.TimeOutOfService = datetime.combine(date=outOfServiceDate, time=outOfServiceTime)
        self.TimeUpdated = utils.parseMetroDatetime(self.DateUpdated)

        del self.DateUpdated
        del self.DateOutOfServ

    def isElevator(self):
        return self.UnitType == 'ELEVATOR'

    def isEscalator(self):
        return self.UnitType == 'ESCALATOR'

    def isInspection(self):
        return self.SymptomDescription == 'PREV. MAINT. INSPECTION'

    def isWalker(self):
        return self.SymptomDescription == 'TURNED OFF/WALKER'

    def isBroken(self):
        return not (self.isWalker() or self.isInspection())

    def __getitem__(self, k):
        return getattr(self, k)