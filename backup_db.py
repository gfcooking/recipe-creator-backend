#!/usr/bin/env python3
import os
import shutil
import time
from os.path import splitext

from glob import glob
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description='Tool to do backups of a db file')
    parser.add_argument('db_file')
    parser.add_argument('-n', '--num-backups', help='Number of backups to keep', default=10, type=int)
    args = parser.parse_args()
    name, ext = splitext(args.db_file)
    new_backup = name + '.' + str(int(time.time())) + ext
    print('Created backup {}.'.format(new_backup))
    shutil.copy(args.db_file, new_backup)
    existing_backups = glob(name + '.*' + ext)
    existing_backups.sort()
    for to_delete in existing_backups[:-args.num_backups]:
        os.remove(to_delete)
        print('Deleted old backup {}.'.format(to_delete))


if __name__ == '__main__':
    main()
