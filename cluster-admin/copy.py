
import getopt
import sys
import commands
import socket


def usage():
    print """
    copy OPTS HOSTs
      OPTS:
        -h: show help
        -f file: file path
        -d dir: dir path
        -s HOSTs file: host list file
    """
    sys.exit(0)



if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:d:s:')
    except Exception,ex:
        print "Exception:", ex
        usage()

    if (not opts):
        usage()

    scp_opt = None
    src = None
    hostfile = None
    for opt,v in opts:
        if opt == '-h':
            usage()
        elif opt == '-f':
            scp_opt = ''
            src = v
        elif opt == '-d':
            scp_opt = '-r'
            src = v
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
        
    for host in hosts:
        if host in socket.gethostname():
            continue
        rt,output = commands.getstatusoutput( 
                "scp %s '%s' '%s:%s'"%(scp_opt,src,host,src))
        print '------------'
        print host,':',rt
        print '------------'
        print output

     
