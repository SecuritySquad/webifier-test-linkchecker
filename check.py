#!/usr/bin/python

import json
import requests
import subprocess

import sys


def get_links(url):
    command = "phantomjs /tmp/check.js " + url
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = proc.stdout.read().split("\n")
    return filter(None, result)


def get_link_results(links):
    content = {
        "urls": links
    }
    headers = {"Content-type": "application/json;charset=UTF-8", "Accept": "application/json;charset=UTF-8"}
    response = requests.post("https://data.webifier.de/check", json=content, headers=headers)
    data = response.content
    return json.loads(data)


def format_result(response):
    checked_hosts = response.get("hosts", {})
    hosts = []
    malicious = 0
    suspicious = 0
    undefined = 0

    for host in checked_hosts:
        host_result = response.get(host, "UNDEFINED")
        if host_result == "MALICIOUS":
            malicious += 1
        elif host_result == "SUSPICIOUS":
            suspicious += 1
        elif host_result == "UNDEFINED":
            undefined += 1
        hosts.append({
            "host": host,
            "result": host_result
        })

    result = "CLEAN"
    if malicious > 0:
        result = "MALICIOUS"
    elif undefined / len(checked_hosts) >= 0.33:
        result = "UNDEFINED"
    elif suspicious > 0:
        result = "SUSPICIOUS"

    return {
        "result": result,
        "info": {
            "hosts": hosts
        }
    }


if __name__ == "__main__":
    if len(sys.argv) == 3:
        prefix = sys.argv[1]
        url = sys.argv[2]
        links = get_links(url)
        print links
        result = get_link_results(links)
        print result
        if result.get("success", False):
            print '{}: {}'.format(prefix, json.dumps(format_result(result)))
        else:
            print "no response received!"
    else:
        print "prefix, url or content missing"
