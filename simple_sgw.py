import socket
import struct
import sys
from ie_master_enc import *

def csreq():
    # SGW IP address
    host = "127.0.0.1"
    # CSReq parameters
    imsi = 302600000001234
    msisdn = 12345678901
    imei = 1234567890123456
    serv_mcc = 302
    serv_mnc = 600
    uli_mcc = 302
    uli_mnc = 600
    uli_tai = 48000
    uli_ecgi_enodebid = 500001
    uli_ecgi_cellid = 11
    mme_s11_teid = "807b4021"
    mme_s11_addr = "20.30.40.50"
    pgw_ip_add = "10.20.30.40"
    #apn = "imstemp"
    apn = "internet.com"
    ambr_ul = 500
    ambr_dl = 500
    mbr_ul = 0
    mbr_dl = 0
    gbr_ul = 0
    gbr_dl = 0
    qci = 8
    # CSReq :
    # x2 Flags
    # x2 Type
    # x4 Lenght
    # x8 TEID
    # x6 Sequence Number
    # x2 Spare
    hflags_ver = "010"
    hflags_pig = "0"
    hflags_teid = "1000"
    hmsg_type = "20"
    hmsg_len = 0
    hteid = "80d3c023"
    hseq_num = "25fa21"
    hspare = "00"
    #
    imsi_ie     = ie_numid_encode(imsi, 1)
    msisdn_ie   = ie_numid_encode(msisdn, 76)
    imei_ie     = ie_numid_encode(imei, 75)
    uli_ie      = ie_86_encode(uli_mcc, uli_mnc, uli_tai, uli_ecgi_enodebid, uli_ecgi_cellid)
    ser_net_ie  = ie_83_encode(serv_mcc, serv_mnc)
    rat_ie      = ie_82_encode(6)
    fteid_mme_ie    = ie_87_encode(4, 10, mme_s11_teid, mme_s11_addr)
    fteid_pgw_ie    = ie_87_encode(4, 7, "00000000", pgw_ip_add)
    apn_ie      = ie_71_encode(apn, serv_mcc, serv_mnc)
    sel_mode_ie = ie_128_encode()
    sel_mode_ie = ie_99_encode()
    paa_ie      = ie_79_encode()
    ind_ie      = ie_77_encode()
    apn_res_ie  = ie_127_encode()
    ambr_ie     = ie_72_encode(ambr_ul, ambr_dl)
    pco_ie      = ie_78_encode()
    bearer_ctx_ie   = ie_93_encode(pgw_ip_add, mbr_ul, mbr_dl, gbr_ul, gbr_dl, qci)
    ue_tz_ie    = ie_114_encode()
    payload = imsi_ie + msisdn_ie + imei_ie + uli_ie + ser_net_ie + rat_ie +\
            fteid_mme_ie + fteid_pgw_ie + apn_ie + sel_mode_ie + sel_mode_ie +\
            paa_ie + ind_ie + apn_res_ie + ambr_ie + pco_ie + bearer_ctx_ie +\
            ue_tz_ie
    hmsg_len = hex(int(len(payload)/2+8))[2:].zfill(4)
    hflags = str(int((hflags_ver + hflags_pig), 2)) + str(int(hflags_teid, 2))
    message = str(hflags) + str(hmsg_type) + str(hmsg_len) + str(hteid) + \
            str(hseq_num) + str(hspare) + str(payload)
    return message



def csres():
    pass

def echoreq():
    pass

def echores():
    pass

csreq_packet = csreq()

"""
GTPv2 listener on port 2123
variables defined in the begining of the script
"""
mySocket = socket.socket()
mySocket.bind((host,2123))

mySocket.listen(1)
conn, addr = mySocket.accept()

print ("Connection from: " + str(addr))
while True:
        data = conn.recv(1024).decode()
        if not data:
                break
        print ("from connected  user: " + str(data))

        csreq_packet = str(csreq_packet).upper()
        print ("sending: " + str(csreq_packet))
        conn.send(data.encode())

#conn.close()
