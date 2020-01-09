# This file is part of flashgun.
# flashgun - a RESTful API for flashnet XML API
from flask import Flask, jsonify, request, abort, make_response, Response
import os, configparser, subprocess, json, datetime, logging
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

app = Flask(__name__)

@app.route('/')
def index():
    return 'flashgun!'


if __name__ == '__main__':
    app.run()

# read flashnet server configuration from config file
config = configparser.ConfigParser()
config.read('./flashgun.conf')
appname = config.get("GENERAL", "appname")
fg_host = config.get("GENERAL", "apphostname")
fn_server_ip = config.get("FNSERVER", "ip")
fn_server_port = config.get("FNSERVER", "port")
fn_host = config.get("FNSERVER", "host")
fn_username = config.get("FNSERVER", "username")
fn_xml_api_ver = config.get("FNSERVER", "xml_api_version")
logging.basicConfig(filename='./logs/flashgun.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# establish tcp connection socket using netcat
nccmd = "nc -v " + fn_server_ip + ' ' + fn_server_port

# get config api
@app.route('/api/v1/config', methods=['GET'])

def getconfig():
    return jsonify(fn_server_ip, fn_server_port, fn_host, fn_username, fn_xml_api_ver, fg_host)

# get flashnet server status api
@app.route('/api/v1/status', methods=['GET'])
def getstatus():

    import xml.etree.ElementTree as etree
    root=Element('FlashNetXML')
    tree=ElementTree(root)
    root.set('APIVersion',fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'Status')
    with open('./xml/status-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "Status.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True,stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())
    #return Response(fn_xml, mimetype='text/xml')

# get flashnet server status api
@app.route('/api/v1/listServer', methods=['GET'])
def ListServer():
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root=Element('FlashNetXML')
    tree=ElementTree(root)
    root.set('APIVersion',fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListServer')
    with open('./xml/ListServer-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListServer.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True,stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())