ACTIVITY_CODE_LUNCH = '009 - Lunch'
TAG_CODE_EXTRA_PAY = 'Hourly Pay'
ACTIVITY_CODE_FORCED_LUNCH = 'forced lunch'

TS_EMPLOYEE = 'Employee'
TS_DATE = 'Date'
TS_CLOCK_IN = 'Clock In Time'
TS_CLOCK_OUT = 'Clock Out Time'
TS_ACTIVITY = 'Activity'
TS_HOURS = 'Hours'
TS_PAYROLL_HOURS = 'Payroll Hours'
TS_TAGS = 'Tags'
TS_NOTE = 'Note'
TS_JOB_NAME = 'Job Name'


EE_FIRST_NAME = 'First Name'
EE_LAST_NAME = 'Last Name'
EE_CATEGORY = 'Category'
EE_PAY = 'Pay'
EE_SNOW_PAY = 'Comm.Rate %' #comm.rate % is the snow pay rate for all employees.

# empnum	strprd	payprd	chknum	chkdte	paytyp	qtrnum	taxste	dirdep	salary	payrt1	payrt2	payrt3	ntetxt	dtewrk	dscrpt	wrkord	jobnum	eqpnum	loctax	crtfid	phsnum	cstcde	paytyp	paygrp	payrte	hrswrk	pcerte	pieces	cmpcde	dptmnt	absnce	usrdf1	ntetxt
O_HEADER = ['empnum', 'strprd', 'payprd', 'chknum', 'chkdte', 'paytyp', 'qtrnum', 'taxste', 'dirdep', 'salary', 'payrt1', 'payrt2', 'payrt3', 'ntetxt', 'dtewrk', 'dscrpt', 'wrkord', 'jobnum', 'eqpnum', 'loctax', 'crtfid', 'phsnum', 'cstcde', 'paytyp', 'paygrp', 'payrte', 'hrswrk', 'pcerte', 'pieces', 'cmpcde', 'dptmnt', 'absnce', 'usrdf1', 'ntetxt']
O_EMPNUM = 'empnum'
O_STRPRD = 'strprd'
O_PAYPRD = 'payprd'
O_CHKNUM = 'chknum'
O_CHKDTE = 'chkdte'
O_PAYTYP = 'paytyp'
O_QTRNUM = 'qtrnum'
O_TAXSTE = 'taxste'
O_DIRDEP = 'dirdep'
O_SALARY = 'salary'
O_PAYRT1 = 'payrt1'
O_PAYRT2 = 'payrt2'
O_PAYRT3 = 'payrt3'
O_NTETXT = 'ntetxt'
O_DTEWRK = 'dtewrk'
O_DSCRPT = 'dscrpt'
O_WRKORD = 'wrkord'
O_JOBNUM = 'jobnum'
O_EQPNUM = 'eqpnum'
O_LOCTAX = 'loctax'
O_CRTFID = 'crtfid'
O_PSSNUM = 'phsnum'
O_CSTCDE = 'cstcde'
O_PAYTYP = 'paytyp'
O_PAYGRP = 'paygrp'
O_PAYRTE = 'payrte'
O_HRSWRK = 'hrswrk'
O_PCERTE = 'pcerte'
O_PIECES = 'pieces'
O_CMPPRD = 'cmpcde'
O_DPTMNT = 'dptmnt'
O_ABSNCE = 'absnce'
O_USRDF1 = 'usrdf1'
O_NTETXT = 'ntetxt'



DEFAULT_COSTCODE = 10



# Removed all the enums, replaced w/ constants
CATEGORY_SALARY = "Field - Salary"
CATEGORY_S_HOURLY = "Field - Hourly (SOT)"
CATEGORY_R_HOURLY = "Field - Hourly (ROT)"