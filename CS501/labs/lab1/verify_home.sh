
len=${#1}

while read line
do
  userhome=$(eval echo ~$line)
  test=${userhome:0:len}
  if [ $1 == $test ]
  then
    echo $userhome
  # else
  #   echo $1 "is not a user on the system."
  #   exit 1
  fi
done
