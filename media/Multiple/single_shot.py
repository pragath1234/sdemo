import pandas as pd
import json
import os
pd.options.mode.chained_assignment = None

d1=pd.read_csv('D://Django_project//backup(mainframe)//mainframe//media//Multiple//K2.csv',thousands=',', dtype={'POS':object,'LOS': object,'INVOICE': object,'NT_NO':object,'fp':object,'NT_DATE':object})

d1['INVOICE']=d1['INVOICE'].str.strip()
d1['GSTIN']=d1['GSTIN'].str.strip()

d2=pd.read_excel('D://Django_project//backup(mainframe)//mainframe//media//Multiple//CDNR.xlsx',dtype={'POS':object,'LOS': object,'INVOICE': object,'NT_NO':object,'fp':object,'NT_DATE':object})
d3=d2[d2.GSTIN.isnull()]
d4=d2[d2.GSTIN.notnull()]
d3['NT_CGST']=d3['NT_CGST']*-1
d3['NT_SGST']=d3['NT_SGST']*-1
d3['NT_IGST']=d3['NT_IGST']*-1
d3['NT_AMT']=d3['NT_AMT']*-1
d_nil=pd.read_excel('D://Django_project//backup(mainframe)//mainframe//media//Multiple//NilGST.xlsx',dtype={'LOS': object,'fp':object})
d1=d1.append(d3)
d1=d1.append(d4)
d1=d1.append(d_nil)

d1['LOSS']=pd.to_numeric(d1['LOS']).round(2)
d1['POSS']=pd.to_numeric(d1['POS']).round(2)

st_1=d1[d1['LOSS']==1]
st_2=d1[d1['LOSS']==2]
st_3=d1[d1['LOSS']==3]
st_4=d1[d1['LOSS']==4]
st_5=d1[d1['LOSS']==5]
st_6=d1[d1['LOSS']==6]
st_7=d1[d1['LOSS']==7]
st_8=d1[d1['LOSS']==8]
st_9=d1[d1['LOSS']==9]
st_10=d1[d1['LOSS']==10]
st_11=d1[d1['LOSS']==11]
st_12=d1[d1['LOSS']==12]
st_13=d1[d1['LOSS']==13]
st_14=d1[d1['LOSS']==14]
st_15=d1[d1['LOSS']==15]
st_16=d1[d1['LOSS']==16]
st_17=d1[d1['LOSS']==17]
st_18=d1[d1['LOSS']==18]
st_19=d1[d1['LOSS']==19]
st_20=d1[d1['LOSS']==20]
st_21=d1[d1['LOSS']==21]
st_22=d1[d1['LOSS']==22]
st_23=d1[d1['LOSS']==23]
st_24=d1[d1['LOSS']==24]
st_27=d1[d1['LOSS']==27]
st_28=d1[d1['LOSS']==28]
st_29=d1[d1['LOSS']==29]
st_30=d1[d1['LOSS']==30]
st_31=d1[d1['LOSS']==31]
st_32=d1[d1['LOSS']==32]
st_33=d1[d1['LOSS']==33]
st_34=d1[d1['LOSS']==34]
st_35=d1[d1['LOSS']==35]
st_36=d1[d1['LOSS']==36]
st_37=d1[d1['LOSS']==37]
st_38=d1[d1['LOSS']==38]

d=[st_1,st_2,st_3,st_4,st_5,st_6,st_7,st_8,st_9,st_10,st_11,st_12,st_13,st_14,st_15,st_16,st_17,st_18,st_19,st_20,st_21,st_22,st_23,st_24,st_27,st_28,st_29,st_30,st_31,st_32,st_33,st_34,st_35,st_36,st_37,st_38]

for k in d:
    if not k.empty:
        k_gstin=k['client_gstin'].iloc[0]
        k_fp=k['fp'].drop_duplicates().iloc[0]
        k_version='GST2.3.1'
        k_hash='hash'
        
        b2b_raw=k[k.GSTIN.notnull()]
        b2b_raww=b2b_raw[b2b_raw['Cat']=='B2b']
        d2= b2b_raww.drop_duplicates(subset='INVOICE', keep="first")
        g=d2.drop(['CHARGE','CGST','SGST','IGST','Sl No.'], axis=1)
        d3 = b2b_raw.groupby(['INVOICE']).sum().reset_index()
        
        b2b_group = pd.merge(d3, g, how='inner',
                             left_on='INVOICE', right_on='INVOICE').drop_duplicates().reset_index()
        b2b_group['INV_DATE'] = pd.to_datetime(b2b_group['INV_DATE'])
        b2b_group['INV_DATE'] = b2b_group['INV_DATE'].dt.strftime('%d-%m-%Y')
        b2b_group['CHARGE']=b2b_group['CHARGE']
        b2b_group['CGST']=b2b_group['CGST']
        b2b_group['SGST']=b2b_group['SGST']
        b2b_group['IGST']=b2b_group['IGST']
        b2b_process=b2b_group[['INVOICE','CHARGE','CGST','SGST','IGST','BRANCHNAME','GSTIN','INV_DATE','POS','LOS']]
        
        b2c_raw=k[k.GSTIN.isnull()]
        b2c_raw=b2c_raw[b2c_raw['Cat']=='b2c']
        b2c_raw['LOS']=pd.to_numeric(b2c_raw['LOS']).round(2)
        b2c_raw['POS']=pd.to_numeric(b2c_raw['POS']).round(2)
        b2cb=b2c_raw.fillna(0)
        b2cb=b2cb[['LOS','POS','CHARGE','CGST','SGST','IGST','NT_CGST','NT_AMT','NT_SGST','NT_IGST','Check']]
        
        b2cb['CGST']=b2cb['CGST']+b2cb['NT_CGST']
        b2cb['CHARGE']=b2cb['CHARGE']+b2cb['NT_AMT']
        b2cb['CHARGE']= b2cb['CHARGE'].round(2)
        b2cb['SGST']=b2cb['SGST']+b2cb['NT_SGST']
        b2cb['IGST']=b2cb['IGST']+b2cb['NT_IGST']
        b2cx=b2cb.drop(['NT_CGST','NT_SGST','NT_IGST','NT_AMT'], axis=1)
        
        b2c_procesd=b2cx.groupby(['LOS','POS','Check']).sum().reset_index()
        b2c_process=b2c_procesd.copy()
        b2c_process["LOS"] = b2c_process.LOS.map("{:02}".format)
        b2c_process["POS"] = b2c_process.POS.map("{:02}".format)
        


        nil_raw=k[k['Cat']=='nil']
        nil_raww=nil_raw[['CHARGE','Nil_Type']]
        
        nil_group=nil_raww.groupby(['Nil_Type']).sum().reset_index()
        nil_group['CHARGE']=nil_group['CHARGE'].round(2)
        nil_X=nil_group.T.reset_index()
        new_header = nil_X.iloc[0]
        nil_X.columns=new_header
        nil_process=nil_X.drop(0)        
    
    
        
        
        
        cdnr_raw=k[(k['Cat']=='cdnr')]
        cdnr2= cdnr_raw.drop_duplicates(subset='NT_NO', keep="first")
        cdnr3=cdnr2.drop(['CHARGE','CGST','SGST','IGST','Sl No.','NT_AMT','NT_CGST','NT_SGST','NT_IGST','RATE'], axis=1)
        cdnr4 = cdnr_raw.groupby(['NT_NO']).sum().reset_index()
        cdnr_group = pd.merge(cdnr4, cdnr3, how='inner',
                              left_on='NT_NO', right_on='NT_NO').drop_duplicates().reset_index()
        
        cdnr_group[['NT_NO','CHARGE','CGST','SGST','IGST','INV_DATE','NT_AMT','NT_CGST','NT_SGST','RATE','NT_IGST','NT_DATE']]
        cdnr_group['NT_DATE'] = pd.to_datetime(cdnr_group['NT_DATE'])
        cdnr_group['NT_DATE'] = cdnr_group['NT_DATE'].dt.strftime('%d-%m-%Y')
        cdnr_group['INV_DATE'] = pd.to_datetime(cdnr_group['INV_DATE'])
        cdnr_group['INV_DATE'] = cdnr_group['INV_DATE'].dt.strftime('%d-%m-%Y')
        cdnr_group['CHARGE']=cdnr_group['CHARGE'].round(2)
        cdnr_group['CGST']=cdnr_group['CGST'].round(2)
        cdnr_group['SGST']=cdnr_group['SGST'].round(2)
        cdnr_group['IGST']=cdnr_group['IGST'].round(2)
        cdnr_group['NT_AMT']=cdnr_group['NT_AMT'].round(2)
        cdnr_group['NT_CGST']=cdnr_group['NT_CGST'].round(2)
        cdnr_group['NT_SGST']=cdnr_group['NT_SGST'].round(2)
        cdnr_group['NT_IGST']=cdnr_group['NT_IGST'].round(2)
        cdnr_process= cdnr_group[['INVOICE','CHARGE','BRANCHNAME','GSTIN','INV_DATE','POS','LOS','NT_DATE','NT_NO','NT_CGST','NT_SGST','NT_IGST','NT_AMT']]
        
        x1=b2b_group['IGST'].sum()
        y1=cdnr_group['NT_IGST'].sum()
        x2=b2b_group['CGST'].sum()
        y2=cdnr_group['NT_CGST'].sum()
        x3=b2b_group['SGST'].sum()
        y3=cdnr_group['NT_SGST'].sum()
        x4=b2b_group['CHARGE'].sum()
        y4=cdnr_group['NT_AMT'].sum()
        
        hsn_process={}
        hsn_process['IGST']=round(x1-y1,2) 
        hsn_process['CGST']=round(x2-y2,2)
        hsn_process['SGST']=round(x3-y3,2)
        hsn_process['CHARGE']=round(x4-y4,2)
        
        
        
     
    
    #UMB_Step2: processing for json file
        
        
        
        data_cdnr=cdnr_process
        data_hsn = hsn_process
    
    
        json_dict = {}
        json_dict['gstin']=k_gstin
        json_dict['fp']=k_fp
        json_dict['version']=k_version
        json_dict['hash']=k_hash
        
        data_b2b = b2b_process
        data_b2b = data_b2b.fillna(0)
        data_b2b_values = data_b2b.values.tolist()
            
        tmp_b2b = []

        for i in data_b2b_values:
            b2b_dict = {}
            b2b_dict['ctin'] = str(i[6]).replace(" ", "")
            tmp = {}
            tmp['inum'] = str(i[0]).replace(" ", "")
            tmp['idt'] = str(i[7])
            tmp['val'] = round(i[1],2)
            tmp['pos'] = str(i[8]).replace(" ", "")
            tmp["rchrg"] = "N"
            tmp["inv_typ"] = "R"
            tmp_1 = {}
            tmp['itms'] = [tmp_1]
            tmp_1['num'] = 1801
            tmp_2 = {}
            tmp_2['txval'] = round(float(i[1]),2)
            tmp_2['rt'] =18
            tmp_2['iamt'] = round(float(i[4]),2)
            if tmp_2['iamt']==0:
                tmp_2['camt'] = round(float(i[3]),2)
                tmp_2['samt'] = round(float(i[2]),2)
            tmp_2['csamt'] = 0
            tmp_1['itm_det'] = tmp_2

            b2b_dict['inv'] = [tmp]

            tmp_b2b.append(b2b_dict)
            if not data_b2b.empty:
                json_dict['b2b'] = tmp_b2b


        data_b2c = b2c_process
        data_b2c = data_b2c.fillna(0)
        data_b2c_values = data_b2c.values.tolist()

        tmp_b2cs = []
        for i in data_b2c_values:
            b2cs_dict = {}
            b2cs_dict['sply_ty'] = str(i[2])
            b2cs_dict['pos'] = str(i[1]).replace(" ", "")
            b2cs_dict['typ'] = 'OE'
            b2cs_dict['txval'] = round(float(i[3]),2)
            b2cs_dict['rt'] = 18
            b2cs_dict['iamt'] = round(float(i[6]),2)
            b2cs_dict['camt'] = round(float(i[4]),2)
            b2cs_dict['samt'] = round(float(i[5]),2)
            b2cs_dict['csamt'] = 0

            tmp_b2cs.append(b2cs_dict)
            if not data_b2c.empty:
                json_dict['b2cs'] = tmp_b2cs


        data_cdnr=cdnr_process
        data_cdnr = data_cdnr.fillna(0)
        data_cdnr_values = data_cdnr.values.tolist()
        
        tmp_cdnr= []

        for i in data_cdnr_values: 
            cdnr_dict = {}
            cdnr_dict['ctin'] = str(i[3])
            tmp = {}
            tmp['nt_num'] = str(i[8])
            tmp['nt_dt'] = str(i[7])
            tmp['val'] = int(i[12])
            tmp['ntty'] = 'C'
            tmp["inum"] = str(i[0])
            tmp["idt"] = str(i[4])
            tmp["p_gst"] = "N"
            tmp_1 = {}
            tmp['itms'] = [tmp_1]
            tmp_1['num'] = 1801
            tmp_2 = {}
            tmp_2['txval'] = round(float(i[12]),2)
            tmp_2['rt'] = 18
            tmp_2['iamt'] = round(float(i[11]),2)
            tmp_2['camt'] = round(float(i[10]),2)
            tmp_2['samt'] = round( float(i[9]),2)
            tmp_2['csamt'] = 0
            tmp_1['itm_det'] = tmp_2
            
            cdnr_dict['nt'] = [tmp]

            tmp_cdnr.append(cdnr_dict)
            if not data_cdnr.empty:
                json_dict['cdnr'] = tmp_cdnr

        data_nil=nil_process
        data_nil = data_nil.fillna(0)
        data_nil_values = data_nil.values.tolist()
        
        tmp_nil= {}

        ftmp_nil= {}

        for i in data_nil_values:
                nb2b_dict={}
                nb2b_dict['sply_ty'] = 'INTRAB2B'
                nb2b_dict['expt_amt'] = round(i[7],2)
                nb2b_dict['nil_amt'] = round(i[9],2)
                nb2b_dict['ngsup_amt'] = round(i[8],2)
                nb2bi_dict={}
                nb2bi_dict['sply_ty'] = 'INTRAB2C'
                nb2bi_dict['expt_amt'] = round(i[10],2)
                nb2bi_dict['nil_amt'] = round(i[12],2)
                nb2bi_dict['ngsup_amt'] = round(i[11],2)
                nb2c_dict={}
                nb2c_dict['sply_ty'] = 'INTRB2B'
                nb2c_dict['expt_amt'] = round(i[1],2)
                nb2c_dict['nil_amt'] = round(i[3],2)
                nb2c_dict['ngsup_amt'] = round(i[2],2)
                nb2ci_dict={}
                nb2ci_dict['sply_ty'] = 'INTRB2C'
                nb2ci_dict['expt_amt'] = round(i[4],2)
                nb2ci_dict['nil_amt'] =  round(i[6],2)
                nb2ci_dict['ngsup_amt'] = round(i[5],2)      
                tmp_nil['inv']=[nb2b_dict,nb2bi_dict,nb2c_dict,nb2ci_dict]
                json_dict['nil'] = tmp_nil        
                
        tmp_hsn= {}

        for i in data_hsn:
            hsn_dict={}
            hsn_dict['num'] = 1
            hsn_dict['hsn_sc'] = '9971'
            hsn_dict['desc'] = 'BFSI'
            hsn_dict['uqc'] = 'OTH'
            hsn_dict['qty'] = 1
            hsn_dict['val']=hsn_process['CHARGE']
            hsn_dict['txval']=hsn_process['CHARGE']
            hsn_dict['camt']=hsn_process['CGST']
            hsn_dict['samt']=hsn_process['SGST']
            hsn_dict['iamt']=hsn_process['IGST']
            hsn_dict['csamt']=0

            tmp_hsn['data']=[hsn_dict]
        json_dict['hsn'] = tmp_hsn
        
        file_name = 'result.json'
        if os.path.isfile(file_name):
            expand = 1
            while True:
                expand += 1
                new_file_name = file_name.split('.json')[0] + str(expand) + '.json'
                if os.path.isfile(new_file_name):
                    continue
                else:
                        file_name = new_file_name
                        break


        with open(file_name, 'x') as json_file:
            json.dump(json_dict, json_file, indent = 2)
          #  print('done')


