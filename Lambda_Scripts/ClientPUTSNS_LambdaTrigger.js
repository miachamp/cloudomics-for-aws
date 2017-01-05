// dependencies

var AWS = require('aws-sdk');
var util = require('util');

// get reference to S3 client 
var s3 = new AWS.S3();

console.log("Loading function");
var AWS = require("aws-sdk");

exports.handler = function(event, context) {
    var eventText = JSON.stringify(event, null, 2);
    var clientID = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' ').replace(/\/.*$/g,''));
    var bucket = event.Records[0].s3.bucket.name;  
    //var key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    var key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' ').replace(/^.*\//g,''));
    
    var typeMatch = key.match(/^.*\.txt$/);

    var dataType = typeMatch[1];
	if (dataType == "txt" ) {
		console.log('found data' + key);
		return;
	}
	
    console.log("Received event:", eventText);
    var sns = new AWS.SNS();
    var params = {
        Message: eventText, 
        Subject: "New Client Alert",
        TopicArn: "arn:aws:sns:us-east-1:046845663771:NewClientIAM"
    };
    //context.succeed(); this statement blocks SNS DO NOT USE ANYWHERE 
    sns.publish(params, context.done);
};