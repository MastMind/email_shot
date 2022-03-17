#!/usr/bin/python3
import sys
import json
import argparse
import time
from smtpmail import mailsender



if __name__ == "__main__":
    targets_conf = "targetsconf"

    parser = argparse.ArgumentParser(description='Email shot script')

    parser.add_argument('-n', '--number', type=int, default=1, help='Numbers of sended emails (default 1; 0 means endless sending)')
    parser.add_argument('-c', '--config', type=str, help='Set targets config file (default targetsconf)')
    parser.add_argument('-d', '--delay', type=int, default=0, help='Delay between messages (in seconds)')

    args = parser.parse_args()

    if args.config:
        targets_conf = args.config

    data = None

    try:
        with open(targets_conf) as json_file:
            data = json.load(json_file)

    except Exception as ex:
        print(str(ex))
        sys.exit(-1)

    m = mailsender()

    if args.number != 0:
        for i in range(0, args.number):
            for element in data:
                m.sendmessage(element["fromaddr"], element["email"], element["text"], element["subject"], element["signature"])

            if args.delay > 0:
                time.sleep(args.delay)
    else:
        while True:
            for element in data:
                m.sendmessage(element["fromaddr"], element["email"], element["text"], element["subject"], element["signature"])

            if args.delay > 0:
                time.sleep(args.delay)

    sys.exit(0)
