######################################################################
#####                           ReadMe                           #####
######################################################################
ReadMe for creation of a script in python to interact with AWS SDK.
Objective is to create and/or control ec2 an instance.

Boto3 documentation website for instructions on getting started:
https://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

Boto3 documentation website for ec2 API explanations:
https://boto3.readthedocs.io/en/latest/reference/services/ec2.html

Credit to both of the above.



######################################################################
#####                        Pre-requisites                      #####
######################################################################
Before being able to run this script, or create another, your machine
must have the following installed:

 > python   -   apt-get install python
 > pip      -   apt-get install python-pip
 > boto3    -   pip install boto3

To use boto3, you must set up authentication credentials as follows:

  > Create file ~/.aws/credentials and enter the following:

[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

  > (Optional) Create file ~/.aws/config and enter the following:

[default]
region=us-east-1



######################################################################
#####                         Using Boto3                        #####
######################################################################

To use Boto 3, you need to import it:

  > import boto3

Then tell it what service you are using:

  > ec2 = boto3.resource('ec2')



######################################################################
#####                         Using argv                         #####
######################################################################

I have used argv as the input method for accepting arguments.
When invoking, you can pass an argument and argv stores it in a list.

To use argv you neet to import it:

  > from sys import argv

Then I error check to confirm an argument has been passed in:

  > if len(argv)==1:
    > error message and exit()

If pass, store into argv:

  > script, arg = argv



######################################################################
#####                     Running the script                     #####
######################################################################

To invoke the script:

  > python awsAssign.py <arg>

Accepted arguments:

  > start
  > stop
  > status
  > terminate

What you get back from invocations:

  > start >>> Starts instance with given instanceID.
                  > If already running, will inform user.
                  > If no instance with that ID exists, will create one.

  > stop >>> Stops instance with given instanceID.
                  > If instanceID doesn't exist, will inform user.
                  > If already stopped, will inform user.
                  > If already stopping, will inform user.

  > status >>> Returns status of instance with given instanceID
                  > If instanceID doesn't exist, will inform user.

  > terminate >>> Terminates instance with given instanceID.
