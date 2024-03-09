import time

def get_time():
   """
   Returns the current time in HH:MM format
   """
   return time.strftime("%H:%M")
   
def check_time(check_time):
   current_time = get_time()
   if current_time == check_time:
      print("Time to wake up!")
      
while True:
   check_time("13:51") 
   time.sleep(60)
