# NHIOT Pipeline

To start run the subscriber which would be the Raspberry Pi or IOT. 
```
python NHSub.py
```
Then run the publisher which will be the main device. This would be the admin that wants to test the executable from a distance with unittests.
```
python -m unittest NHUnitPub.py
```

## Data Pipeline

1. Create aretefact 
2. Upload artefact to google cloud storage
3. Pull google cloud storage artefact from raspberry pi
4. Create version control with hashes.

# Create AWS IoT Broker
https://chatgpt.com/c/693c1e00-27fc-832c-99c4-f8de3b7067cd



# TODO
1. Subscriber, Publisher, Build Executable and Run Executable works. Now just kwargs for function name in C file and args for parameters then validation in unittest then data collection.

This is not in the position to be able to be run from other machines yet because of the aws iot permissions and github tokens.