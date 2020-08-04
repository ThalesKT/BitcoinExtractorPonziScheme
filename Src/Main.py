from Src.Features import *
from datetime import *

#USING THE CLASS FEATURES
#Features = Features("1MCy4VFrM5cGFths1XVm98bDNCEX9Wc5ae")
#Features = Features("19BXnWPKVkiL2bhrUaSsxdxmkFUXzfS47z")  #Possui apenas 2 transações



Features = Features("18qRaHxAmAxzR1QwTGs6211zwWoYnEUEBR")
#result = Features.getAddressLifeTimeOrActivityDaysOrMaximumNumberDailyTransactions("AddressLifeTime")
#result1 = Features.getAddressLifeTimeOrActivityDaysOrMaximumNumberDailyTransactions("ActivityDays")
#result2 = Features.getAddressLifeTimeOrActivityDaysOrMaximumNumberDailyTransactions("MaximumNumberDailyTransactions")
#result3 = Features.getNumberIncomingTransactionsOrRatio("NumberIncomingTransactions")
#result4 = Features.getNumberIncomingTransactionsOrRatio("Ratio")
#print("Address life time: {}".format(result))
#print("Activity Days: {}".format(result1))
#print("Maximum Number of Daily Transactions: {}".format(result2))


print(Features.getNumberIncomingTransactionsOrRatio("Ratio"))