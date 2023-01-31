from cmath import nan
from numpy import NaN
import constants as c
import json
import datetime


class Block:
    def __init__(self, row, day, hours, overtime = False, note = True):
        self.row = row
        self.clockIn = row[c.TS_CLOCK_IN]
        self.clockOut = row[c.TS_CLOCK_OUT]
        self.date = row[c.TS_DATE]
        # round hours to 3 decimal places
        self.hours = round(hours, 4)
        self.overtime = overtime
        self.day = day
        self.extraPay = False
        self.color = (255, 255, 255)
        self.payRate = 0



        try:
            self.tags = json.loads(row[c.TS_TAGS])
        except:
            self.tags = []
         
        for tag in self.tags:
            name  = tag['Name']
            color = tag['Color']
            if name == c.TAG_CODE_EXTRA_PAY:
                self.extraPay = True
                self.color = color

        self.category = self.day.week.employee.category

        if (not self.category == c.CATEGORY_SALARY and not self.day.lunchTaken and self.hours < 0):
            self.color = '#efbbb9'



        # TODO: change this 0 to a number code
        self.costCode = 0
    
        if (hours < 0):
            self.activity = c.ACTIVITY_CODE_FORCED_LUNCH
        else:
            self.activity = row[c.TS_ACTIVITY]
            
        if '-' in self.activity:
            self.costCode = float(self.activity.split('-')[0].strip())
        else:
            self.costCode = c.DEFAULT_COSTCODE


            
        premiumRate = None

        if self.costCode == 280 or self.costCode >= 300 and self.costCode <= 399:
            premiumRate = self.day.week.employee.employee[c.EE_SNOW_PAY]
            if premiumRate == None:
                premiumRate = 0

        
      
        # assumes salary extra pay never occurs in winter
        if (self.category == c.CATEGORY_SALARY and self.extraPay): 
            self.payRate = self.day.week.employee.payRate
        elif (self.category == c.CATEGORY_SALARY):
            if (premiumRate != None):
                self.payRate = premiumRate
            else:
                self.payRate = 0
        elif (self.category == c.CATEGORY_S_HOURLY):
            
            if (self.overtime):
        
                if (premiumRate != None):
                    self.payRate = self.day.week.getOvertimeRate(premiumRate)
               
                else:
                    self.payRate = self.day.week.getOvertimeRate(self.day.week.employee.payRate)
            else:
                
                if (premiumRate != None):
                    self.payRate = premiumRate
                else:
                    self.payRate = self.day.week.employee.payRate
        elif (self.category == c.CATEGORY_R_HOURLY):
            if (self.overtime):
                if (premiumRate != None):
                    self.payRate = premiumRate * 1.5
                else:
                    self.payRate = self.day.week.employee.payRate * 1.5
            else:
                if (premiumRate != None):
                    self.payRate = premiumRate
                else:
                    self.payRate = self.day.week.employee.payRate


        self.__setPayType(premiumRate != None)
        self.__setJobNumber()
        self.__setWorkOrder()
        self.__setDescription()
        self.__setDepartment()
        self.__setEquipment() #modified
        if (note):
            tempNote = str(row[c.TS_NOTE])
            if (tempNote == 'nan'):
                tempNote = None

            # remove char number 10 from note
            if (tempNote != None):
                tempNote = self.__removeChar(tempNote, chr(10))

            self.note = tempNote
        else:
            self.note = None


    def __removeChar(self, string, char):
        return string.replace(char, ' ')

        


    def __setPayType(self, isPremium):
        if isPremium:
            self.payType = 3
        elif (self.overtime and (self.category == c.CATEGORY_S_HOURLY or self.category == c.CATEGORY_R_HOURLY)):
            self.payType = 2
        else:
            self.payType = 1
        

    def __setJobNumber(self):
        job = str(self.row[c.TS_JOB_NAME])
        number = -1
        if '-' in job:
            number = str(job.split('-')[0].strip())

        if (self.__getNoteNumber() != None):
            self.jobNumber = None
        elif (not number == -1):
            if (len(number) < 5):
                self.jobNumber = number
            else:
                self.jobNumber = None
        else:
            self.jobNumber = self.__getInvalid()
        if self.costCode >= 9000 and self.costCode <= 9999:
            self.jobNumber = ""


    def __setWorkOrder(self):
        job = str(self.row[c.TS_JOB_NAME])

        number = '-1'
        if '-' in job:
            number = str(job.split('-')[0].strip())

        if (self.__getNoteNumber() != None):
            self.workOrder = self.__getNoteNumber()
        elif (not number == '-1' and len(number) == 5):
            self .workOrder = str(job.split('-')[0].strip())
        else:
            self.workOrder = None

    def __getNoteNumber(self):
        noteNumber = self.row[c.TS_NOTE]
        if (not noteNumber == None and len(str(noteNumber)) >= 8):

            # remove all spaces from possibleWO
            possibleWO = str(noteNumber).replace(' ', '')
     
            if (possibleWO[0:3] == "WO#"):
                return noteNumber[3:8]
            
            else:
                return None
        else:
            return None


    def __getInvalid(self):
        if self.costCode >= 1 and self.costCode <= 9:
            return 99
        elif self.costCode >= 10 and self.costCode <= 99:
            return 100
        elif self.costCode >= 200 and self.costCode <= 299:
            return 200
        elif self.costCode >= 300 and self.costCode <= 399:
            return 300
        elif self.costCode >= 400 and self.costCode <= 499:
            return 400
        else:
            return 99



    
    
    

    def __setDescription(self):
        if (self.hours < 0):
            self.description = "Forced Lunch"
        elif self.costCode >= 1 and self.costCode <= 99:
            self.description = "Landscape Work"
        elif self.costCode >= 200 and self.costCode <= 299:
            self.description = "Maintenance Jobs"
        elif self.costCode >= 300 and self.costCode <= 399:
            self.description = "Snow Removal"
        elif self.costCode >= 400 and self.costCode <= 499:
            self.description = "Sprinkler Work"
        elif self.costCode >=9000 and self.costCode <= 9999:
            self.description = "Equipment Repair" #modified
        else:
            self.description = "Misc/Odd Jobs"

    def __setDepartment(self):
        if self.costCode >= 1 and self.costCode <= 99:
            self.department = 1
        elif self.costCode >= 200 and self.costCode <= 299:
            self.department = 2
        elif self.costCode >= 300 and self.costCode <= 399:
            self.department = 3
        elif self.costCode >= 400 and self.costCode <= 499:
            self.department = 4
        elif self.costCode >= 9000 and self.costCode <= 9999:
            self.department = 9 #modified
        else:
            self.department = 5

    def __setEquipment(self):
        if self.costCode >= 9000 and self.costCode <= 9999:
            self.equipment = 95 #modified
        else:
            self.equipment = ""
    

    
    # gets an output row to be added to dataframe
    #  empnum	strprd	payprd	chknum	chkdte	paytyp	qtrnum	taxste	dirdep	salary	payrt1	payrt2	payrt3	ntetxt	dtewrk	dscrpt	wrkord	jobnum	eqpnum	loctax	crtfid	phsnum	cstcde	paytyp	paygrp	payrte	hrswrk	pcerte	pieces	cmpcde	dptmnt	absnce	usrdf1	ntetxt
    def getOutputRow(self, startDate, endDate, checkDate):
        # if checkdate isnt defined, change checkdate to the friday following the end date
        if checkDate == None:
            self.checkDate = endDate + datetime.timedelta(days=(4-endDate.weekday()) % 7 )
        else:
            self.checkDate = checkDate

        quarter = 1
        # get which quarter of the year the checkdate is in
        if (self.checkDate.month >= 1 and self.checkDate.month <= 3):
            quarter = 1
        elif (self.checkDate.month >= 4 and self.checkDate.month <= 6):
            quarter = 2
        elif (self.checkDate.month >= 7 and self.checkDate.month <= 9):
            quarter = 3
        else:
            quarter = 4
        
        self.qtrNumber = quarter
        # print(self.checkDate.month)
        # self.qtrNumber = self.checkDate.month // 3 + 1


         # change cost code to a string with .000 at the end
        self.costCode = str(self.costCode) + ".000"

        
        row = [
           self.day.week.employee.employeeNumber, # empnum
            startDate, # strprd
            endDate, # payprd
            '0000', # chknum
            self.checkDate, # chkdte
            1, # paytyp
            self.qtrNumber, # qtrnum
            'UT', # taxste
            '', # dirdep
            '', # salary
            '', # payrt1
            '', # payrt2
            '', # payrt3
            '', # ntetxt
            self.date, # dtewrk
            self.description, # dscrpt
            self.workOrder, # wrkord
            self.jobNumber, # jobnum
            self.equipment, # eqpnum
            '', # loctax
            '', # crtfid
            '', # phsnum
            self.costCode, # cstcde
            self.payType, # paytyp
            '', # paygrp
            self.payRate, 
            self.hours, # hrswrk
            '', # pcerte
            '', # pieces
            '', # cmpcde
            self.department, # dptmnt
            '', # absnce
            '', # usrdf1
            self.note, # ntetxt
            self.color, # color
        ]

        return row



            


    




    
