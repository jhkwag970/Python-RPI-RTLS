# Python-RPI-RTLS
Python-DWM1001 Real Time Location System for Data Collection

Dr. Yilmaz and Dr. Toth at the PCVLab. 

# Sensors 

<h4>DWM1001-DEV</h4>

DWM1001 uses UWB to measure the distance between anchor and tag. 

More info: https://www.qorvo.com/products/p/MDEK1001#documents

<h4>Adafruit 9-DoF IMU</h4>

IMU uses 3-axis of Gyroscope, Accelerometer, and Magnetometer to measure the orientation of the object: 

More info: https://www.adafruit.com/product/4554

# Past Update

<ol>
  <li>Implement DWM1001 - IMU to RPI</li>
  
  ![image](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/21f6099e-dcc1-4b95-898d-14afe2334823)

  <li>DWM1001 sensor Analysis (More info in the presentation)</li>

![UWB offset](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/650c2d2b-c8ea-4302-866a-80ee4d39b6ad)
![1HZ](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/599cdf59-78b6-48f4-9b69-a58eeddc6ed2)
![30m_2Hz_with_Ant](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/24922d5d-fc36-488e-92cf-d4275a0b34a9)
![25m_2Hz_with_Ant](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/5f406fc4-958d-4e4b-ba83-bed8f1c552e7)



  <li>Calibration of IMU for accurate measurement (More info in the presentation)</li>

  ![3d_cal_uncal](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/1ea148c3-a5a2-4c48-898a-7bb1158555e0)
  ![3d_cal_uncal_2](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/d2fcf259-7bc2-4dfb-b878-a17e36169f49)

  ![2d_mag_cal](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/f4826097-3c2f-40be-8843-7092abac54e2)
  ![2d_mag_uncal](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/7952b031-df15-47f4-8f88-8cb14482bc3a)

  <li>Low Pass Filter of Magnetometer</li>

![turning](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/9840ff50-2aba-48d0-bf90-73f51a3d82ed)
![noturning](https://github.com/jhkwag970/Python-RPI-RTLS/assets/54969114/0a181210-ea8f-454d-92d9-9f12346d8eee)



</ol>
