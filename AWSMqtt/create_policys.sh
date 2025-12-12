aws iot create-policy --policy-name MyIoTPolicy --policy-document file://iot_policy.json
aws iot attach-policy --policy-name MyIoTPolicy --target <certificateArn>
aws iot attach-thing-principal --thing-name Amari-Desktop-CREM --principal <certificateArn>
