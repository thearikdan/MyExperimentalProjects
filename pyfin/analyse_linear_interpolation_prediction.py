from datetime import datetime
from utils import prediction
start_date = datetime(2018, 1, 24, 9, 30)
end_date = datetime(2018, 1, 24, 10, 30)

DAYS_TO_ANALYSE = 30


#symbol = "WEED.TO"
#symbol = "EMHTF"
#symbol = "PRMCF"
#symbol = "ACBFF"
#symbol = "MEDFF"
#symbol = "AMZN"
symbol = "NVDA"

ROOT_DIR = "results/analysis"

prediction.analyse_linear_interpolation_prediction_performance(symbol, start_date, end_date, DAYS_TO_ANALYSE, ROOT_DIR)



