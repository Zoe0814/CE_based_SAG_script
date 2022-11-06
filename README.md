# CE_based_SAG_script

This script aims to automatically execute the three-step algorithm experiment on the server.

## first and second step
To run the first and second step algorithm, we should comment out one line in the **config** file as:
> //#define CONFIG_COUNTER_EXAMPLE

The rest remain same. Follow by that we need to change the python file (last line) in the **runme.sh** as 
> python3 ce_tas_test_script.py

## third step
To run the third step algorithm, we should define in the **config** file as:
> #define CONFIG_COUNTER_EXAMPLE

Then we should replace the last line in the *runme.sh** as 
> python3 third_test_script.py

## License
IRIS group
