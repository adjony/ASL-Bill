#!/usr/bin/env python

from json.encoder import INFINITY
import xlwings as xw
import pandas as pd
import employee as emp
import constants as c
import datetime
#from appscript import k
import xlsxwriter
import os


#template_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Personal', 'Education_Learning', 'PythonStuff', 'vba', 'EiD_SageImport_Template.xlsm')
template_path = os.path.join(os.path.expanduser('~'), 'Documents', 'asl-payroll', 'EiD_SageImport_Template.xlsm')
wb = xw.Book(template_path) #optional: can also be a path to an existing file
output = wb.sheets['Flat Import']
timesheet = wb.sheets['Arborgold_TimesheetData']
employees = wb.sheets['Arborgold_EmployeeData']

#Defines the column ranges within the source data sheets
dfTimesheet = pd.read_excel(template_path, sheet_name='Arborgold_TimesheetData', skiprows=0, usecols="C:M").dropna(subset=[c.TS_EMPLOYEE])
dfEmployees = pd.read_excel(template_path, sheet_name='Arborgold_EmployeeData', skiprows=0, usecols="A:E").dropna(subset=[c.EE_FIRST_NAME])

# write "Processing..." to the output sheet in cell A5
#output.range('B5').value = "Processing Arborgold data from employee and timesheet tabs..."
#output.Shapes("Step2").TextFrame.Characters.Text = "Processing..."
#output.Shapes("Step2").Fill.ForeColor.RGB = RGB(204, 0, 0)


employees = []

# create employee objects
for index, row in dfEmployees.iterrows():
    employee = emp.Employee(row, dfTimesheet)
    employees.append(employee)

# sort employees by last name (ascending)

employees.sort(key=lambda x: x.lastName)





dfOutput = pd.DataFrame(columns=[*c.O_HEADER, 'color'])
i = 0
    
# 1970
# override checkdate if cell P1 contains a new date
checkDate = output.range('P1').value

earliestWeek = min([min([week.startDate for week in employee.weeks], default=datetime.date(datetime.MAXYEAR, 1, 1)) for employee in employees], default=datetime.date(datetime.MAXYEAR, 1, 1))
latestWeek = max([max([week.endDate for week in employee.weeks], default=datetime.date(datetime.MINYEAR, 1, 1)) for employee in employees], default=datetime.date(datetime.MINYEAR, 1, 1))
for employee in employees:
    for negBlock in employee.negBlocks:
        dfOutput.loc[i + 2] = negBlock.getOutputRow(earliestWeek, latestWeek, checkDate)
        i += 1
    for week in employee.weeks:
        for day in week.days:
            for block in day.blocks:
                dfOutput.loc[i + 2] = block.getOutputRow(earliestWeek, latestWeek, checkDate)
                i += 1

colorsCol = dfOutput['color']
dfOutput.drop(columns=['color'], inplace=True)






startRow = 12
startColumnNumber = 2
startColumn = xlsxwriter.utility.xl_col_to_name(startColumnNumber - 1)


endColumnNumber = startColumnNumber + dfOutput.shape[1] - 1
endColumn  = xlsxwriter.utility.xl_col_to_name(endColumnNumber - 1)
endRow = startRow + dfOutput.shape[0] - 1




output[startColumn + str(startRow)].options(pd.DataFrame, header=0, index=False, expand='table').value = dfOutput

start = 2
end = dfOutput.shape[0] + 2
# fit cells
# output.range(startColumn + str(startRow) + ':' + endColumn + str(endRow)).api.autofit()
    # 'B11:AI' + str(dfOutput.shape[0] + 2)).autofit()

for i in range(start, end):


    row = startColumn + str(i + startRow - 2) + ':' + endColumn + str(i + startRow - 2)
    output.range(row).color = colorsCol[i]
#     # output.range(row).api.get_border(which_border=k.border_top).line_style.set(1)
#     # output.range(row).api.get_border(which_border=k.border_bottom).line_style.set(1)
#     # output.range(row).api.get_border(which_border=k.border_left).line_style.set(1)
#     # output.range(row).api.get_border(which_border=k.border_right).line_style.set(1)
    
# write "Done!" to the output sheet in cell B2
output.range('B3').value = "Done!"
output.range('A5').value = ""
output.range('K1').value = str(checkDate)



