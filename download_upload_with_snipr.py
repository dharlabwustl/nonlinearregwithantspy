## I will download and upload files to the SNIPR.
from xnatSession import *
import json, os,glob,sys,time
import pandas as pd
XNAT_HOST_URL=os.environ['XNAT_HOST']  #'http://snipr02.nrg.wustl.edu:8080' #'https://snipr02.nrg.wustl.edu' #'https://snipr.wustl.edu'
XNAT_HOST = XNAT_HOST_URL # os.environ['XNAT_HOST'] #
XNAT_USER = os.environ['XNAT_USER']#
XNAT_PASS =os.environ['XNAT_PASS'] #
# api_token=os.environ['REDCAP_API']
def get_metadata_session(sessionId,outputfile="NONE.csv"):
    url = ("/data/experiments/%s/scans/?format=json" %    (sessionId))
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    xnatSession.close_httpsession()
    metadata_session=response.json()['ResultSet']['Result']
    metadata_session_1=json.dumps(metadata_session)
    df_scan = pd.read_json(metadata_session_1)
    df_scan.to_csv(outputfile,index=False)
    return metadata_session
