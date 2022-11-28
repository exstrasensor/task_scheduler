import argparse
from logic import JobScheduler
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--User", help="Username", required=True)
parser.add_argument("-a", "--Action",
                    help="Actions: create, completed, scheduled",
                    required=True,
                    choices=["create", "completed", "scheduled"])

create_task = parser.add_argument_group('Create task arguments')
create_task.add_argument("-c", "--Command", help="Command for execution")
create_task.add_argument("-s", "--Schedule", help="Time for execution")


completed_task = parser.add_argument_group('List completed tasks arguments')
completed_task.add_argument("-l", "--Limit", help="Limit tasks")

args = parser.parse_args()


if args.Action == "create":
    if args.Command is None or args.Schedule is None:
        print("Must specify cmd command and time to execute")
        sys.exit()

    scheduler = JobScheduler(user=args.User,
                             console_command=args.Command,
                             start_at=args.Schedule)

    scheduler.create_job()

if args.Action == "completed":
    if args.Limit is None:
        print("Must specify limit")
        sys.exit()

    scheduler = JobScheduler(user=args.User)
    for item in scheduler.check_completed_jobs(args.Limit):
        print(item)

if args.Action == "scheduled":
    if args.Limit is None:
        print("Must specify limit")
        sys.exit()

    scheduler = JobScheduler(user=args.User)

    for item in scheduler.check_scheduled_jobs(args.Limit):
        print(item)
