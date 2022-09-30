import datetime as dt

def log_request(request, filename = "logfile.txt"):
    with open(filename, "a") as f:
        remote_ip = request.access_route[0] if request.access_route != None and len(request.access_route) != 0 \
            else request.remote_addr
        f.write('[%s] {%s} {%s}\n' % (dt.datetime.now(), remote_ip, request.full_path))