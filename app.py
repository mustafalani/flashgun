# This file is part of flashgun.
# flashgun - a RESTful API for flashnet XML API
from flask import Flask, jsonify, request, abort, make_response, Response, render_template, redirect, url_for, request
from flask_cors import CORS, cross_origin
import os, configparser, subprocess, json, datetime, logging
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('/api/v1/config'))
    return render_template('login.html', error=error)


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

# establish tcp connection socket using netcat
nccmd = "nc -v " + fn_server_ip + ' ' + fn_server_port


# read config
@app.route('/api/v1/config', methods=['GET'])
def getconfig():
    return jsonify(fn_server_ip, fn_server_port, fn_host, fn_username, fn_xml_api_ver, fg_host)


# Archive api


# Restore api
@app.route('/api/v1/Restore', methods=['GET'])
def getrestore():
    if not request.json or not 'requestId' in request.json:
        abort(400)
    requestId = request.json['requestId']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    status_attributes = {"Restore.DWD": requestId}
    status_subelement = etree.SubElement(root, "status", attrib=status_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'Restore')
    with open('./xml/Restore-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "Restore.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())

# Delete api


# ListGuid api
@app.route('/api/v1/ListGuid', methods=['GET'])
def getListGuid():
    if not request.json or not 'guid' in request.json:
        abort(400)
    guid = request.json['guid']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    guid_attributes = {"Guid": guid}
    guid_subelement = etree.SubElement(root, "ListGuid", attrib=guid_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListGuid')
    with open('./xml/ListGuid-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListGuid.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# ReadLog api
@app.route('/api/v1/ReadLog', methods=['GET'])
def getReadLog():
    if not request.json or not 'LogFileKey' in request.json:
        abort(400)
    requestId = request.json['LogFileKey']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    readloag_attributes = {"LogFileKey.DWD": requestId}
    readlog_subelement = etree.SubElement(root, "ReadLog", attrib=readloag_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ReadLog')
    with open('./xml/ReadLog-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ReadLog.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())

# ListGroup api
@app.route('/api/v1/ListGroup', methods=['GET'])
def getListGroup():
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    tree = ElementTree(root)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListGroup')
    with open('./xml/ListGroup-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListGroup.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# status api
@app.route('/api/v1/Status', methods=['GET'])
def getstatus():
    if not request.json or not 'requestId' in request.json:
        abort(400)
    requestId = request.json['requestId']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    status_attributes = {"RequestId.DWD": requestId}
    status_subelement = etree.SubElement(root, "status", attrib=status_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'Status')
    with open('./xml/Status-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "Status.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# ListServer api
@app.route('/api/v1/ListServer', methods=['GET'])
@cross_origin()
def getListServer():
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    tree = ElementTree(root)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListServer')
    with open('./xml/ListServer-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListServer.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# ListWatchFolder api
@app.route('/api/v1/ListWatchFolder', methods=['GET'])
def getListWatchFolder():
    if not request.json or not 'list_watch_pattern' in request.json:
        list_watch_pattern = '*'
    if request.json and 'list_watch_pattern' in request.json:
        list_watch_pattern = request.json['list_watch_pattern']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    tree = ElementTree(root)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListWatchFolder')
    root.set('Pattern', list_watch_pattern)
    with open('./xml/ListWatchFolder-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListWatchFolder.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# ListRestoreFolder api
@app.route('/api/v1/ListRestoreFolder', methods=['GET'])
def getListRestoreFolder():
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    tree = ElementTree(root)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ListRestoreFolder')
    with open('./xml/ListRestoreFolder-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ListRestoreFolder.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# StopJob api
@app.route('/api/v1/StopJob', methods=['GET'])
def getStopJob():
    if not request.json or not 'jobId' in request.json:
        abort(400)
    jobId = request.json['jobId']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    stop_attributes = {"Job.DWD": jobId}
    job_subelement = etree.SubElement(root, "Stop", attrib=stop_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'StopJob')
    with open('./xml/StopJob-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "StopJob.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# PauseJob api
@app.route('/api/v1/PauseJob', methods=['GET'])
def getPauseJob():
    if not request.json or not 'jobId' in request.json:
        abort(400)
    jobId = request.json['jobId']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    pause_attributes = {"Job.DWD": jobId}
    job_subelement = etree.SubElement(root, "Pause", attrib=pause_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'PauseJob')
    with open('./xml/PauseJob-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "PauseJob.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# ResumeJob api
@app.route('/api/v1/ResumeJob', methods=['GET'])
def getResumeJob():
    if not request.json or not 'jobId' in request.json:
        abort(400)
    jobId = request.json['jobId']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    resume_attributes = {"Job.DWD": jobId}
    job_subelement = etree.SubElement(root, "Resume", attrib=resume_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'ResumeJob')
    with open('./xml/ResumeJob-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "ResumeJob.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())


# SearchArchive api
@app.route('/api/v1/SearchArchive', methods=['GET'])
def getSearchArchive():
    if not request.json or 'Guid' and 'Group' and 'Volume' not in request.json:
        abort(400)
    guid = request.json['Guid']
    group = request.json['Group']
    volume = request.json['Volume']
    archivedfromfate = request.json['ArchivedFromDate']
    archivedtodate = request.json['ArchivedToDate']
    deletedfromdate = request.json['DeletedFromDate']
    deletedtodate = request.json['DeletedToDate']
    pagesize = request.json['PageSize']
    fromqmd = request.json['FromQWD']
    flagsdwd = request.json['FlagsDWD']
    includemetadata = request.json['IncludeMetadataDWD']
    _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    import xml.etree.ElementTree as etree
    root = Element('FlashNetXML')
    stop_attributes = {"Guid": guid, "Group": group, "Volume": volume, "ArchivedFromDate": archivedfromfate, "ArchivedToDate": archivedtodate, "DeletedFromDate": deletedfromdate, "DeletedToDate": deletedtodate, "PageSize.DWD": pagesize, "From.QWD": fromqmd, "Flags.DWD": flagsdwd, "IncludeMetadata.DWD": includemetadata}
    job_subelement = etree.SubElement(root, "SearchArchive", attrib=stop_attributes)
    root.set('APIVersion', fn_xml_api_ver)
    root.set('SourceServer', fg_host)
    root.set('UserName', fn_username)
    root.set('CallingApplication', fn_username)
    root.set('Operation', 'SearchArchive')
    with open('./xml/SearchArchive-' + _now + '.xml', "w", encoding='UTF-8') as fn_xml_out:
        doc_type = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE FlashNetXML SYSTEM "SearchArchive.dtd">'
        _tostring = etree.tostring(root).decode('utf-8')
        fn_xml = (f"'{doc_type}{_tostring}'").replace('\'', '')
        fn_xml_out.write(fn_xml)
    fg_api_cmd = subprocess.Popen("echo \'" + fn_xml + "\' | " + nccmd, shell=True, stdout=subprocess.PIPE)
    return_code = fg_api_cmd.wait()
    if return_code == 0:
        logging.info('done')
    else:
        print('bad')
    return (fg_api_cmd.communicate())