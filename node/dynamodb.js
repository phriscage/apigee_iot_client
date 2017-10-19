/*
    Name: server.js
    Developer: Chris Page
    Email: phriscage@gmail.com
    Purpose:
        An AWS DynamoDB NodeJS server example. 
        Start a server and set the callback for a valid JSON
        payload to store the document in DynamoDB. The AWS
        credentials are provided in a custom header that is
        determined outside this logic.
*/

var http = require('http');
var apigee = require('apigee-access');
var uuidv4 = require('uuid/v4');
var AWS = require('aws-sdk');
const awsRegion = 'us-east-1';
const awsDynamoDBapiVersion = '2012-08-10';

AWS.config.update({region: awsRegion});

// Check if isObject is an object
function isObject(val) {
        if (val === null) { return false;}
        return ( (typeof val === 'function') || (typeof val === 'object') );
}

// format the DynamoDB item and insert the document
// with unique id and createdAt timestamps.
function putDynamoData(resp, data) {

    var uuid = uuidv4();
    var date = new Date();
    data['id'] = uuid;
    data['created_at'] = date.toISOString();
    // Create DynamoDB document client
    var docClient = new AWS.DynamoDB.DocumentClient({apiVersion: awsDynamoDBapiVersion});

    var params = {
        Item: data,
        ReturnConsumedCapacity: 'TOTAL',
        TableName: 'test'
    };

    docClient.put(params, function(err, responseData) {
        if (err) {
            var message = 'Something went wrong';
            console.log(err, err.stack); // an error occurred
            sendResponse(resp, {message: message, error: err}, 500);
        } else {
            console.log(responseData);   // successful response
            resp.setHeader('X-AWS-DynamoDB-UUID', uuid);
            sendResponse(resp, {message: 'Success', data: data, response: responseData}, 201);
        }
    });
}

// Build a custom response
function sendResponse(resp, data, status) {
    data['status'] = status
    var responseHeaders = {
        'Content-Type': 'application/json',
    }
    resp.writeHead(status, responseHeaders);
    var json = JSON.stringify(data, null, 4);
    resp.end(json + '\n');
}

// main server logic
// capture the payload data before continuing response
// and enforce basic validation for JSON.
// parse the AWS credentials from a custom header for testing
var server = http.createServer(function(req, resp) {
    console.log('Processing request url: ' + req.url);
    //  console.log(req.headers);
    if ("aws-authorization" in req.headers) {
        var aws_creds = req.headers['aws-authorization'];
        //var [client_id, client_secret] = Buffer(
            //aws_creds, 'base64'
        //).toString().split(':', 2);
        var creds = aws_creds.split(':', 2);
        if (creds.length === 2) {
            var client_id = creds[0];
            var client_secret = creds[1];
            AWS.config.update({
                accessKeyId: client_id,
                secretAccessKey: client_secret
            });
            resp.setHeader('X-AWS-client_id', client_id);
            resp.setHeader('X-AWS-client_secret', client_secret);
        }

    }
    var messageId = apigee.getVariable(req, 'messageid') || ""
    resp.setHeader('X-Apigee-messageId', messageId);
    // Let's add the request headers if exist
    //var key, requestHeaders = ['user-agent', 'x-forwarded-for'];
    //for (var key in req.headers) {
    //for (key of requestHeaders) {
        //if (req.headers.hasOwnProperty(key)) {
            //responseHeaders['X-Request-' + key] = req.headers[key];
        //}
    //}
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
                //sendResponse(resp, {data: req.headers}, 200);
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

// Handle any http server errors
server.on('error', function (e) {
    // Handle your error here
    message = "Something broke"
    console.log(e)
    sendResponse(resp, {error: message}, 500);
});

// Start the server on port 9000
server.listen(9000, function() {
    console.log('Node HTTP server is listening');
});
