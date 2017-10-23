# Apigee Playground

Trying out some features of Apigee. Created a IoT OAuth client for the EnviroPhat hat on the Raspberry Pi.

## <a name="prerequisites"></a>Prerequisites:

*	[Apigee Account](https://apigee.com)
*	[Rasperry Pi](https://www.raspberrypi.org)
*	[Rasperry Pi Rasbian OS installed](https://www.raspberrypi.org/documentation/installation/installing-images/)
*	[Rasperry Pi Rasbian OTG Configured](https://gist.github.com/gbaman/975e2db164b3ca2b51ae11e45e8fd40a)


### <a name="configuration"></a>Configuration:


### <a name="Example"></a>Example:

Create an application in Apigee, associate it to the EnviroPhat API, and capture the CLIENT_ID and CLIENT_SECRET of the app. The app credentials can be extracted manually from the Apigee Edge interface or programatically via Apigee Edge admin API.

Manual:

	export CLIENT_ID=<CLIENT_ID>; 
	export CLIENT_SECRET=<CLIENT_SECRET>;

Automatic:

    EMAIL=phriscage@gmail.com; 
    stty -echo; read -p "Password: " PASSWORD; echo; stty echo; export BASIC_AUTH=`echo -n $EMAIL:$PASSWORD | base64`; 

    APP_ID=79535e6d-5dac-4391-bfa8-52a6650d8ee1;
    JSON=`curl -s -H "Authorization: Basic $BASIC_AUTH" "https://api.enterprise.apigee.com/v1/o/phriscage-trial/apps/$APP_ID?includeCred=true&expand=true"`; export CLIENT_ID=`echo $JSON | python -c "import sys, json; print json.load(sys.stdin)['credentials'][0]['consumerKey']"`; echo "CLIENT_ID: $CLIENT_ID"; export CLIENT_SECRET=`echo $JSON | python -c "import sys, json; print json.load(sys.stdin)['credentials'][0]['consumerSecret']"`; echo "CLIENT_SECRET: $CLIENT_SECRET"

In addition to the app client credentials, the EnviroPhat IoT requires the OAUTH_TOKEN_URL and PROTECTED_URL when it bootstraps. You can defined these in the [.env](.env) hidden file or via command line. Best practices would leverage Docker secrets or Vault to provide secrets to the application, but this is only for demostration pruposes. 

	export OAUTH_TOKEN_URL=https://phriscage-trial-test.apigee.net/oauth/v2/token
	export PROTECTED_URL=https://phriscage-trial-test.apigee.net/envirophat/v4/data

Try using curl on the PROTECTED_URL without credentials. Will you see a 401 or 403 response?:

    curl -i $PROTECTED_URL
    
Let's get OAuth credentials for the application via curl. EnviroPhat is a trusted app that has can store the application credentials in a secure location:

    export BASIC_CLIENT_AUTH=`echo -n $CLIENT_ID:$CLIENT_SECRET | base64`; export ACCESS_TOKEN=`curl -s -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Basic $BASIC_CLIENT_AUTH" -X POST --data-urlencode 'grant_type=client_credentials' https://phriscage-trial-test.apigee.net/oauth/v2/token | python -c "import sys, json; print json.load(sys.stdin)['access_token']"`; echo $ACCESS_TOKEN;

Now try to call the PROTECTED_URL with credentials. Will you see a 403 now or 404?
    
    curl -i -H "Authorization: Bearer $ACCESS_TOKEN" $PROTECTED_URL 


Verify Docker is running on the IoT Device and Docker-Compose exists 

    docker version
    docker-compose version

Run the *phriscage/iot_enviro_client* Docker container with privledged mode via Docker Compose [config](docker-compose.yml). _Docker Swarm priviledged mode is not available yet. [issue](https://github.com/moby/moby/issues/24862)_

	make 

View the logs

	make logs 

View the charts 

	https://apigee.com


### <a name="development"></a>Development:

Sample OAuth commands:

* Call OAuth 2.0 client credentials grant.
Needed to adjust the <GrantType>request.formparam.grant_type</GrantType>

```
export BASIC_CLIENT_AUTH=`echo -n $CLIENT_ID:$CLIENT_SECRET | base64`; export ACCESS_TOKEN=`curl -s -H 'Content-Type: application/x-www-form-urlencoded' -H "Authorization: Basic $BASIC_CLIENT_AUTH" -X POST --data-urlencode 'grant_type=client_credentials' https://phriscage-trial-test.apigee.net/oauth/v2/token | python -c "import sys, json; print json.load(sys.stdin)['access_token']"`; echo $ACCESS_TOKEN;
```

* Call protected resource:

```
curl -i -X POST -H "Authorization: Bearer $ACCESS_TOKEN" https://phriscage-trial-test.apigee.net/envirophat/v4/data 
```

* Call protected resource with AWS credentials;

```
export AWS_CLIENT_AUTH=`echo -n $AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY | base64`;
```

```
curl -i -H "Authorization: Bearer $ACCESS_TOKEN" -H "AWS-Authorization: $AWS_CLIENT_AUTH" https://phriscage-trial-test.apigee.net/test/aws -d '{"a": 123}'
```


* Set/Get encrypted vaults:

```
curl -i -X GET -H "Authorization: Basic $BASIC_AUTH" 'https://api.enterprise.apigee.com/v1/o/phriscage-trial/e/test/vaults'
```


### <a name="todo"></a>To-Do:

*	Add exception and retry handling
* 	Unit tests?
