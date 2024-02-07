# SesameChecker
Python class to check Sesame criteria for HVSR measures:
  -  **sesame.py** contains the class definition;
  -  **sesame_utils.py** contains some utility functions to read Geopsy .hv (and .log) output files.

# Usage example
```
  from sesame_utils import geopsy_hv_reader
  from sesame import SesameChecker
  
  hvfile = /path/to/file.hv
  logfile = /path/to/file.log
  
  inputs = geopsy_hv_reader(hvfile, logfile)
  SC = SesameChecker(*inputs)
  criteria = SC.runChecks(explicit_criteria=True)
```

## Dependencies
**numpy** is the only current dependence needed.

## Disclaimer
The code in this repository has not been thoroughly tested!\
If you find bugs or errors during use, please report them.
