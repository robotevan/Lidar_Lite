# LidarLite v3 Python

This package contains all the code necessary to control the LidarLite v3 optical range finder via SMBUS.

## Dependancies
You must install smbus2 before running any of this code, you can use pip to install it:
```
pip install smbus2 
```
## Usage Example
The following code creates a new Lidar object, then prints the distance measurement using bias correction.
If the distance is over 5m, it will break out of the loop and stop reading the distance.
```
Lidar = Lidar()
while True:
  dist = Lidar.read_distance()
  print(dist)
  if dist > 500:
    print("The last measurement was over 5m!")
    break
 ```
