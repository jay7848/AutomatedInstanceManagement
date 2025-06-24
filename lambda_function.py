import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    print("Searching for instances with Action=Auto-Stop")
    stop_instances = list(ec2.instances.filter(Filters=[
        {'Name': 'tag:Action', 'Values': ['Auto-Stop']}
    ]))

    if stop_instances:
        for instance in stop_instances:
            print(f"Found instance {instance.id} in state {instance.state['Name']}")
            if instance.state['Name'] == 'running':
                instance.stop()
                print(f"Stopping instance: {instance.id}")
            else:
                print(f"Instance {instance.id} is not running, skipping stop")
    else:
        print("No instances found with Action=Auto-Stop")

    print("Searching for instances with Action=Auto-Start")
    start_instances = list(ec2.instances.filter(Filters=[
        {'Name': 'tag:Action', 'Values': ['Auto-Start']}
    ]))

    if start_instances:
        for instance in start_instances:
            print(f"Found instance {instance.id} in state {instance.state['Name']}")
            if instance.state['Name'] == 'stopped':
                instance.start()
                print(f"Starting instance: {instance.id}")
            else:
                print(f"Instance {instance.id} is not stopped, skipping start")
    else:
        print("No instances found with Action=Auto-Start")

    return {
        'status': 'Success',
        'stopped_instances': [i.id for i in stop_instances],
        'started_instances': [i.id for i in start_instances]
    }