import boto3
import argparse
import sys

def start_instances(instance_ids):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.start_instances(InstanceIds=instance_ids)
        print(f'Started instances {instance_ids}: {response}')
    except Exception as e:
        print(f'Error starting instances {instance_ids}: {str(e)}')

def stop_instances(instance_ids):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.stop_instances(InstanceIds=instance_ids)
        print(f'Stopped instances {instance_ids}: {response}')
    except Exception as e:
        print(f'Error stopping instances {instance_ids}: {str(e)}')

def read_instance_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            instance_ids = [line.strip() for line in file if line.strip()]
        return instance_ids
    except Exception as e:
        print(f'Error reading instance IDs from file: {str(e)}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Start or stop AWS EC2 instances.')
    parser.add_argument('--start', action='store_true', help='Start the EC2 instances')
    parser.add_argument('--stop', action='store_true', help='Stop the EC2 instances')
    parser.add_argument('--instance-id', type=str, nargs='+', help='EC2 Instance ID(s)')
    parser.add_argument('--file', type=str, help='File containing the EC2 Instance ID(s)')

    args = parser.parse_args()

    if not args.start and not args.stop:
        print('Error: You must specify either --start or --stop')
        parser.print_help()
        sys.exit(1)

    instance_ids = []
    if args.instance_id:
        instance_ids.extend(args.instance_id)
    elif args.file:
        instance_ids.extend(read_instance_ids_from_file(args.file))
    else:
        print('Error: You must specify either --instance-id or --file')
        parser.print_help()
        sys.exit(1)

    if args.start:
        start_instances(instance_ids)
    elif args.stop:
        stop_instances(instance_ids)

if __name__ == '__main__':
    main()
