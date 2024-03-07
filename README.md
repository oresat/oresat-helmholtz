# oresat-helmholtz

![alt text](https://user-images.githubusercontent.com/33878769/50576984-cde2d900-0dd2-11e9-8117-1c2e21f85c7d.png)

## Installation

```shell
$ pip3 install --user -r requirements.txt
```

## Find PSUs

As a sanity check, you can look through your dmesg logs to find the TTYs your psus are wired to.
```
dmesg | grep 'pl2303 converter now attached' | sed -e 's/.\+\(ttyUSB[0-9]\)/\1/g' | sort | uniq
```

## Magnetic Environment Simulator for CubeSats

SOP can be found [here](http://psu-epl.github.io/doc/equip/testing/ETL/) at the Electronics Prototyping Lab website

![alt text](https://user-images.githubusercontent.com/33878769/48651456-dfe9f300-e9af-11e8-9a90-02227cccc314.jpg)

MCECS BETA Project 2018
