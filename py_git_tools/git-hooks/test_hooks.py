#!/usr/bin/env python


import sys
import os
import commands


if __name__ == '__main__':
    print 'hi, git client, i am server. by hxb.'

    logf = open('/tmp/git-hook-log.hxb', 'a')
    logf.write('\n------------------------\n')

    pid = os.getpid()
    ppid = os.getppid()
    logf.write( str(pid) + ' -> ' + str(ppid) + '\n')

    output = commands.getoutput('ps -aux').split('\n')
    for line in output:
        if str(ppid) in line.split():
            logf.write(line + '\n')
        elif str(pid) in line.split():
            logf.write(line + '\n')

    logf.write( 'cur dir:' + os.getcwd() + '\n')
    logf.write( '\n' )
    logf.write( str(sys.argv) )
