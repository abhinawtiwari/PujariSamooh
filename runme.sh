# !/bin/bash

echo "Enter username: "
read -s username

echo "Enter Password: "
read -s passName

basedir=$PWD
echo $PWD

nohup python3 router.py &

echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-029.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py truck>/dev/null 2>&1 &"
echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-040.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py car>/dev/null 2>&1 &"
echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-041.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py car>/dev/null 2>&1 &"
echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-042.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py bike>/dev/null 2>&1 &"
echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-043.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py bike>/dev/null 2>&1 &"
echo $passName | ./pass.sh ssh -o StrictHostKeyChecking=no $username@rasp-044.berry.scss.tcd.ie "nohup python3 $basedir/advertise-feature.py truck>/dev/null 2>&1 &"

sleep 10
echo "system ready"
