#
# import urllib
# import os
#
# import zipfile2
#
from src.models.factor_data import factor_data
# url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_TXT.zip"
# filename = os.path.basename(url)
# urllib.urlretrieve(url, filename)
# current_path = os.getcwd()
# file_path = current_path + "//" + filename
# with zipfile2.ZipFile(file_path, 'r') as zip_ref:
#     zip_ref.extractall(current_path)
# # print(file_path)
# txt_path = filename[:-8] + ".txt"
# # print(txt_path)
# f = open(txt_path, "r")
# lines = f.readlines()
# lines = [x.split() for x in lines]
# cleaned_lines=lines[4:679]
# # print(cleaned_lines[668])
# half_year=[0]*21
# for i in range(0,21):
#      half_year[i]=cleaned_lines[674-6*i]
#
# # print(half_year)
# factors={}
# factors['MKT']=[]
# factors['SMB']=[]
# factors['HML']=[]
# factors['RMW']=[]
# factors['CMA']=[]
# factors['RF']=[]
# # print(factors)
# for line in half_year:
#      factors['MKT'].append(float(line[1]))
#      factors['SMB'].append(float(line[2]))
#      factors['HML'].append(float(line[3]))
#      factors['RMW'].append(float(line[4]))
#      factors['CMA'].append(float(line[5]))
#      factors['RF'].append(float(line[6]))
# print(factors)
