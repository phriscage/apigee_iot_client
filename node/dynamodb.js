// AWS DynamoDB example
var http = require('http');
var apigee = require('apigee-access');
var uuidv4 = require('uuid/v4');
var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});
//
// Get AWS credentials KVM values
// var kvm = apigee.getKeyValueMap('aws', 'environment');
// kvm.get('client_id', function(err, client_id) {
//     AWS.config.accessKeyId = client_id;
// });
// kvm.get('client_secret', function(err, client_secret) {
//     AWS.config.secretAccessKey = client_secret;
// });

// Check if isObject is an object
function isObject(val) {
        if (val === null) { return false;}
        return ( (typeof val === 'function') || (typeof val === 'object') );
}

// create the DynamoDB item
function putDynamoData(req, resp, data) {

    // set the primary key
    data['id'] = uuidv4();
	// Create DynamoDB document client
	var docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
	//var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

	var params = {
   		Item: data,
  		ReturnConsumedCapacity: "TOTAL", 
  		TableName: "test"
	};

    //sendResponse(req, resp, {params: params}, 200);
	//dynamodb.putItem(params, function(err, data) {
	docClient.put(params, function(err, responseData) {
	    if (err) {
            var message = "Something went wrong";
		    console.log(err, err.stack); // an error occurred
            sendResponse(req, resp, {message: message, error: err}, 500);
        } else {
		    console.log(responseData);   // successful response
            sendResponse(req, resp, {message: "Success", data: data, response: responseData}, 201);
        }
	});
}

// Build a custom response
function sendResponse(req, resp, data, status) {
    var messageId = apigee.getVariable(req, 'messageid') ? messageId : ""
    var responseHeaders = {
        "Content-Type": "application/json", 
        "X-Apigee-messageId": messageId
    }
    // Let's add the request headers if exist
    var key, requestHeaders = ['user-agent', 'x-forwarded-for'];
    //for (var key in req.headers) {
    for (key of requestHeaders) {
        if (req.headers.hasOwnProperty(key)) {
            responseHeaders['X-Request-' + key] = req.headers[key];
        }
    }
    data['status'] = status
    resp.writeHead(status, responseHeaders);
    var json = JSON.stringify(data, null, 4);
    resp.end(json + '\n');
}

var svr = http.createServer(function(req, resp) {
	console.log('Processing request url: ' + req.url);
	console.log(req.headers);
    var payload = "";
    req.on('data', function (chunk) {
        payload += chunk;
    });
    var jsonPayload = {}
    req.on('end', function () {
        console.log('payload: ' + payload);
        try {
            jsonPayload = JSON.parse(payload);
            if (isObject(jsonPayload)){
                putDynamoData(req, resp, jsonPayload);
            } else {
                var message = "JSON payload required";
                console.log(message);
                sendResponse(req, resp, {error: message}, 400);
            }
        } catch (e) {
            console.error(e);
            var message = "JSON payload required";
            sendResponse(req, resp, {error: message}, 400);
        };
    })
});

svr.listen(9000, function() {
    console.log('Node HTTP server is listening');
});
