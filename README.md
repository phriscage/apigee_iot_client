# Apigee Playground

Trying out some features of Apigee. 

## <a name="prerequisites"></a>Prerequisites:

*	[Apigee Account](https://apigee.com)


### <a name="configuration"></a>Configuration:

### <a name="Example"></a>Example:

Create an application and capture the CLIENT_ID and CLIENT_SECRET. 

Run the Docker container with privledged mode via Docker Compose. _Docker Swarm priviledged mode is not available yet. [issue](https://github.com/moby/moby/issues/24862)_

	make 


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
