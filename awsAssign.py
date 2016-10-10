# Program for use with AWS ec2 instances. Capabilities: Start, Stop, Create, Terminate, and fetch Status of an instance

# Use argv for input of arguments while executing script for method calling
from sys import argv
# First index in agv is the script name, if there is nothing else
# it means no argument was provided when the scipt was invoked
if len(argv)==1:
	print("You failed to provide an argument. \nPlease provide either start, stop, status, or terminate as an argument.")
	exit()
script, arg = argv

# Boto3 is the AWS SDK for python
import boto3
# Tell boto3 what resource we are using and assign to variable
ec2 = boto3.resource('ec2')

# This method has filters defined in it, that are returned in response: Instance state (all except terminated), Tag value (Instance tag "Williamson"), and Image-id, as instructed
def findInstance():
	client = boto3.client('ec2')					# Define a client, store into client variable
													# Variable response is assigned what describe_instances returns, the instance is determined by matching with the filters passed in
	response = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']}, {'Name': 'tag-value', 'Values': ['Williamson']}, {'Name': 'image-id', 'Values': ['ami-31490d51']}])

	return response

# Method to return the id of an instance when given the response from findInstance
def getInstanceID(response):
	if len(response["Reservations"]) == 0:			# If the Reservations field of response holds nothing
		return False								# Break out of method
	else:
		instanceID = response["Reservations"][0]["Instances"][0]["InstanceId"]
		return instanceID 							# Otherwise grab the id

# Method to return the status of an instance when given the instance id
def getInstanceStatus(instanceID):
	if instanceID != False:							# If the instance id is not false
		instance = ec2.Instance(instanceID)			# Assign an ec2 instance to variable instance, based on the instance id

		return instance.state 						# Return the state from that instance
	else:
		return False 								# Else break out of method

# Method to display the state of an instance, same as method above, only it displays to user instead of storing
def showInstanceStatus(instanceID):
	instance = ec2.Instance(instanceID)
	print("Instance " + instanceID + " is in status: " + instance.state["Name"])

# Method to create an instance if one does not already exist when start is called
def createInstance():
	instance = ec2.create_instances(ImageId='ami-31490d51', InstanceType='t2.nano', MinCount=1, MaxCount=1) # Define the id, type, and count of instance
	instanceID = instance[0].id
	ec2.create_tags(Resources=[instanceID], Tags=[{'Key': 'Name', 'Value': 'Williamson'}]) # Define resources and tags
	print("Created instance: " + instanceID)		# Display success to user

# Method to create an instance when given an instance id and state
def startInstance(instanceID, instanceState):
	if instanceState == 16:							# Already runnning, break out
		print("Instance is already running")
		return
	elif instanceState == 0:						# Already pending start, break out
		print("Instance is alreay pending start")
		return

	instance = ec2.Instance(instanceID) 			# Assign an ec2 instance to variable instance, based on the instance id
	instance.start() 								# Start that instance
	print("Starting Instance: " + instanceID) 		# Display to user

# Method to stop an instance when given an instance id and state
def stopInstance(instanceID, instanceState):
	if instanceState == 80:							# Already stopped, break out
		print("Instance already stopped")
		return
	elif instanceState == 64:						# Already in process of stopping, break out
		print("Instance alreay stopping")
		return

	instance = ec2.Instance(instanceID) 			# Assign an ec2 instance to variable instance, based on the instance id
	instance.stop() 								# Stop the instance
	print("Stopping Instance: " + instanceID) 		# Display to user

# Method to terminate an instance when given an instance id
def terminateInstance(instanceID):
	instance = ec2.Instance(instanceID)				# Assign an ec2 instance to variable instance, based on the instance id
	instance.terminate() 							# Terminate the instance
	print("Terminating Instance: " + instanceID)	# Display to user


# Ask for an instance using pre-defined values, store as response
response = findInstance()
# Get the ID of that instance
instanceID = getInstanceID(response)
# Get the state of that instance
instanceState = getInstanceStatus(instanceID)

# If argument given is the string "start"
if arg == "start":
	if instanceID == False:							# If the getInstanceID method returned false
		createInstance()							# No instance exists, so create it
	else:
		startInstance(instanceID, instanceState)	# Otherwise start the instance using the id and state gathered above

# If argument given is the string "stop"
elif arg == "stop":
	if instanceID == False:							# If the getInstanceID method returned false
		print("No instance available to stop, please run start")
	stopInstance(instanceID, instanceState)			# Otherwise stop the instance using the id and state gathered above


elif arg == "status":
	if instanceID == False:							# If the getInstanceID method returned false
		print("No instance available to retreive status, please run start")
	showInstanceStatus(instanceID)					# Otherwise show the status of the instance using the id and state gathered above


elif arg == "terminate":							# No false check needed as findInstance does not return Ids with status terminated
	terminateInstance(instanceID)					# Terminate the instance using the id gathered above

else:												# Argument passed in with invocation not valid
	print("Argument provided not valid. \nPlease provide either start, stop, status, or terminate as an argument.")
