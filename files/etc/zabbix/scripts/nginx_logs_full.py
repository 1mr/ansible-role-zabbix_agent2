#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import json
import subprocess as s

path = '/var/log/nginx'
sender = '/usr/bin/zabbix_sender'
logtail = '/usr/sbin/logtail2 -f'
cfg = '/etc/zabbix/zabbix_agent2.conf'
tmp = '/var/tmp'
tmpd = '%s/nginx_logs.dat' % tmp
sufl = ['2xx-access.log', '3xx-access.log', '4xx-access.log', '5xx-access.log']
sufd = 'offset.dat'
list_vhosts = []
list = []


def vhosts():
    for d, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(sufl[0]):
                list_vhosts.append(file[:-15])
    return list_vhosts


def main():
    # list all nginx vhosts
    if len(sys.argv) < 2:
        print("Run as:\n{0} [list_vhosts|status]".format(sys.argv[0]))

    elif sys.argv[1] == 'list_vhosts':
        for vhost in vhosts():
            element = {'{#VHOSTNAME}': vhost}
            list.append(element)
        print(json.dumps({'data': list}, indent=4))

    elif sys.argv[1] == 'status':
        # send all vhosts info as traps
        out = ''
        for vhost in vhosts():
            for suf in sufl:
                cmd = '%s %s/%s-%s -o %s/%s-%s-%s' % (logtail, path, vhost, suf, tmp, vhost, suf[:-11], sufd)  # noqa: E501
                wc = s.Popen('wc -l'.split(), stdin=s.PIPE, stdout=s.PIPE)
                log = s.Popen(cmd.split(), stdout=wc.stdin)
                output = wc.communicate()[0]
                log.wait()
                out += "- nginx[%s,%s] %s" % (vhost, suf[:-11], output)

        # write data for zabbix sender
        try:
            with open(tmpd, 'w') as f:
                f.write(out)
        except Exception:
            print("Unable to save data to send!")
            sys.exit(1)

        # send data with debug
        if len(sys.argv) > 2 and sys.argv[2] == 'debug':
            print(out)
            os.system("{0} -c {1} -i {2} -vv".format(sender, cfg, tmpd))
        else:
            os.system("{0} -c {1} -i {2} 2>&1 >/dev/null".format(sender, cfg, tmpd))    # noqa: E501


if __name__ == '__main__':
    main()
