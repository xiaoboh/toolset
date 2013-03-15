# create a lot of connection to http server
import httplib
import sys

def new_http_conn( ip , url ):
    try:
        conn = httplib.HTTPConnection(ip)
        headers = {'Connection':'Keep-Alive'}
        conn.request("GET", url, "", headers)
        return conn 
    except Exception, ex:
        print ex

    return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "http_client_concurrency.py <ip> <url>"
        sys.exit(0)

    conns = []
    while True:
        conn = new_http_conn( sys.argv[1], sys.argv[2] )
        if not conn:
            while True:
                ui = raw_input("Create Connection Failed, is continue create[y/n/e]:")
                if ui is 'y':
                    break 
                if ui is 'e':
                    sys.exit(0)
                continue

        conns.append(conn)
        print "Cur Connection Count:", len(conns)





