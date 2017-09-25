# Apigee Playground

Trying out some features of Apigee. Created a IoT OAuth client for the EnviroPhat hat on the Raspberry Pi.

## <a name="prerequisites"></a>Prerequisites:

*	[Apigee Account](https://apigee.com)
*	[Rasperry Pi](https://www.raspberrypi.org)
*	[Rasperry Pi Rasbian OS installed](https://www.raspberrypi.org/documentation/installation/installing-images/)
*	[Rasperry Pi Rasbian OTG Configured](https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a)


### <a name="configuration"></a>Configuration:


### <a name="Example"></a>Example:

Create an application in Apigee and capture the CLIENT_ID and CLIENT_SECRET. 

	export CLIENT_ID=<CLIENT_ID>; 
	export CLIENT_SECRET=<CLIENT_SECRET>;
	export OAUTH_TOKEN_URL=https://phriscage-trial-test.apigee.net/oauth/v2/token
	export PROTECTED_URL=https://phriscage-trial-test.apigee.net/envirophat

Run the *phriscage/iot_enviro_client* Docker container with privledged mode via Docker Compose [config](docker-compose.yml). _Docker Swarm priviledged mode is not available yet. [issue](https://github.com/moby/moby/issues/24862)_

	make 

View the logs

	make logs 

View the charts 

	https://apigee.com


### <a name="development"></a>Development:

Sample OAuth commands:

* Set session Basic Auth

```
export EMAIL=phriscage@gmail.com; 
stty -echo; read -p "Password: " PASSWORD; echo; stty echo; export BASIC_AUTH=`echo -n $EMAIL:$PASSWORD | base64`; 
```

* List Organization API products: 

```
curl -i -H "Authorization: Basic $BASIC_AUTH" https://api.enterprise.apigee.com/v1/o/phriscage-trial/apiproducts
```

* List Apps with credentials:

```
curl -i -H "Authorization: Basic $BASIC_AUTH" 'https://api.enterprise.apigee.com/v1/o/phriscage-trial/apps?includeCred=true&expand=true'
```

* Set session Basic client Auth:

```
export CLIENT_KEY=<abc>;
export CLIENT_SECRET=<123>;
export BASIC_CLIENT_AUTH=`echo -n $CLIENT_KEY:$CLIENT_SECRET | base64`;
```

* Call OAuth 2.0 client credentials grant.
Needed to adjust the <GrantType>request.formparam.grant_type</GrantType>

```
export ACCESS_TOKEN=`curl -s -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Basic $BASIC_CLIENT_AUTH" -X POST --data-urlencode 'grant_type=client_credentials' https://phriscage-trial-test.apigee.net/oauth/v2/token | python -c "import sys, json; print json.load(sys.stdin)['access_token']"`; echo $ACCESS_TOKEN;
```

* Call protected resource:

```
curl -i -H "Authorization: Bearer $ACCESS_TOKEN" https://phriscage-trial-test.apigee.net/envirophat
```


### <a name="todo"></a>To-Do:

*	Add exception and retry handling
* 	Unit tests?
