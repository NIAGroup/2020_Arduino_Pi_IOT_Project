# 2020_Arduino_Pi_IOT_Project [![CircleCI](https://circleci.com/gh/adonaygyb/2020_Arduino_Pi_IOT_Project.svg?style=shield)](https://circleci.com/gh/adonaygyb/2020_Arduino_Pi_IOT_Project)

A pulse-width modulation project that leverages a Flask webapp for remote access hosted on a Raspberry PI communicating via bluetooth between a cluster of Arduinos.


## Required Hardware

* Arduino & Supplies [LINK](https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4/ref=sr_1_1_sspa?dchild=1&keywords=arduino+uno&qid=1594145201&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzOENFRUxFTVlBUklEJmVuY3J5cHRlZElkPUEwOTIwMjA3MUxQOFZUSjIxT0wzSyZlbmNyeXB0ZWRBZElkPUExMDAxMzc2M1RTT1dKR0NNR05TQiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=):  
    * Arduino Uno [alternate(s): arduino nano] 
    * Ultrasonic Sensor [alternate(s): IR Range Finder]
    * Stepper Motor & Driver
    * Jumper Wires (male-to-female & female-to-female)
* Raspberry Pi:
    * Pi 3 B+ & Power Supply [LINK](https://www.amazon.com/CanaKit-Raspberry-Power-Supply-Listed/dp/B07BC6WH7V/ref=sr_1_4?crid=34MED5FZB2G0L&dchild=1&keywords=raspberry+pi+3&qid=1594145572&sprefix=raspberry+%2Caps%2C241&sr=8-4) [alternate(s): Pi 4, Pi Zero W]
    * 32GB Micro SD Card [LINK](https://www.amazon.com/SanDisk-Ultra-microSDXC-Memory-Adapter/dp/B073JWXGNT/ref=sr_1_3?crid=2E17J9I1WJHVM&dchild=1&keywords=32gb+micro+sd+card&qid=1594145686&sprefix=32GB+%2Caps%2C252&sr=8-3) (16GB may be enough, but for future scaling up 32GB or greater would be best)
* Raspberry Pi Camera [LINK](https://www.amazon.com/Arducam-Raspberry-Camera-Module-Megapixel/dp/B083BHJZ16/ref=sr_1_4?dchild=1&keywords=raspberry+pi+camera&qid=1594145852&sr=8-4)
* Ping Pong Ball [LINK](https://www.amazon.com/meizhouer-Colored-Entertainment-Tennis-Advertising/dp/B07JNCVVMF/ref=sxin_7?ascsubtag=amzn1.osa.64b70dad-9350-49c9-849c-d42395af5029.ATVPDKIKX0DER.en_US&creativeASIN=B07JNCVVMF&crid=1Q8B1E98FMBEB&cv_ct_cx=ping+pong+balls&cv_ct_id=amzn1.osa.64b70dad-9350-49c9-849c-d42395af5029.ATVPDKIKX0DER.en_US&cv_ct_pg=search&cv_ct_wn=osp-single-source&dchild=1&keywords=ping+pong+balls&linkCode=oas&pd_rd_i=B07JNCVVMF&pd_rd_r=6f9143f5-dc06-4d7a-be18-363f493eefa9&pd_rd_w=JGlTs&pd_rd_wg=wEyt2&pf_rd_p=ad792221-7c05-4384-852b-971b142fa109&pf_rd_r=HN5YJ39XYFMPRWP6BR46&qid=1594145725&sprefix=ping+pong%2Caps%2C266&sr=1-1-72d6bf18-a4db-4490-a794-9cd9552ac58d&tag=bargainsbaby-20)
* HC-05 Bluetooth Module [LINK](https://www.amazon.com/Wireless-Bluetooth-Transceiver-Module-Arduino/dp/B07T7ZZ3S5/ref=sr_1_4?dchild=1&keywords=hc05&qid=1594144714&sr=8-4)
* The Balance Beam 
>NOTE:: The balance beam will have to be hand crafted for now. When a tested design has been found/made it can be included in the list.  

## Prior Knowledge Needed/Googled

* Basic linux commands (i.e. cd, ls, mkdir, etc)
* Basic C/C++ understanding for arduino
* Basic circuit wiring understanding
* Intermediate Python 
* Basic HTML

## Expected Gained Knowledge  

* PWM - Pulse Width Modulation for Stepper Motor Control [EXPLAINED](https://www.youtube.com/watch?v=avrdDZD7qEQ)
* Bluetooth communication [ARDUINO & HC-05](https://www.youtube.com/watch?v=OhnxU8xALtg) [Raspberry PI](https://www.youtube.com/watch?v=F5-dV6ULeg8)
* Web Server Website/WebApp setup using apache2 [TUTORIAL](https://www.youtube.com/watch?v=dmBqzq3M5jQ)
* Front-End & Back-End Development
* PID - Proportional-Integral-Derivative Controller [EXPLAINED](https://www.youtube.com/watch?v=g7apd9a7Jxs)
