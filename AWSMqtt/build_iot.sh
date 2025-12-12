aws iot create-thing --thing-name Amari-Desktop-CREM
aws iot create-keys-and-certificate --set-as-active
echo "$CERTIFICATE_PEM_CONTENT" > device-certificate.pem.crt
echo "PRIVATE_KEY_CONTENT" > private.pem.key
curl -o AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem