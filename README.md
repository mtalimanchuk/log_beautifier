# log_beautifier
Filters SL4J format logs by given criteria

1. Add logs to libs/log.txt
2. Execute solution.py
3. You will be asked to input filtering criteria. At least 1 must be present

    a) Timespan (From/To dd-MM-yyyy HH:mm.ss). Both have default values and can be omitted

    Example:
    
        From: 02-05-2016 10:00.00
        To: 24-12-2018 12:00.00

    b) Log level. Choose from INFO/ERROR/WARN/TRACE/DEBUG/FATAL. Multiple entries should be divided by space
    
    NOT case sensitive

    Example:
    
        warn error

    c) Instance name. Enter any sequence of characters that should be found in the instance name
    
    Case sensitive

    Example:
    
        c.n.c.sources.URLCon
        
