import week
import datetime
import constants as c
import enums as e
import block



class Employee:
    def __init__(self, row, dfTimesheet):
        self.weeks = []
        self.__parseName(row[c.EE_FIRST_NAME], row[c.EE_LAST_NAME])
        self.category = row[c.EE_CATEGORY]
        self.payRate = row[c.EE_PAY]
        self.employee = row


        # if employeeNumber is not 4 digits, dfEmployeeTimesheet is invalid
        if (len(str(self.employeeNumber)) == 4):
            self.timesheet  = dfTimesheet[dfTimesheet[c.TS_EMPLOYEE].str.contains(str(self.employeeNumber))].sort_values(by=[c.TS_DATE])
        else:
            self.timesheet = None
        
        self.row = row.copy()
        self.negBlocks = []
        if (self.timesheet is not None):
            self.__setWeeks(self.timesheet)


    def __parseName(self, firstName, lastName):
        if '-' in firstName:
            # get employee number as number
            self.employeeNumber = int(firstName.split('-')[0].strip())
            self.firstName = firstName.split('-')[1].strip()
        else:
            self.firstName = firstName.strip()
            self.employeeNumber = 99
        self.lastName = lastName.strip()




    # function takes in a dataframe and creates a list of weeks
    def __setWeeks(self, df):
        startDate = None
        for index, row in df.iterrows():
            date = row[c.TS_DATE]
            newStart = date  - datetime.timedelta(days=(date.weekday() + 1) % 7)
            newEnd = newStart + datetime.timedelta(days=6)
            if startDate != newStart:
                weekDf = df[df[c.TS_DATE] >= newStart]
                weekDf = weekDf[weekDf[c.TS_DATE] <= newEnd]
                self.weeks.append(week.Week(weekDf, self))
                startDate = newStart

 

            