
import getopt
import sys
import commands


def usage():
    print """
    exec OPTS HOSTs
      OPTS:
        -h: show help
        -c CMD: cmd will exec on all host,default 'echo OK'
        -s HOSTs file: host list file
    """
    sys.exit(0)



if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:s:')
    except Exception,ex:
        print "Exception:", ex
        usage()

    cmd = 'echo OK'
    hostfile = None
    for opt,v in opts:
        if opt == '-h':
            usage()
        elif opt == '-c':
            cmd = v
        elif opt == '-s':
            hostfile = v
        else:
            usage()

    hosts = [] 
    if hostfile:
        for l in open(hostfile):
            hosts.extend(l.split())

    for host in args:
        hosts.append( host)

    print hosts    
    for host in hosts:
        rt,output = commands.getstatusoutput( "ssh %s '%s'"%(host,cmd))
        print '------------'
        print host,':',rt
        print '------------'
        print output

     
