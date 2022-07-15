#!/bin/bash
echo "Store new data in here" >> $HOME/demand_data.txt && stat -c "%y"  $HOME/demand_data.txt >> $HOME/demands.log
