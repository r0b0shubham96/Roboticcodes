import math
import evdev
import _thread
import time

import serial

from Stepper import stepper

def print_time(threadName, delay, s, steps, dir, speed):
   count = 1
   while count >=1:
      time.sleep(delay)
      count -= 1
      print ("%s: %s" % ( threadName, time.ctime(time.time())))
      testStepper = stepper(s)
      testStepper.step(steps, dir,speed);


################ Angle Check
      
##arduinoSerialData = serial.Serial('/dev/ttyACM1',9600)
###if(arduinoSerialData.inWaiting()>0):
##myData = arduinoSerialData.readline()
##print(myData.decode('utf-8'))

#################
#[stepPin, directionPin, enablePin]
s1=[6,13,4]    #31,33,7--Rpi pins
s2=[17,27,22]  #11,13,15
s3=[20,21,11]   #38,40,23

######### Link Lenghts in cm.
l1=0 ##34.5
l2=42
l3=35.6

######## Coordinates in xy frame in cm
hx = 17.8
hy = 0
hz = 18.4

htheta1=math.degrees(math.atan(hy/hx))
htheta3=-math.degrees(math.acos((hx*hx+hy*hy+hz*hz-(l1*l1)-(l2*l2)-(l3*l3)-2*l1*(hz-l1))/(2*l2*l3)))  
htheta2=math.degrees(math.atan((hz-l1)*(math.cos(htheta1*math.pi/180)-math.sin(htheta1*math.pi/180))/(hx-hy))) - math.degrees(math.atan((l3*math.sin(htheta3*math.pi/180))/(l2 + l3*math.cos(htheta3*math.pi/180))))
##htheta3=math.degrees(math.acos(hz/(l1*math.cos(htheta1*math.pi/180) + l2*math.cos((htheta2 + htheta1)*math.pi/180))))

print("\n")
print(str(htheta1)+" htheta2:"+str(htheta2)+ " htheta3:"+str(htheta3))
print("\n")

##ox = 35 * (math.sqrt(2))
ox = 17.8
oy = 0
oz = 18.4

#######Inverse Kinematics Equation for obtaining th joint angles -
oldtheta1=math.degrees(math.atan(oy/ox))
oldtheta3=-math.degrees(math.acos((ox*ox+oy*oy+oz*oz-(l1*l1)-(l2*l2)-(l3*l3)-2*l1*(oz-l1))/ (2*l2*l3)))
oldtheta2=math.degrees(math.atan((oz-l1)*(math.cos(oldtheta1*math.pi/180)-math.sin(oldtheta1*math.pi/180))/(ox-oy))) - math.degrees(math.atan((l3*math.sin(oldtheta3*math.pi/180))/(l2 + l3*math.cos(oldtheta3*math.pi/180))))
##oldtheta1=math.degrees(math.atan(oy/ox) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
##oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))

print("\n")
print(str(oldtheta1)+" oldtheta2:"+str(oldtheta2)+ " oldtheta3:"+str(oldtheta3))
print("\n")
ppr=1600  # Pulse Per Revolution

x = 17.8 #17.8
##x = (ox * 2.0 / (math.sqrt(3)))
##x = ox * (math.sqrt(2))
y = 15  #18.4
z = 18.4

print("\n")
print(str(x)+" y:"+str(y)+ " y:"+str(z))  

theta1=math.degrees(math.atan(y/x))
theta3=-math.degrees(math.acos((x*x+y*y+z*z-(l1*l1)-(l2*l2)-(l3*l3)-2*l1*(z-l1))/ (2*l2*l3)))
theta2=math.degrees(math.atan((z-l1)*(math.cos(theta1*math.pi/180)-math.sin(theta1*math.pi/180))/(x-y))) - math.degrees(math.atan((l3*math.sin(theta3*math.pi/180))/(l2 + l3*math.cos(theta3*math.pi/180))))
##theta1=math.degrees(math.atan(y/x) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
##theta3=math.degrees(math.acos(z/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))

# angles to be moved
oa1=oldtheta1 - htheta1 #base
oa2=oldtheta2 - htheta2 #link 1
oa3=oldtheta3 - htheta3 #link 2

na1=theta1 - htheta1 #base
na2=theta2 - htheta2 #link 1
na3=theta3 - htheta3 #link 2

a1 = na1 - oa1
a2 = na2 - oa2
a3 = na3 - oa3

##a1 = -45
##a2 = 0
##a3 = 0

print("\n")
print(str(theta1)+" theta2:"+str(theta2)+ " theta3:"+str(theta3))
print("\n")
print(str(a1)+" a2:"+str(a2)+ " a3:"+str(a3))
print("\n")
##a1=0  #base
##a2=-39  #link 1
##a3=0  #link 2

## Gear Ratios
g1=12.22222222222
g2=10
g3=10
 
# Calculation for step and Speed
step1=(ppr/360)*a1*g1  
#speed1=0.01

step2=(ppr/360)*a2*g2
#speed2=0.01

step3=(ppr/360)*a3*g3  
#speed3=0.01

# Calculation of timedelay for differnt motors
execTime=10

if (step1 == 0):
    td1 = 0
else :
##    td1=abs((execTime-(step1*0.002))/step1)
    td1 = execTime/step1

if (step2 == 0):
    td2 = 0
else:
##    td2=abs((execTime-(step2*0.002))/step2)
    td2 = execTime/step2

if (step3 == 0) :
    td3 = 0
else:
##    td3=abs((execTime-(step3*0.002))/step3)
    td3 = execTime/step3

print(td1)
print(td2)
print(td3)

if step1<0:
    dir1="r"
else:
    dir1="l"

if step2<0:
    dir2="l"
else:
    dir2="r"

if step3<0:
    dir3="l"
else:
    dir3="r"

##_thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
##_thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
##_thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3))
##
##time.sleep(10)

print("\n")
print("Opening port")
print("\n")
