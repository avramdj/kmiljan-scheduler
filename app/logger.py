import datetime as dt

def log_request(request, filename = "logfile.txt"):
    with open(filename, "a") as f:
        f.write('[%s] {%s} {%s}\n' % (dt.datetime.now(), request.remote_addr, request.full_path))