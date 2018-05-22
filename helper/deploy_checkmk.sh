#!/bin/bash

set -e
# set -x

url="$1"
user="$2"
pass="$3"
hash="$4"
host="$5"
folder="$6"

tmpdir=$(mktemp -d)

if [ -x /usr/bin/dpkg ]; then
  tmpfile=$tmpdir/checkmkagent.deb
  wget -O $tmpfile "$url/check_mk/download_agent.py?hash=$hash&os=linux_deb&_username=$user&_secret=$pass"
  if dpkg -l check-mk-agent > /dev/null; then
    dpkg -P check-mk-agent
  fi
  apt-get install xinetd curl
  dpkg -i $tmpfile
elif [ -x /usr/bin/rpm -o -x /bin/rpm ]; then
  tmpfile=$tmpdir/checkmkagent.rpm
  wget -O $tmpfile "$url/check_mk/download_agent.py?hash=$hash&os=linux_rpm&_username=$user&_secret=$pass"
  if rpm -q check-mk-agent > /dev/null; then
    rpm -e check-mk-agent
  fi
  if [ -x /usr/bin/zypper ]; then
      zypper install xinetd curl
  elif [ -x /usr/bin/yum ]; then
      yum install xinetd curl
  fi
  rpm -i $tmpfile
else
  echo "Unknown package system"
  exit 1
fi

rm -rfv $tmpdir
rm -fv /etc/cmk-update-agent.state

echo
read -p "Agent installed"

curl -v "$url/check_mk/webapi.py?action=add_host&_username=$user&_secret=$pass" -d "request={\"hostname\": \"$host\", \"folder\": \"$folder\"}"

echo
read -p "Host created"

curl -v "$url/check_mk/webapi.py?action=activate_changes&_username=$user&_secret=$pass"

echo
read -p "Changes activated"

/usr/bin/cmk-update-agent register -v -U $user -S $pass -H $host

echo
read -p "Agent Updater registered"

curl -v "$url/check_mk/webapi.py?action=bake_agents&_username=$user&_secret=$pass"

echo
read -p "Agents baked"

/usr/bin/cmk-update-agent -v

echo
read -p "Agent updated"

curl -v "$url/check_mk/webapi.py?action=discover_services&_username=$user&_secret=$pass" -d "request={\"hostname\": \"$host\"}"

echo
read -p "Host services discovered"

curl -v "$url/check_mk/webapi.py?action=activate_changes&_username=$user&_secret=$pass"

echo
read -p "Changes activated"
