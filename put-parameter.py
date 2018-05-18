
import boto3
import botocore
import os , errno
#global variables



#value retrieved from environment variable
region_var = os.environ['REGION']

session = boto3.Session(region_name=region_var, profile_name='default')
iam = session.client('iam')
kms = session.client('kms')
ssm = session.client('ssm')
s3  = boto3.resource('s3')

policy_name_var='nops-test-policy-uat-2'
alias_var = 'alias/nops-test-kms-uat-2'

response = kms.create_key(
    Description='nops Test Key 1',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS',
    BypassPolicyLockoutSafetyCheck=False,
    Tags=[{'TagKey': 'Name', 'TagValue': 'TestKey'}]
)

keyid_var = response['KeyMetadata']['KeyId']
print(keyid_var)

#code to create IAM policy

response = iam.create_policy(
    PolicyName=policy_name_var,
    PolicyDocument='''{
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "Stmt1517212478111",
            "Action": [
                "kms:Decrypt",
                "kms:Encrypt"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:kms:us-east-2:0123456799012:key/%s"
        }]
    }'''%(keyid_var),
    Description='nops KMS Test Policy'
)

print(response['Policy']['Arn'])

#asssigning alias to policy

response = kms.create_alias(AliasName=alias_var, TargetKeyId=keyid_var)

#create list of directories
directory = ['/tmp/secret/uat','/tmp/secret/prod']


#create directories in /tmp/secrets location
for i in directory:
    try:
        os.makedirs(i)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


#download files from S3 bucket
conn = client('s3')
var_bucketName = 'nclouds-nops-secrets'
data = conn.list_objects(Bucket=var_bucketName)['Contents']
uat = []
prod = []


for key in data :
    if "uat" in str(key) and "gpg" in str(key):
        var_key_uat =str(key['Key'])
    #    uat.append(var_key_uat)
        try:
            data_uat = var_key_uat.split("/")
            key_value = "/tmp/secrets/uat/"+str(data_uat[1])
            s3.Bucket(var_bucketName).download_file(var_key_uat, key_value )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    elif "prod" in str(key) and "gpg" in str(key):
        var_key_prod =str(key['Key'])
        #prod.append(var_key_prod)
        try:
            data_prod = var_key_prod.split("/")
            key_value = "/tmp/secrets/prod/"+str(data_prod[1])
            s3.Bucket(var_bucketName).download_file(var_key_prod ,key_value)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    else:

        print ""


'''
files_uat_path="/tmp/secrets/uat/"
files_prod_path= "/tmp/secrets/prod/"

# using os library we get file names returned as list
files_uat = os.listdir(files_uat_path)
files_prod = os.listdir(files_prod_path)

print("printing uat files ")
#read data from file downloaded from s3 for encryption
for x in files_uat:
    with open(files_uat_path+x, 'r') as content_file:
        content = content_file.read()

        response = ssm.put_parameter(
            Name=x,
            Description='initial value',
            Value=content,
            Type='SecureString',
            KeyId=keyid_var,
            Overwrite=True
            )

for x in files_prod:
    with open(files_prod_path+x, 'r') as content_file:
        content = content_file.read()

        response = ssm.put_parameter(
            Name=x,
            Description='initial value',
            Value=content,
            Type='SecureString',
            KeyId=keyid_var,
            Overwrite=True
            )

# using glob we get the absoludte path returned as list
'''
files_uat_2 = glob.glob("/tmp/secrets/uat/*.gpg")
files_prod_2 = glob.glob("/tmp/secrets/prod/*.gpg")


for x in files_uat_2:
    with open(x, 'r') as content_file:
        content = content_file.read()
        #print content
        response = ssm.put_parameter(
            Name=x,
            Description='initial value',
            Value=content,
            Type='SecureString',
            KeyId=keyid_var,
            Overwrite=True
            )


for x in files_prod_2:
    with open(x, 'r') as content_file:
        content = content_file.read()
        #print content
        response = ssm.put_parameter(
            Name=x,
            Description='initial value',
            Value=content,
            Type='SecureString',
            KeyId=keyid_var,
            Overwrite=True
            )

#variables containing secret value and tag for keys used in pushing the key to paramter store


#create kms key



#pushing key to paramter store in secured string format


#describing paramters

#response = ssm.describe_parameters(
#    Filters=[{'Key': 'Name', 'Values': [name_var]}]
##)
#print(response['ResponseMetadata']['Parameters'][0]['Name'])
