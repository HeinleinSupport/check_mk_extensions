#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2015 Heinlein Support GmbH
#

import sys

baseurl = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
email = sys.argv[4]
command_executor = sys.argv[5]

from selenium import webdriver

try:
    mydriver = webdriver.Remote(
        desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
        command_executor=command_executor
    )	

    mydriver.get(baseurl)
    mydriver.maximize_window()
    mydriver.implicitly_wait(5)
except:
    print("Error! Cant init the Webdriver")
    sys.exit(3)

#Clear Username TextBox if already allowed "Remember Me" 
try:
    mydriver.find_element_by_name("username").clear()
except:
    print("No Element found name=username")
    sys.exit(3)

#Write Username in Username TextBox
try:
    mydriver.find_element_by_name("username").send_keys(username)
except: 
    print("No Element found name=username")
    sys.exit(3)

##Clear Password TextBox if already allowed "Remember Me" 
try:
    mydriver.find_element_by_name("password").clear()
except:
    print("No Element found name=password")
    sys.exit(3)

#Write Password in password TextBox
try:
    mydriver.find_element_by_name("password").send_keys(password)
except:
    print("Error! Can't set the password.")
    sys.exit(3)

#Click Login button
try:
    mydriver.find_element_by_name('Login').click()
except:
    print("Error Cant 'click' Element! name=Login")
    sys.exit(3)

mydriver.implicitly_wait(5)

try:
    mydriver.find_element_by_id('io-ox-core') 
    print("Logged In")
except:
    print("Critical", "Kann Id der Seite nicht finden, kein Login")
    sys.exit(2)

sys.exit(0)
