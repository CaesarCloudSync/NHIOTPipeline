# NHIOT Pipeline
To start in on terminal run the subscriber which would be the Raspberry Pi or IOT. Make sure that in Github actions the correct aarch/x86_64 compiler is installed.
```
python NHSub.py
```
Then first build the artifact with this will build the artifact, in the NHSub window it should say "Downloading artifact 'hello_x86'...":
```
./build_artifact.sh
```

Then run the publisher which will be the main device. This would be the admin that wants to test the executable from a distance with unittests.
```
python -m unittest NHUnitPub.py
```

## Data Pipeline
### Resources used.
1. AWS IoT Core using MQTT - Cloud Architecture
2. Github Actions - DevOps
3. C/C++ Artifacts - Compile Programming.
4. Python - MQTT Subscriptions
5. Unittesting - Testing.

# TODO 
1. Automate AWSMqtt Authentication and Policy creation process.
2. Determine testing metrics like *Mean Time To Repair (MTTR)* and Mean Time Between Failures (MTBF).