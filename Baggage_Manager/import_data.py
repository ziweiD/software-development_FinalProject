#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "United_Baggage_Manager.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()

from Baggage_Recovery_App.models import *
from django.core.files.images import ImageFile
from django.conf import settings
from Baggage_Recovery_App.views import getMatchResultByReport
from Baggage_Recovery_App.matching import *

WorkList = [] #initial a list for saving data

#====================IMPORT CUSTOMER DATA=======================================
CUSTOMER.objects.all().delete() # delete all data in table

f = open('customer_data.txt')
for line in f:
    if line[0] == '#':
        continue
    line = line.strip() # remove '\n' from end of line
    parts = line.replace('"','') #replace '' to be null
    parts = parts.split(';') # split by ;
    WorkList.append(CUSTOMER(MILEAGEPLS_NUM=parts[0], FIRST_NAME=parts[1],
                           MIDDLE_NAME=parts[2], LAST_NAME=parts[3]))
f.close()
CUSTOMER.objects.bulk_create(WorkList)

# #====================IMPORT CONTENT DATA======================================
CONTENT_DETAIL.objects.all().delete() # delete all data in table

f = open('content_data.txt')
WorkList.clear()
for line in f:
    if line[0] == '#':
        continue
    line = line.strip() # remove '\n' from end of line
    parts = line.replace('"','') #replace '' to be null
    parts = parts.split(';') # split by ;
    WorkList.append(CONTENT_DETAIL(ITEM_NUM=parts[0], NAME=parts[1]))
f.close()
CONTENT_DETAIL.objects.bulk_create(WorkList)

#====================IMPORT CUSTOMER IMG DATA===================================
CUSTOMER_BAGGAGE_IMAGE.objects.all().delete() # delete all data in table

f = open('customer_image_data.txt')
WorkList.clear()
for line in f:
    if line[0] == '#':
        continue
    image = CUSTOMER_BAGGAGE_IMAGE()
    line = line.strip() # remove '\n' from end of line
    parts = line.replace('"','') #replace '' to be null
    parts = parts.split(';') # split by ;
    image.CUST_IMG_MILEAGEPLS_NUM = CUSTOMER.objects.get(MILEAGEPLS_NUM=parts[0])
    image.BAG_NAME = parts[1]
    file_path = os.path.join(settings.CUS_IMG_DIR, parts[2])
    file = open(file_path, 'rb')
    image.CUST_IMG.save(parts[2], file)
    image.save()
f.close()

#====================IMPORT WAREHOUSE BAGGAGE DATA========================
# delete all data in table
WAREHOUSE.objects.all().delete()
WAREHOUSE_BAGGAGE_IMAGE.objects.all().delete()
WAREHOUSE_BAGGAGE_DESCRIPTION.objects.all().delete()
BAGGAGE_CONTENT_IMAGE.objects.all().delete()

f = open('warehouse_data.txt')
WorkList.clear()
for line in f:
    line = line.strip() # remove '\n' from end of line
    if line[0] == '#':
        continue
    parts = line.replace('"','') #replace '' to be null
    parts = parts.split(';') # split by ;
    w = WAREHOUSE()
    w.save()
    image = WAREHOUSE_BAGGAGE_IMAGE()
    image.WAREHOUSE_IMG_BAG_ID = WAREHOUSE.objects.get(id=w.id)
    file_path = os.path.join(settings.WARE_IMG_DIR, parts[0])
    file = open(file_path, 'rb')
    image.WAREHOUSE_IMG.save(parts[0], file)
    image.save()
    description = WAREHOUSE_BAGGAGE_DESCRIPTION()
    description.BAG_DESC_WAREHOUSE_BAG_ID = WAREHOUSE.objects.get(id=w.id)
    description.BAG_SIZE = parts[1]
    description.BAG_COLOR = parts[2]
    description.BAG_BRAND = parts[3]
    if parts[4] == "1":
        description.ITEM1 = True
    if parts[5] == "1":
        description.ITEM2 = True
    if parts[6] == "1":
        description.ITEM3 = True
    if parts[7] == "1":
        description.ITEM4 = True
    if parts[8] == "1":
        description.ITEM5 = True
    if parts[9] == "1":
        description.ITEM6 = True
    if parts[10] == "1":
        description.ITEM7 = True
    if parts[11] == "1":
        description.ITEM8 = True
    if parts[12] == "1":
        description.ITEM9 = True
    if parts[13] == "1":
        description.ITEM10 = True
    description.DETAILS = parts[14]
    description.save()
    image = BAGGAGE_CONTENT_IMAGE()
    image.CONTENT_WAREHOUSE_BAG_ID = WAREHOUSE.objects.get(id=w.id)
    file_path = os.path.join(settings.WARE_CONTENT_DIR, parts[15])
    file = open(file_path, 'rb')
    image.CONTENT_IMG.save(parts[15], file)
    image = BAGGAGE_CONTENT_IMAGE()
    image.CONTENT_WAREHOUSE_BAG_ID = WAREHOUSE.objects.get(id=w.id)
    file_path = os.path.join(settings.WARE_CONTENT_DIR, parts[16])
    file = open(file_path, 'rb')
    image.CONTENT_IMG.save(parts[16], file)
f.close()

#====================IMPORT REPORT DATA========================================
CONFIRMATION_DETAIL.objects.all().delete()
REPORT_POTENTIAL_BAG.objects.all().delete()
CUSTOMER_BAGGAGE_DESCRIPTION.objects.all().delete()
REPORT.objects.all().delete()

f = open('report_data.txt')
WorkList.clear()
for line in f:
    if line[0] == '#':
        continue
    line = line.strip() # remove '\n' from end of line
    parts = line.replace('"','') #replace '' to be null
    parts = parts.split(';') # split by ;
    description = CUSTOMER_BAGGAGE_DESCRIPTION()
    description.BAG_COLOR = parts[0]
    description.BAG_SIZE = parts[1]
    description.BAG_BRAND = parts[2]
    if parts[3] == "1":
        description.ITEM1 = True
    if parts[4] == "1":
        description.ITEM2 = True
    if parts[5] == "1":
        description.ITEM3 = True
    if parts[6] == "1":
        description.ITEM4 = True
    if parts[7] == "1":
        description.ITEM5 = True
    if parts[8] == "1":
        description.ITEM6 = True
    if parts[9] == "1":
        description.ITEM7 = True
    if parts[10] == "1":
        description.ITEM8 = True
    if parts[11] == "1":
        description.ITEM9 = True
    if parts[12] == "1":
        description.ITEM10 = True
    description.DETAILS = parts[13]
    description.save()
    report = REPORT()
    report.REPO_MILEAGEPLS_NUM = CUSTOMER.objects.get(MILEAGEPLS_NUM = parts[14])
    report.REPO_BAG_DESC_ID = CUSTOMER_BAGGAGE_DESCRIPTION.objects.get(id=description.id)
    bag = CUSTOMER_BAGGAGE_IMAGE.objects.get(CUST_IMG_MILEAGEPLS_NUM=parts[14])
    report.REPO_BAG_IMG_ID = CUSTOMER_BAGGAGE_IMAGE.objects.get(id=bag.id)
    report.CUST_PERM_ADDR = parts[15]
    report.CUST_TEMP_ADDR = parts[16]
    report.TEMP_ADDR_VALID_DATE = parts[17]
    report.save()
    getMatchResultByReport(report, description)
f.close()
