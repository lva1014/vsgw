import sys
import re
import binascii

def ie_numid_encode(ivalue,itype):
    """
    Construct IMSI(1) / MSISDN(76) / IMEI(75)
    in: DEC IMSI/MSISDN/IMEI
    out: HEX IMSI/MSISDN/IMEI IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x~ IMSI/MSISDN/IMEI
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    try:
        # Invert IMSI numbers
        i = 0
        while 1:
            temp1 = str(ivalue)[i:i+1]
            temp2 = str(ivalue)[i+1:i+2]
            if len(temp1) == 0:
                break
            if len(temp2) == 0:
                temp2 = "f"
            ie_out = ie_out + "%s%s" %(temp2, temp1)
            i += 2
        # Prepare values
        ileng = hex(int(len(str(ie_out))/2))[2:].zfill(4)
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ie_out)
        return ie_out
    except:
        print('[ie_master.py] %s IE error: %s' %(itype, sys.exc_info()[1]))
        return None

def ie_71_encode(apn, mcc, mnc):
    """
    Construct APN
    in: char APN
    out: HEX APN IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x~ APN name
    """
    ie_out = ""
    itype = 71
    icrfl = 0
    iinst = 0
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        apn = apn.split(".")
        i = 0
        apn_ = ""
        if len(apn) > 1:
            while len(apn) > i:
                if i == 0:
                    apn_ = str(hex(len(apn[i]))[2:].zfill(2)) + \
                            str(''.join(hex(ord(c))[2:] for c in apn[i]))
                else:
                    apn_ = apn_ + str(hex(len(apn[i]))[2:].zfill(2)) + \
                    str(''.join(hex(ord(c))[2:] for c in apn[i]))
                i += 1
        else:
            apn_ = str(hex(len(apn[i]))[2:].zfill(2)) + str(''.join(hex(ord(c))[2:] for c in apn[i]))
        mcc = "mcc%s" %mcc
        mnc = "mnc%s" %(str(mnc).zfill(3))
        mcc = ''.join(hex(ord(c))[2:] for c in mcc)
        mnc = ''.join(hex(ord(c))[2:] for c in mnc)
        gprs = ''.join(hex(ord(c))[2:] for c in "gprs")
        ie_out =  apn_ + "06" + str(mcc) + "06" + str(mnc) + "04" + str(gprs)
        ileng = hex(int(len(ie_out)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ie_out)
        return ie_out
    except:
        print('[ie_master.py] 71 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_72_encode(bps_ul, bps_dl):
    """
    Construct AMBR
    in: DEC UL/DL bps
    out: HEX AMBR IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x8 bps UL
        x8 bps DL
    """
    ie_out = ""
    itype = 72
    icrfl = 0
    iinst = 0
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        bps_dl = hex(int(bps_dl))[2:].zfill(8)
        bps_ul = hex(int(bps_ul))[2:].zfill(8)
        ileng = hex(8)[2:].zfill(4)
        ie_out = "%s%s%s%s%s%s" %(itype, ileng, icrfl, iinst, bps_ul, bps_dl)
        return ie_out
    except:
        print('[ie_master.py] 72 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_77_encode():
    """
    Construct Indications
    in: empty
    out: HEX Indications IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x8 Indications (BIN -> HEX)
    """
    ie_out = ""
    itype = 77
    icrfl = 0
    iinst = 0
    indications = "00180000"  # CRSI=1, PS=1 enabled only
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        ileng = hex(int(len(indications)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, indications)
        return ie_out
    except:
        print('[ie_master.py] 77 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_78_encode():
    """
    Construct PCO
    in: empty
    out: HEX PCO IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x1 Extension (BIN -> HEX)
        x1 Configuration Protocol (BIN -> HEX)
        x~ Proto/ContainerID / IP
        x~ Proto/ContainerID / DNS IPv4
        x~ Proto/ContainerID / P-CSCF IPv4
        x~ Proto/ContainerID / IP allocation via NAS
    """
    ie_out = ""
    itype = 78
    icrfl = 0
    iinst = 0
    proto_id1 = "8021000001000010810600000000830600000000"
    proto_id2 = "000d00"
    proto_id3 = "000c00"
    proto_id4 = "000a00"
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        ileng = hex(int(len(proto_id1+proto_id2+proto_id3+proto_id4)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s%s%s%s" %(itype, ileng, icrfl, iinst, proto_id1,\
                                    proto_id2, proto_id3, proto_id4)
        return ie_out
    except:
        print('[ie_master.py] 78 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_79_encode():
    """
    Construct Selection Mode
    in: DEC Mode
    out: HEX Selection Mode IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x2 PDN Type
        x8 IPv4 / x32 IPv6
    """
    ie_out = ""
    itype = 79
    icrfl = 0
    iinst = 0
    ptype = 1
    ip_addr = ""
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        ptype = hex(ptype)[2:].zfill(2)
        if ptype == "01":
            if re.search(r'^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', ip_addr):
                ip_addr = ip_addr.split(".")
                ip_addr = str(hex(ip_addr[0])[2:])+str(hex(ip_addr[1])[2:])+\
                            str(hex(ip_addr[2])[2:])+str(hex(ip_addr[3])[2:])
            else:
                ip_addr = "00000000"
        ileng = hex(1+int(len(ip_addr)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ptype, ip_addr)
        return ie_out
    except:
        print('[ie_master.py] 79 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_82_encode(rat):
    """
    Construct RAT Type
    in: DEC RAT
    out: HEX RAT IE
    structure:
        x2 IE Type
        x4 IE Length
        x2 CR Flag (BIN -> HEX)
        x2 RAT
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 82
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        rat = hex(rat)[2:].zfill(2)
        ileng = hex(int(len(rat)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, rat)
        return ie_out
    except:
        print('[ie_master.py] 82 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_83_encode(mcc, mnc):
    """
    Construct Serving Network
    in: DEC MCC, MNC
    out: HEX MCC + MNC IE
    structure:
        x2 IE Type
        x4 IE Length
        x2 CR Flag (BIN -> HEX)
        x6 MCC + MNC (mixed)
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 83
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        mcc = str(mcc).zfill(3)
        mnc = str(mnc).zfill(3)
        ie_out = mcc[1:2]+mcc[:1]+mnc[2:3]+mcc[2:3]+mnc[1:2]+mnc[:1]
        ileng = hex(int(len(mcc+mnc)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ie_out)
        return ie_out
    except:
        print('[ie_master.py] 83 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_86_encode(uli_mcc, uli_mnc, uli_tai, uli_ecgi_enodebid, uli_ecgi_cellid):
    """
    Construct User Location IE (86)
    in: DEC MCC, MNC, TAI, eNbID, CellID
    out: HEX ULI IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x2 Flags
            nn.. .... Spare
            ..n. .... LAI
            ...n .... ECGI
            .... n... TAI
            .... .n.. RAI
            .... ..n. SAI
            .... ...n CGI
        x10 TAI
            x3 MNC x3 MCC (mixed)
            x4 TAC
        x14 ECGI
            x3 MNC x3 MCC (mixed)
            x1 Spare
            x7 ECI
                x5 eNbID
                x2 CellID
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 86
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        uli_flags = "18"    # ECGI + TAI for now
        uli_mcc = str(uli_mcc)
        uli_mnc = str(uli_mnc).zfill(3)
        mncmcc = uli_mcc[1:2]+uli_mcc[:1]+uli_mnc[2:3]+uli_mcc[2:3]+uli_mnc[1:2]\
                +uli_mnc[:1]
        uli_tai = str(hex(uli_tai)[2:]).zfill(4)
        uli_ecgi_enodebid = str(hex(uli_ecgi_enodebid)[2:]).zfill(5)
        uli_ecgi_cellid = str(hex(uli_ecgi_cellid)[2:]).zfill(2)
        ileng = hex(int(1 + len(uli_flags + uli_mcc + uli_mnc + uli_tai + \
                                uli_mcc + uli_mnc + uli_ecgi_enodebid + \
                                uli_ecgi_cellid)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s%s%s%s%s%s%s" %(itype, ileng, icrfl, iinst, \
                                                uli_flags, mncmcc, uli_tai, \
                                                mncmcc, '0', uli_ecgi_enodebid, \
                                                uli_ecgi_cellid)
        return ie_out
    except:
        print('[ie_master.py] 86 IE error: %s' %sys.exc_info()[1])
        return None

def ie_87_encode(ipv, intype, teid, fteid):
    """
    Construct Serving Network
    in: DEC IPv4/IPv6, Interface Type, TEID, FTEID IP
    out: HEX FTEID Info IE
    structure:
        x2 IE Type
        x4 IE Length
        x2 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x1 IPv4 / IPv6 (BIN -> HEX)
        x1 If type (BIN -> HEX)
        x8 TEID/GRE
        x8 IPaddrr when IPv4 / x32 IP addr when IPv6
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 87
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        if int(ipv) == 4:
            ipv = 8
        #if int(ipv) == 6:
        #    ipv = 4
        intype = hex(int(intype))[2:]
        if len(str(teid)) < 8:
            teid = str(teid).zfill(8)
        if re.search(r'^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', fteid):
            addr = fteid.split(".")
            addr = str(hex(int(addr[0]))[2:])+str(hex(int(addr[1]))[2:])+\
                    str(hex(int(addr[2]))[2:])+str(hex(int(addr[3]))[2:])
        else:
            addr = "01020304"
        ie_out = str(ipv) + str(intype) + str(teid) + str(addr)
        ileng = hex(int(len(ie_out)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ie_out)
        return ie_out
    except:
        print('[ie_master.py] 87 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_93_encode(pgw_ip_add, mbr_ul, mbr_dl, gbr_ul, gbr_dl, qci):
    """
    Construct Bearer Ctx
    in: mbr_ul, mbr_dl, gbr_ul, gbr_dl, qci
    out: HEX Bearer Ctx IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
            x2 IE Type
            x4 IE Length
            x1 CR Flag (BIN -> HEX)
            x1 Instance (BIN -> HEX)
            x1 Spare Bits
            x1 Bearer ID
            ****
            x2 IE Type
            x4 IE Length
            x1 CR Flag (BIN -> HEX)
            x1 Instance (BIN -> HEX)
            x2 PCI / PL / PVI
                PCI = enabled, PL = 4, PVI = enabled
            x2 Label (QCI)
            x10 MBR UL
            x10 MBR DL
            x10 GBR UL
            x10 GBR DL
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 93
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        # included EBI
        inc1_itype = hex(int(73))[2:].zfill(2)
        inc1_crfl = 0
        inc1_inst = 0
        inc1_spar = 0
        bearer_id = 5
        inc1_leng = "0001"
        ie_out = str(inc1_itype) + str(inc1_leng) + str(inc1_crfl) + str(inc1_inst)\
            + str(inc1_spar) + str(bearer_id)
        # included Bearer QoS
        inc2_itype = hex(int(80))[2:].zfill(2)
        inc2_len = "0016"
        inc2_crfl = 0
        inc2_inst = 0
        inc2_pci_pl_pvi = 10 # enable,4,enable
        inc2_label = hex(int(qci))[2:].zfill(2)
        mbr_ul = hex(int(mbr_ul))[2:].zfill(10)
        mbr_dl = hex(int(mbr_dl))[2:].zfill(10)
        gbr_ul = hex(int(gbr_ul))[2:].zfill(10)
        gbr_dl = hex(int(gbr_dl))[2:].zfill(10)
        ie_out = ie_out + str(inc2_itype) + str(inc2_len) + str(inc2_crfl) + \
                str(inc2_inst) + str(inc2_pci_pl_pvi) + str(inc2_label) + \
                str(mbr_ul) + str(mbr_dl) + str(gbr_ul) + str(gbr_dl)
        ileng = hex(int(len(ie_out)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, ie_out)
        return ie_out
    except:
        print('[ie_master.py] 93 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_99_encode():
    """
    Construct PDN Type
    in: DEC Type
    out: HEX PDN Type IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x1 Spare (BIN -> HEX)
        x1 PDN Type (BIN -> HEX)
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 99
    ptype = 1       # IPv4 only for now
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        ptype = hex(ptype)[2:]
        ileng = hex(int(1))[2:].zfill(4)
        ie_out = "%s%s%s%s0%s" %(itype, ileng, icrfl, iinst, ptype)
        return ie_out
    except:
        print('[ie_master.py] 99 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_114_encode():
    """
    Construct TZ
    in: empty
    out: HEX TZ IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance
        x2 TZ
        x2 DST
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 114
    tz = "69"     # GMT-4
    dst = 1    # +1h DST
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        dst = hex(dst)[2:].zfill(2)
        ileng = hex(int(len(tz+dst)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s%s" %(itype, ileng, icrfl, iinst, tz, dst)
        return ie_out
    except:
        print('[ie_master.py] 114 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_127_encode():
    """
    Construct APN Restrictions
    in: empty
    out: HEX APN Restrictions IE
    structure:
        x2 IE Type
        x4 IE Length
        x1 CR Flag (BIN -> HEX)
        x1 Instance (BIN -> HEX)
        x2 APN Restrictions
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 127
    apn_res = 0
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        apn_res = hex(apn_res)[2:].zfill(2)
        ileng = hex(int(len(apn_res)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, apn_res)
        return ie_out
    except:
        print('[ie_master.py] 127 IE error: %s' %(sys.exc_info()[1]))
        return None

def ie_128_encode():
    """
    Construct Selection Mode
    in: DEC Mode
    out: HEX Selection Mode IE
    structure:
        x2 IE Type
        x4 IE Length
        x2 CR Flag (BIN -> HEX)
        x2 Selectio Mode
    """
    ie_out = ""
    icrfl = 0
    iinst = 0
    itype = 128
    smode = 0
    try:
        itype = hex(itype)[2:].zfill(2)
        icrfl = hex(icrfl)[2:]
        iinst = hex(iinst)[2:]
        smode = hex(smode)[2:].zfill(2)
        ileng = hex(int(len(smode)/2))[2:].zfill(4)
        ie_out = "%s%s%s%s%s" %(itype, ileng, icrfl, iinst, smode)
        return ie_out
    except:
        print('[ie_master.py] 128 IE error: %s' %(sys.exc_info()[1]))
        return None
