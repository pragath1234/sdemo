import pandas as pd
import json

#pip install pandas, pip install xlrd

data_1 = pd.read_excel('D://Django_project//backup(mainframe)//mainframe//media//shri.xlsx', sheet_name=0, header=None)
data_2 = pd.read_excel('D://Django_project//backup(mainframe)//mainframe//media//shri.xlsx', sheet_name=1, header=0)
data_3 = pd.read_excel('D://Django_project//backup(mainframe)//mainframe//media//shri.xlsx', sheet_name=2, header=None)

json_dict = {}

data_1 = data_1.values.tolist()

for i in data_1:
    json_dict[i[0].lower()] = str(i[1])

data_2 = data_2.fillna(0)
data_2_values = data_2.values.tolist()

tmp_b2b = []
tmp_b2cl = []
tmp_b2cs = []

for i in data_2_values:
    if i[1] == 'SALE-B2B':
        b2b_dict = {}
        b2b_dict['ctin'] = str(i[2])
        tmp = {}
        tmp['inum'] = str(i[3])
        tmp['idt'] = str(i[4])
        tmp['val'] = i[8]
        tmp['pos'] = str(i[5])
        tmp["rchrg"] = str(i[7])
        tmp["inv_typ"] = str(i[6])
        tmp_1 = {}
        tmp['itms'] = [tmp_1]
        tmp_1['num'] = int(i[9])
        tmp_2 = {}
        tmp_2['txval'] = int(i[10])
        tmp_2['rt'] = int(i[16])
        tmp_2['iamt'] = int(i[13])
        tmp_2['csamt'] = int(i[14])
        tmp_1['itm_det'] = tmp_2

        b2b_dict['inv'] = [tmp]

        tmp_b2b.append(b2b_dict)
    
    if i[1] == 'SALE-B2CL':
        b2cl_dict = {}
        b2cl_dict['pos'] = str(i[5])
        tmp = {}
        tmp['inum'] = str(i[3])
        tmp['idt'] = str(i[4])
        tmp['val'] = i[8]
        tmp_1 = {}
        tmp['itms'] = [tmp_1]
        tmp_1['num'] = int(i[9])
        tmp_2 = {}
        tmp_2['txval'] = int(i[10])
        tmp_2['rt'] = int(i[16])
        tmp_2['iamt'] = int(i[13])
        tmp_2['csamt'] = int(i[14])
        tmp_1['itm_det'] = tmp_2

        b2cl_dict['inv'] = [tmp]

        tmp_b2cl.append(b2cl_dict)
    
    if i[1] == 'SALE-B2CS':
        b2cs_dict = {}
        b2cs_dict['splt_ty'] = str(i[17])
        b2cs_dict['pos'] = str(i[5])
        b2cs_dict['typ'] = str(i[18])
        b2cs_dict['txval'] = int(i[10])
        b2cs_dict['rt'] = int(i[16])
        b2cs_dict['iamt'] = int(i[13])
        b2cs_dict['camt'] = int(i[11])
        b2cs_dict['samt'] = int(i[12])
        b2cs_dict['csamt'] = int(i[14])

        tmp_b2cs.append(b2cs_dict)

json_dict['b2b'] = [tmp_b2b]
json_dict['b2bl'] = tmp_b2cl
json_dict['b2cs'] = tmp_b2cs

data_3 = data_3.fillna(0)
data_3_values = data_3.values.tolist()

tmp_docs = []

for i in data_3_values:
    if i[0] == 0:
        i.remove(i[0])
    if len(i) > 2:
        i.remove(i[-1])

doc_dict = {}
tmp = {}

for i in data_3_values:
    if i[0] == 'doc_num':
         doc_dict['doc_num'] = i[1]
    if i[0] == 'doc_typ':
        doc_dict['doc_typ'] = i[1]


    if i[0] == 'num':
        tmp['num'] = i[1]
    if i[0] == 'to':
        tmp['to'] = i[1]
    if i[0] == 'from':
        tmp['from'] = i[1]
    if i[0] == 'totnum':
        tmp['totnum'] = i[1]
    if i[0] == 'cancel':
        tmp['cancel'] = i[1]
    if i[0] == 'net_issue':
        tmp['net_issue'] = i[1]

    doc_dict['docs'] = [tmp]

tmp = {}
tmp['doc_det'] = [doc_dict]
json_dict['doc_issue'] = tmp


with open('result.json', 'w') as json_file:
  json.dump(json_dict, json_file, indent = 2)

print("file saved!")