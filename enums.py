#from strenum import StrEnum
from enum import Enum

class Category(Enum):
  Salary = "Field - Salary"
  S_Hourly = "Field - Hourly (SOT)"
  R_Hourly = "Field - Hourly (ROT)"
  #Hourly = "Field - Hourly - ROT" (regular overtime) *add these later
  #Hourly = "Field - Hourly - SOT" (seasonal overtime) *add these later
