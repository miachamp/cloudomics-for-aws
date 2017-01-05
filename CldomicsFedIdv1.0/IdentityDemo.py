import json
import os, binascii
from flask import Flask, render_template, request, url_for, redirect, session

# Flask Initialization
# global variable must be named "application" as per EB requirement
application = Flask(__name__)
application.debug = True

# secret key to encode session cookie (http://flask.pocoo.org/docs/quickstart/#sessions)
application.secret_key = binascii.b2a_hex(os.urandom(30))
#
#
# Read config file and create Identity provider
#
def getIdentityProvider(provider) :
    import os
    from IdentityProvider import getIdentityProvider
    
    appID      = os.environ.get(provider.upper() + '_APP_ID')
    appSecret  = os.environ.get(provider.upper() + '_APP_SECRET')
    roleARN    = os.environ.get(provider.upper() + '_ROLE_ARN')
    
    return getIdentityProvider(provider, appID, appSecret, roleARN)
    
@application.route("/")
def index():
    enabled_providers = getEnabledProviders()
    return render_template('default.html', enabled_providers=enabled_providers)
    
@application.route("/privacy")
def privacy():
    return render_template('privacy.html')

@application.route('/initiateLogin/<provider>')
def initiateLogin(provider):
    print '--- Initiate login for provider : ' + provider
    return redirect(getIdentityProvider(provider).loginURL())

@application.route('/oauth2callback/<provider>')
def OAuth2Callback(provider):
    print '--- OAuth2Callback called for IP : ' + provider  
    
    code  = request.args.get('code', 'unknown') 
    if (code == 'unknown'):
        result = render_template('error.html')
    else:
        credentials, profile = getIdentityProvider(provider).oauthCallback(code)
        
        import urllib
        # _scheme is required for SSL, see
        # https://github.com/mitsuhiko/flask/issues/773
        #url = url_for('s3', _scheme="https", _external=True, **dict(credentials.items() + profile.items()))
        url = url_for('s3', _scheme="https", _external=True)
        #print '--- redirect url : ' + url

        # save credentials and profile in the server side session
        session.update(credentials)
        session.update(profile)
        #print '--- session : ' + str(session)

        result = redirect(url)
            
    return result
    
@application.route('/s3/')
def s3():
    # all args are provided in the session

    # workaround URL encoding issue where + signs are replaced by ' '
    # it looks like it is a bug introduced with Flask 0.10.1 (0.9 is OK)
    # https://github.com/mitsuhiko/flask/issues/771
    import boto
    from boto import s3
    from boto import sts
    import json 
    from json import dumps
    
    from boto.sts.connection import STSConnection
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key 
    #from boto.s3.bucket import Bucket
    from boto.s3.connection import Location
   
    session['session_token'] = session['session_token'].replace(' ', '+')
    session['access_key'] = session['access_key'].replace(' ', '+')
    session['secret_key'] = session['secret_key'].replace(' ', '+')
    
    # call S3 to list buckets
    client_bucket = doListCreateBuckets(session) 
    conn = Usercreds(session)
    
    new_config = str(client_bucket).replace('[','').replace(']','').replace('\'','')+'.txt' 
    resource1 = 'arn:aws:s3:::'+client_bucket
    resource = 'arn:aws:s3:::'+client_bucket+'/*'
    #userprincipal = 'arn:aws:iam::*:user/'+client_bucket
    #rootprincipal = 'arn:aws:iam::*:root'
    
    AWS_ACCESS_KEY_ID=appID #Need to define users KEY ID 
    AWS_SECRET_ACCESS_KEY=appSecret #Need to define users access Key
    
    iam = boto.connect_iam(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
    user_response = iam.create_user(client_bucket)
    
    policy_to_grant = {'Statement': [{'Sid': client_bucket,
                                    'Action': ['s3:*'],
                                    'Effect': 'Allow',
                                    'Resource': resource}]}
    
    policy_to_json=dumps(policy_to_grant)
    newbucket = conn.create_bucket(client_bucket, location=Location.DEFAULT)
   
    iam.put_user_policy(client_bucket, 'allow_access_s3', policy_to_json)

    key_response = iam.create_access_key(client_bucket)
    credkey = key_response.create_access_key_response.create_access_key_result.access_key
    
    mybucket=conn.get_bucket(client_bucket)
    mydata = Key(mybucket)
    mydata.key = (new_config)
    #mystring = ("client temporary S3 bucket : "+str(client_bucket)+"\n"+"aws_access_key_id : "+aws_access_key_id+"\n"+"aws_secret_access_key : "+aws_secret_access_key+"\n")
    mystring = ("client temporary S3 bucket : "+str(client_bucket)+"\n"+"aws_access_key_id :"+str(credkey.access_key_id)+"\n"+"aws_secret_access_key : "+str(credkey.secret_access_key)+"\n")
    mydata.set_contents_from_string(mystring)
    
    return render_template('s3.html', client_bucket=client_bucket, args=session, aws_access_key_id=credkey.access_key_id, aws_secret_access_key=credkey.secret_access_key)
    
def getEnabledProviders():
  providers = ['amazon', 'facebook', 'google']
  enabled = []
  
  for provider in providers:
    if os.environ.get(provider.upper() + '_APP_ID') and os.environ.get(provider.upper() + '_APP_SECRET') and os.environ.get(provider.upper() + '_ROLE_ARN'):
      enabled.append(provider)
  
  return enabled
    
def doListCreateBuckets(credentials):
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key 
    #from boto.s3.bucket import Bucket
    from boto.s3.connection import Location
 
    conn = S3Connection(credentials['access_key'], credentials['secret_key'], security_token=credentials['session_token'])

    client_bucket= binascii.b2a_hex(os.urandom(5))
    new_line = 'cloud'+str(client_bucket).replace('[','').replace(']','').replace('\'','')
    
    return new_line

def Usercreds(credentials):
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key 
    #from boto.s3.bucket import Bucket
    from boto.s3.connection import Location
 
    conn = S3Connection(credentials['access_key'], credentials['secret_key'], security_token=credentials['session_token'])
            
    return conn
    
if (__name__ == "__main__"):
    application.run(debug=True)