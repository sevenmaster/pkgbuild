#!/usr/bin/bash

#newtask -p mediatomb /usr/bin/mediatomb --home /etc/mediatomb --daemon $* 
/usr/bin/mediatomb --home /etc/mediatomb --daemon $* &
