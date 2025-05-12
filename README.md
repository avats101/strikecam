# StrikeCam

StrikeCam is a project focused on detecting and classifying military assets in images and videos using advanced computer vision techniques. To setup the Pi and laptop, follow the instructions mentioned in the [Setup Instructions](setup.pdf) document. Following the documentation you could be able to achieve this [demonstration](https://youtube.com/shorts/MGN6QMfUiwU) The project is designed to run on a Raspberry Pi, which captures images and sends them to a laptop for processing and analysis. 

## Dataset

The model is trained on the [Military Assets Dataset (YOLOv8 Format)](https://www.kaggle.com/datasets/rawsi18/military-assets-dataset-12-classes-yolo8-format). This dataset contains labeled images of various military and civilian assets.

## Model Overview

The model is built using the YOLOv8 architecture, a state-of-the-art object detection framework. Training can be performed using the `train.py` script provided in this repository.

### Key Features (with the Deployment on Pi):
- Detects and classifies 12 distinct military and civilian assets.
- Raspberry Pi boots and becomes a hotspot.
- Laptop connects to PiHotspot (10.42.0.1 gateway).
- yolo.py autostarts and captures from PiCamera.
- Pi sends payloads (JSON + base64 image) to the laptop server.
- Laptop saves images and logs JSON per detection.

### Classes:
1. **Camouflage Soldier**: Soldiers in camouflaged gear for stealth and defense.
2. **Weapon**: Handheld firearms and other weaponry.
3. **Military Tank**: Armored combat vehicles with heavy weaponry.
4. **Military Truck**: Troop or supply transport trucks.
5. **Military Vehicle**: General military vehicles excluding tanks or trucks.
6. **Civilian**: Non-military, unarmed individuals.
7. **Soldier**: Uniformed military personnel without camouflage.
8. **Civilian Vehicle**: Civilian cars and trucks.
9. **Military Artillery**: Large-caliber, heavy-armament systems.
10. **Trench**: Ground combat defensive earthworks.
11. **Military Aircraft**: Combat, surveillance, or transport planes and helicopters.
12. **Military Warship**: Naval vessels for warfare.

---

For more details on usage, contact me.