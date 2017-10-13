// AWS DynamoDB example
var http = require('http');
var url = require('url');
var apigee = require('apigee-access');
var uuidv4 = require('uuid/v4');
var AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'});

// Check if isObject is an object
function isObject(val) {
        if (val === null) { return false;}
        return ( (typeof val === 'function') || (typeof val === 'object') );
}

// format the DynamoDB item and insert the document
function putDynamoData(resp, data) {

    // set the primary key
    var uuid = uuidv4();
    data['id'] = uuid;
    // set created_at time stamps
    var date = new Date();
    data['created_at'] = date.toISOString(); 
	// Create DynamoDB document client
	var docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
	//var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

	var params = {
   		Item: data,
  		ReturnConsumedCapacity: 'TOTAL', 
  		TableName: 'test'
	};

	//dynamodb.putItem(params, function(err, data) {
	docClient.put(params, function(err, responseData) {
	    if (err) {
            var message = 'Something went wrong';
		    console.log(err, err.stack); // an error occurred
            sendResponse(resp, {message: message, error: err}, 500);
        } else {
		    console.log(responseData);   // successful response
            resp.setHeader('X-Apigee-UUID', uuid);
            sendResponse(resp, {message: 'Success', data: data, response: responseData}, 201);
        }
	});
}

// Build a custom response
function sendResponse(resp, data, status) {
    var responseHeaders = {
        'Content-Type': 'application/json', 
        //'X-Apigee-messageId': messageId
    }
    // Let's add the request headers if exist
    //var key, requestHeaders = ['user-agent', 'x-forwarded-for'];
    //for (var key in req.headers) {
    //for (key of requestHeaders) {
        //if (req.headers.hasOwnProperty(key)) {
            //responseHeaders['X-Request-' + key] = req.headers[key];
        //}
    //}
    data['status'] = status
    resp.writeHead(status, responseHeaders);
    var json = JSON.stringify(data, null, 4);
    resp.end(json + '\n');
}

// main server logic
var server = http.createServer(function(req, resp) {
	console.log('Processing request url: ' + req.url);
	console.log(req.headers);
    //var queryData = url.parse(req.url, true).query;
	//console.log(queryData);
    //AWS.config.update({accessKeyId: queryData.client_id});
    //AWS.config.update({secretAccessKey: queryData.client_secret});
    var messageId = apigee.getVariable(req, 'messageid') ? messageId : ""
    resp.setHeader('X-Apigee-messageId', messageId);
    var payload = '';
    req.on('data', function (chunk) {
        payload += chunk;
    });
    var jsonPayload = {}
    req.on('end', function () {
        console.log('payload: ' + payload);
        try {
            jsonPayload = JSON.parse(payload) || {};
            if (isObject(jsonPayload)){
                putDynamoData(resp, jsonPayload);
            } else {
                var message = 'JSON payload required';
                console.log(message);
                sendResponse(resp, {error: message}, 400);
            }
        } catch (e) {
            var message = 'JSON payload required';
            console.log(e);
            sendResponse(resp, {error: message}, 400);
           // this.emit('error');
        }
    })
});

server.on('error', function (e) {
    // Handle your error here
     console.log("asdfasdf");
     sendResponse(resp, {error: message}, 400);
});

server.listen(9000, function() {
    console.log('Node HTTP server is listening');
});
