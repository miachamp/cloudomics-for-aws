// dependencies

var AWS = require('aws-sdk');
var util = require('util');

// get reference to S3 client 
var s3 = new AWS.S3();

console.log("Loading function");
 
var AWS = require('aws-sdk');
//var s3 = new aws.S3({ apiVersion: '2012-10-29' });
 
exports.handler = function(event, context) {
    //Copy client config to omicslanderconfigs
    var eventText = JSON.stringify(event, null, 2);
    var clientID = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' ').replace(/\/.*$/g,'').replace(/\.zip/g,''));
    var bucket = event.Records[0].s3.bucket.name+'/'+clientID;  
    var putbucket = "omicslanderconfigs";
    //var key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    var key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' ').replace(/^.*\//g,''));
    var putkey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' ').replace(/^.*\//g,'').replace(/\.zip/g,'.txt'));
    
    console.log("EVENT VARS:", clientID, bucket, key, putbucket, putkey );
    //console.log("Received event:", eventText);

    var GETparams = {
        Bucket: bucket,
        Key: key
    };    
    
    var PUTparams = {
        Bucket: putbucket,
        Key: putkey
    };    

    s3.getObject(GETparams, function(err, data) {
        if (err) {
            console.log(err);
            var message = "Error getting object " + key + " from bucket " + bucket +
                ". Make sure they exist and your bucket is in the same region as this function.";
            console.log(message);
            context.fail(message);
        } else {
            console.log('CONTENT TYPE:', data.ContentType);
            context.succeed(data.ContentType);
        }
    });
    
    s3.putObject(PUTparams, function(err, data) {
        if (err) {
            console.log(err);
            var message = "copy failed";
            console.log(message);
            context.fail(message);
        } else {
            console.log('CONTENT TYPE:', data.ContentType);
            context.succeed(data.ContentType);
        }
    });
};