Section 1 (main section):
login to rasp-028.berry.scss.tcd.ie (rasp-028 is mandatory here, since it's hardcoded to act as a router)
unzip the p3-integrated file from the submission and copy the p3-integrated folder to any path on the pi
cd to the p3-integrated folder and run the following:

chmod +x runme.sh
chmod +x pass.sh
./runme.sh

When terminal prompts with "system ready" message, run "python3 send-interest.py" and press 1 to send interest packets for a truck.
This should send a series of interest packets, receive corresponding data packets, actuate on the received data and output on screen.
You should see a series of messages on screen. Sample messages are shown in appendix at the end of this readme for reference.

You're done and can close this readme. Keep going if you faced any error or you expected more detailed execution.

You can follow the instructions in the next section if
the runme.sh did not work, or
you want to see the router and advertisement files in action in terminal (runme.sh hides those in background)

Section 2 (backup section - read this section if you are somehow not satisfied with the previous section)

Steps to execute:
1. run the command "ssh username@macneill.scss.tcd.ie" on your terminal where username is your username
enter password

run the command "ssh -i username rasp-028.berry.scss.tcd.ie" (mandatory to run on rasp-028)
enter password

cd www/p3-integrated/ (assuming this is the path where the code folder I submitted was copied to)
run "python3 router.py"

2. run the command "ssh username@macneill.scss.tcd.ie" on another instance of terminal
enter password

run "ssh -i username rasp-029.berry.scss.tcd.ie" (rasp-029 not mandatory, any pi works with the caveat that private pis are safer from "address already in use" error, which might come on common pis)
enter password

cd www/p3-integrated/
python3 advertise-feature.py
enter "truck" when prompted for enter vechicle type

you should now start seeing the following in the terminal opened in step 1

truck arrived. Added to system
Number of vehicles in network:  {'truck': 1, 'bike': 0, 'car': 0}

3. run "ssh username@macneill.scss.tcd.ie" on another instance of terminal
enter password

run "ssh -i username rasp-029.berry.scss.tcd.ie" (rasp-029 not mandatory, any pi works with the caveat that private pis are safer as said before)
enter password

cd www/p3-integrated/

python3 send-interest.py
press 1 when prompted

pressing 1 should start the sending of interest packets and do their actuation upon receiving data for those. See appendix for sample output.

---------------------------------------------------------

You are done and can close this readme.

Continue reading if you faced error.
if you received the following for any of the interest packets, the sensors were removed by the time you requested for interest packets.

attempting to send interest packet:  truck/engine-temperature
Data packet received:  Sensors/actuators not available to serve this request  for interest packet  truck/engine-temperature
Truck is appraoching with engine temperature of  Sensors/actuators not available to serve this request  degree Fahrenheit

For such a case, just check the terminal running the router.py file and wait for the arrival of truck again.
When you see the following message:

truck arrived. Added to system
Number of vehicles in network:  {'truck': 1, 'bike': 0, 'car': 0}

run the python3 send-interest.py again and you should receive the right set of data. Now, you're done.


===============================================================
===========================APPENDIX============================
===============================================================

*******************************************************************
***************(1) SUCCESSFUL OUTPUT LOOKS LIKE THIS***************
*******************************************************************

attempting to send interest packet:  truck/speed
Data packet received:  76  for interest packet  truck/speed
Truck approaching at speed  76  km/h



attempting to send interest packet:  interest/corrupted
Data packet received:  404 not found  for interest packet  interest/corrupted



attempting to send interest packet:  truck/proximity
Data packet received:  27  for interest packet  truck/proximity
Truck is near at  27  metres



attempting to send interest packet:  truck/pressure
Data packet received:  94  for interest packet  truck/pressure
Truck tyre pressure is at  94  psi



attempting to send interest packet:  truck/light-on
Data packet received:  off  for interest packet  truck/light-on
Truck light is  off



attempting to send interest packet:  truck/wiper-on
Data packet received:  faulty  for interest packet  truck/wiper-on
Truck wiper is  faulty



attempting to send interest packet:  truck/passengers-count
Data packet received:  2  for interest packet  truck/passengers-count
Truck is approaching with  2  number of passengers



attempting to send interest packet:  truck/fuel
Data packet received:  full  for interest packet  truck/fuel
Truck is approaching with fuel at  full



attempting to send interest packet:  truck/engine-temperature
Data packet received:  215  for interest packet  truck/engine-temperature
Truck is appraoching with engine temperature of  215  degree Fahrenheit
 
 *** Sending data for AI/ML prediction ***   

making the inspection decision...


 AI/ML prediction:  truck  needs inspection 




Press 1 to send truck interest packets
Press 2 to send bike interest packets
Press 3 to send car interest packets