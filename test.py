from utils import *
import pandas as pd

df = pd.read_excel('read.xlsx')
password = "tdye giwa ounx wuvp"
recipients = ["1719kshitij@gmail.com"]
send_email_with_dataframe(recipients,df,password)