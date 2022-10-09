# Sendroid
### Warning
Project alpha version is still in build, please do not take project and its README seriously for now.
### Description
Do not know the *plyer* module enough to use it? this module is the answer, I posted it on *PyPI* for developers **who need simple and intuitive access** to android sensor data (like I do).\
Everything is commented so if you are not sure what class/method is used for, then **look up the source code**, I have tried to make things obvious in this documentation file.
### Structure
##### Importing
Module contains separate management classes for each sensor that is supported, thus if you want to get access to *Accelerometer* class you write import statement as shown below:
```python
from sendroid.accelerometer import Accelerometer
```
This rule applies to other sensors too.
##### Common methods
Every sensor inherits from class *Sensor* which contains a few methods:
- **\_\_init\_\_**\
Initializes the *Sensor* class instance
- **\_\_enter\_\_**\
Called on *with* statement enter (object creation), enables the sensor
- **\_\_exit\_\_**\
Called on *with* statement exit (end of indentation block), disables the sensor
- **start**\
Starts the sensor job (enables it)
- **close**\
Stops the sensor job (disables it)
