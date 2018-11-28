#!/usr/bin/env python
# -*- coding: utf-8 -*-
#**
#
#########
# trape #
#########
#
# trape depends of this file
# For full copyright information this visit: https://github.com/jofpin/trape
#
# Copyright 2018 by Jose Pino (@jofpin) / <jofpin@gmail.com>
#**
import hashlib
import httplib 
import json
import os
import random
import socket
import sys
import threading
import time

import requests
from colorama import Fore, Style, init
init()

banner = """\033[H\033[J
\t{redBold} _
\t{redBold}| |_   ____ ____ ____   ____
\t{redBold}|  _) / ___) _  |  _ \ / _  )
\t{redBold}| |__| |  ( ( | | | | ( (/ /
\t{redBold} \___)_|   \_||_| ||_/ \____)
\t{redBold}                |_|{white} 2018 by {whiteBold}Jose Pino{white} ({blue}@jofpin{white})
\t-----------------------------------------------
\t{green}People tracker on internet for OSINT research {white}|=-
\t-----------------------------------------------
\t| v{redBold}2.0{white} |
\t--------\n"""


class utils:
    # Functions 1to get is right
    def __init__(self):
        pass

    # Simplification print
    @staticmethod
    def Go(string):
        print(string)

    # All color for design terminal UI
    Color = {
      "cyan": Style.NORMAL+Fore.CYAN,
      "cyanBold": Style.BRIGHT+Fore.CYAN,
      "blue": Fore.BLUE,
      "blueBold": Style.BRIGHT+Fore.BLUE,
      "red": Style.NORMAL+Fore.RED,
      "redBold": Style.BRIGHT+Fore.RED,
      "green": Style.NORMAL+Fore.GREEN,
      "greenBold": Style.BRIGHT+Fore.GREEN,
      "white": Style.NORMAL+Fore.WHITE,
      "whiteBold": Style.BRIGHT+Fore.WHITE,
      "yellow": Style.NORMAL+Fore.YELLOW,
      "yellowBold": Style.BRIGHT+Fore.YELLOW
    }

    # Text in bold, lines and end.
    Text = {
      "underline": Style.NORMAL+Fore.YELLOW,
      "bold": Style.BRIGHT,
      "end": Style.NORMAL+Fore.WHITE
    }
    
    @staticmethod
    def colorize(fmt):
        return fmt.format(**utils.Color)

    # Banner trape
    @staticmethod
    def banner():
        utils.Go(utils.colorize(banner))

    # Loader with console cleaning and OS checking    
    @staticmethod
    def checkOS():
        if "posix" in os.name:
            os.system("clear")
            pass
        elif "nt" in os.name:
            pass
            #os.system("cls")
            #utils.Go("Currently there is no support for Windows.")
        else:
            pass
        utils.Go(utils.colorize("Loading {blue}trape{white}..."))
        time.sleep(0.4)

    # Generates a unique token of up to 30 characters.
    @staticmethod
    def generateToken(length=8):
        chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz01234567890')
        random.shuffle(chars)
        chars = ''.join(chars)
        sha1 = hashlib.sha1(chars.encode('utf8'))
        token = sha1.hexdigest()
        return token[:length]

    # Simple port scan for the victim or user    
    @staticmethod
    def portScanner(victimIP):
        clientIP = socket.gethostbyname(victimIP)
        listPorts = (0, 21, 22, 23, 25, 42, 43, 53, 67, 79, 80, 102, 110, 115, 119, 123, 135, 137, 143, 161, 179, 379, 389,
                     443, 445, 465, 636, 993, 995, 1026, 1080, 1090, 1433, 1434, 1521, 1677, 1701, 1720, 1723, 1900, 2409,
                     2082, 2095, 3101, 3306, 3389, 3390, 3535, 4321, 4664, 5190, 5500, 5631, 5632, 5900, 65535, 7070, 7100,
                     8000, 8080, 8880, 8799, 9100)
        results = []
        for port in listPorts:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            result = sock.connect_ex((clientIP, port))
            sys.stdout.flush()
            if result == 0:
                results.append(str(port))
        return ",".join(results)

    # Local port check to allow trape to run    
    @staticmethod
    def checkPort(port):
        try:
            clientIP = socket.gethostbyname('127.0.0.1')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((clientIP, port))
            sys.stdout.flush()
            if result == 0:
                return False
            else:
                try:
                    return 0 < int(port) < 65535
                except Exception as e:
                    return False
        except Exception as e:
            return False

    @staticmethod
    def checkUrl(url):
        c = httplib.HTTPConnection(url, timeout=5)
        try:
            c.request("HEAD", "/")
            c.close()
            return True
        except Exception as e:
            c.close()
            return False

    # Goo.gl shortener service
    @staticmethod
    def gShortener(api_key, p_url):
        url = "https://www.googleapis.com/urlshortener/v1/url?key=" + api_key
        payload = '{"longUrl":"' + p_url + '"}'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=payload, headers=headers)
        return r

    # Autocompletion
    @staticmethod
    def niceShell(text, state):
        matches = [i for i in commands if i.startswith(text)]
        if state < len(matches):
            return matches[state]
        else:
            return None
