# Apigee Playground

Trying out some features of Apigee. 

## <a name="prerequisites"></a>Prerequisites:

*	[Apigee Account](https://apigee.com)


### <a name="configuration"></a>Configuration:

### <a name="development"></a>Development:

Sample OAuth commands:

* Set session Basic Auth

export EMAIL=phriscage@gmail.com; 
stty -echo; read -p "Password: " PASSWORD; echo; stty echo; export BASIC_AUTH=`echo -n $EMAIL:$PASSWORD | base64`; 

* List Organization API products: 

curl -i -H "Authorization: Basic $BASIC_AUTH" https://api.enterprise.apigee.com/v1/o/phriscage-trial/apiproducts

* List Apps with credentials:

curl -i -H "Authorization: Basic $BASIC_AUTH" 'https://api.enterprise.apigee.com/v1/o/phriscage-trial/apps?includeCred=true&expand=true'


* Set session Basic client Auth:

export CLIENT_KEY=<abc>;
export CLIENT_SECRET=<123>;
export BASIC_CLIENT_AUTH=`echo -n $CLIENT_KEY:$CLIENT_SECRET | base64`;

* Call OAuth 2.0 client credentials grant.
Needed to adjust the <GrantType>request.formparam.grant_type</GrantType>


curl -i -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Basic $BASIC_CLIENT_AUTH" -X POST --data-urlencode 'grant_type=client_credentials' https://phriscage-trial-test.apigee.net/oauth/client_credential/accesstoken


