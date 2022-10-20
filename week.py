import day 
import constants as c
import datetime

class Week:


    def __init__(self, df, employee):
        self.employee = employee
        self.df = df
        date = df[c.TS_DATE].iloc[0]
        self.startDate = date  - datetime.timedelta(days=(date.weekday() + 1) % 7)
        self.endDate = self.startDate + datetime.timedelta(days=6)
        self.lunchHours = self.__getLunchHours()
        self.hours = self.__getWeekHours(self.lunchHours)
        #self.__setOvertimeRate()
        self.__setDays(self.__getLunchHours())
        self.__setLunchDays()


    def __getWeekHours(self, lunchHours):
        daysDf = self.df.drop_duplicates(subset=[c.TS_DATE], keep='first')
        daysDf = daysDf.sort_values(by=[c.TS_CLOCK_IN])
        hours = -lunchHours
        for index, row in daysDf.iterrows():
            dayDf = self.df[self.df[c.TS_DATE] == row[c.TS_DATE]]
            dayDf = dayDf.sort_values(by=[c.TS_CLOCK_IN])
            dayDf = dayDf[~dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)]

            i = 0
            for index, row in dayDf.iterrows():
                newHours = row[c.TS_PAYROLL_HOURS]

                if (newHours > .008):
                    hours += newHours
                i += 1


        return hours

    def __setDays(self, lunchHours):
        daysDf = self.df.drop_duplicates(subset=[c.TS_DATE], keep='first')
        daysDf = daysDf.sort_values(by=[c.TS_CLOCK_IN])
        days = []
        hours = 0#-lunchHours
        for index, row in daysDf.iterrows():
            dayDf = self.df[self.df[c.TS_DATE] == row[c.TS_DATE]]
            dayDf = dayDf.sort_values(by=[c.TS_CLOCK_IN])
            dayDf = dayDf[~dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)]

            newDay = day.Day(dayDf, self)
            i = 0
            for index, row in dayDf.iterrows():
                newHours = row[c.TS_PAYROLL_HOURS]

                if (newHours > .008):
                    hours += newHours
                    newDay.addBlock(row, hours)
                i += 1
            days.append(newDay)

        self.days = days
        #self.hours = hours


    def __setLunchDays(self):
        totalHours = self.__getWeekHours(0)
        daysDf = self.df.drop_duplicates(subset=[c.TS_DATE], keep='first')
        for index, row in daysDf.iterrows():
            hadLunch = True
            lunchTime = 0
            dayDf = self.df[self.df[c.TS_DATE] == row[c.TS_DATE]]
            dayDf = dayDf.sort_values(by=[c.TS_CLOCK_IN])

            # check to see if they took a lunch that on this date
            hoursWorked = dayDf[~dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)][c.TS_PAYROLL_HOURS].sum()
            if (hoursWorked > 5 and self.employee.category != c.CATEGORY_SALARY):
               
                lunchRow = dayDf[dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)]
                if not lunchRow.empty:
                    
                    lunchRow = lunchRow.iloc[0]
                    temp = lunchRow[c.TS_HOURS]
                     # if temp is less than 20 minutes
                    if (temp < (1.0 / 60.0) * 20.0):
                        lunchTime = temp
                        hadLunch = False
                else:
                    hadLunch = False
            
            if not hadLunch:
                for day in self.days:
                    if day.date == row[c.TS_DATE]:
                        totalHours -= (.5 - lunchTime)
                        block = day.getLunchBlock((-.5 + lunchTime), totalHours > 40)
                        self.employee.negBlocks.append(block)
                        break
             

            

    def __getLunchHours(self):
        lunchHours = 0
        daysDf = self.df.drop_duplicates(subset=[c.TS_DATE], keep='first')
        daysDf = daysDf.sort_values(by=[c.TS_CLOCK_IN])
        for index, row in daysDf.iterrows():
            lunchTime = 0
            lunchDefault = .5
            dayDf = self.df[self.df[c.TS_DATE] == row[c.TS_DATE]]
            dayDf = dayDf.sort_values(by=[c.TS_CLOCK_IN])

            # check to see if they took a lunch that on this date
            hoursWorked = dayDf[~dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)][c.TS_PAYROLL_HOURS].sum()
            if (hoursWorked > 5 and self.employee.category != c.CATEGORY_SALARY):
            
                lunchRow = dayDf[dayDf[c.TS_ACTIVITY].str.contains(c.ACTIVITY_CODE_LUNCH)]
                if not lunchRow.empty:
                    lunchRow = lunchRow.iloc[0]
                    temp = lunchRow[c.TS_HOURS]
                     # if temp is less than 20 minutes
                    if (temp < (1.0 / 60.0) * 20.0):
                        lunchTime = temp
                    else :
                        lunchDefault = 0

                lunchHours += (lunchDefault - lunchTime)

        return lunchHours

            
              


    def getOvertimeRate(self, rate):
        newRate = ((rate * 40) / self.hours) * 1.5 
        if newRate <= rate:
            newRate = rate + .01
        return round(newRate, 2)
    


