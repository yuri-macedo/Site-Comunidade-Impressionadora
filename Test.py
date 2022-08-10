from datetime import datetime,timezone
import pytz

utc_time = datetime.utcnow()
tz = pytz.timezone('America/Sao_Paulo')
time=pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)
print(utc_time,"\n",time)