import datetime
import time
import sched
import sys

# from RPi import GPIO
from RPIO import PWM as pwm

JJY_FORMAT="M{0:03b}0{1:04b}M00{2:02b}0{3:04b}M00{4:02b}0{5:04b}M{6:04b}00{10}{11}0M0{7:04b}{8:04b}M{9:03b}000000M"

scheduler = sched.scheduler(time.time, time.sleep)

IO_PIN=4 # BCM4 = board 7
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(IO_PIN, GPIO.OUT)

pwm.set_loglevel(pwm.LOG_LEVEL_ERRORS)
pwm.setup(5)
pwm.init_channel(0, 5000)
#p = GPIO.PWM(IO_PIN, 40000)



# M 200 [ms]
def signalM ():
  #p.start(50.0)
  for x in range(1,1000,5): 
    pwm.add_channel_pulse(0, IO_PIN, x ,3)
  time.sleep(0.2)
  pwm.clear_channel_gpio(0, IO_PIN)
  #p.stop()
  sys.stdout.write('.')
  sys.stdout.flush()

# 1 500 [ms]
def signal1 ():
  #p.start(50.0)
  for x in range(1,1000,5): 
    pwm.add_channel_pulse(0, IO_PIN, x ,3)
  time.sleep(0.5)
  pwm.clear_channel_gpio(0, IO_PIN)
  #p.stop()
  sys.stdout.write('1')
  sys.stdout.flush()

# 0 800 [ms]
def signal0 ():
  #p.start(50.0)
  for x in range(1,1000,5): 
    pwm.add_channel_pulse(0, IO_PIN, x ,3)
  time.sleep(0.8)
  pwm.clear_channel_gpio(0, IO_PIN)
  #p.stop()
  sys.stdout.write('0')
  sys.stdout.flush()

senders = {'M': signalM, '1': signal1, '0': signal0}

def schedule_next ():
  a = datetime.datetime.now() + datetime.timedelta(minutes=1)
  next0sec = time.mktime(datetime.datetime(a.year, a.month, a.day, a.hour, a.minute, 0, 0).timetuple())
  (mhjyw, h, m) = a.strftime('%M%H%j%y%w,%H,%M').split(',')
  data = [int(x) for x in mhjyw]
  parity_h = "".join(["{:b}".format(int(x)) for x in h]).count('1') % 2
  parity_m = "".join(["{:b}".format(int(x)) for x in m]).count('1') % 2
  signals = JJY_FORMAT.format(*(data+[parity_h, parity_m]))
  for i, signal in enumerate(signals):
    scheduler.enterabs(next0sec + i, 1, senders[signal], ())
  scheduler.enterabs(time.mktime(a.timetuple()), 1, schedule_next, ()) 

if __name__ == '__main__':
  schedule_next()
  scheduler.run()
  while True:
    time.sleep(60)

