Steps to execute:
1. run the command "ssh atiwari@macneill.scss.tcd.ie" on your terminal
enter password "Ghoda@123"

run the command "ssh -i atiwari rasp-028.berry.scss.tcd.ie"
enter password "Ghoda@123"

cd www/p3-integrated/
run "python3 router.py"

2. run the command "ssh atiwari@macneill.scss.tcd.ie" on your terminal
enter password "Ghoda@123"

run the command "ssh -i atiwari rasp-028.berry.scss.tcd.ie"
enter password "Ghoda@123"

run "ssh -i atiwari rasp-029.berry.scss.tcd.ie"
enter password "Ghoda@123"

cd www/p3-integrated/
python3 advertise-feature.py
enter "truck" when prompted for enter vechicle type

you should now start seeing the following in the terminal opened in step 1

truck arrived. Added to system
Number of vehicles in network:  {'truck': 1, 'bike': 0, 'car': 0}

3. run "ssh saxenac@macneill.scss.tcd.ie" on a terminal
enter password: "Jaimatadi@78"

run "ssh -i saxenac rasp-029.berry.scss.tcd.ie"
enter password: "Jaimatadi@78"

cd www/p3-integrated/

python3 send-interest.py
press 1 when prompted

pressing 1 should start the sending of interest packets and their actuation upon receiving data for those.

The screen looks like following:

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

/users/pgrad/saxenac/.local/lib/python3.8/site-packages/sklearn/base.py:329: UserWarning: Trying to unpickle estimator LinearRegression from version 1.1.2 when using version 1.1.3. This might lead to breaking code or invalid results. Use at your own risk. For more info please refer to:
https://scikit-learn.org/stable/model_persistence.html#security-maintainability-limitations
  warnings.warn(
 predicting on data:  [1, 76, 27, 94, 1, 2, 2, 2, 215] 
/users/pgrad/saxenac/.local/lib/python3.8/site-packages/sklearn/base.py:450: UserWarning: X does not have valid feature names, but LinearRegression was fitted with feature names
  warnings.warn(
 model predicting... 
 AI/ML prediction:  truck  does not need inspection  





Press 1 to send truck interest packets
Press 2 to send bike interest packets
Press 3 to send car interest packets

---------------------------------------------------------

You are done.
if you received the following for any of the interest packets, the sensors were removed by the time you requested for interest packets.

attempting to send interest packet:  truck/engine-temperature
Data packet received:  Sensors/actuators not available to serve this request  for interest packet  truck/engine-temperature
Truck is appraoching with engine temperature of  Sensors/actuators not available to serve this request  degree Fahrenheit

For such a case, just check the terminal running the router.py file and mark the arrival of truck again.
When you see the following message:

truck arrived. Added to system
Number of vehicles in network:  {'truck': 1, 'bike': 0, 'car': 0}

run the python3 send-interest.py again and you should receive the right set of data. Now, you're done.

<!-- =============================================================== -->
login to your pi
copy the p3-integrated folder into any folder on the pi
cd to the p3-integrated folder and run the following:

chmod +x runme.sh
chmod +x pass.sh
./runme.sh

When terminal prompts with "system ready" message, run "python3 send-interest.py"