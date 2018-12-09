import imagehash
from PIL import Image
import queue
import cv2
import numpy as np
from Baggage_Recovery_App.models import *
from django.conf import settings
import os

def resize_img( im, max_dim ):
    '''
    This function will resize the input image to our target dimension.
    @para: im is the input image
    @para: max_dim is the target dimension we want to set the image
    @return: an image after processing
    '''
    scale = float(max_dim) / max(im.shape)
    if scale >= 1:
        return np.copy(im)

    new_size = (int(im.shape[1]*scale), int(im.shape[0]*scale))
    im_new = cv2.resize(im, new_size)   # creates a new image object
    return im_new

def cut(img):
    '''
    This function will grab the baggage outside of its background.
    @para: img is the input image
    @return: an image after processing
    '''
    rect_line = "(1,1) (599,1) (599,449) (1,449)"
    outer_rect = rect_line.split()
    im2arr = cv2.imread(img)
    im2arr = resize_img(im2arr,600).astype(np.uint8)
    mask = np.zeros(im2arr.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    point1 = tuple(eval(outer_rect[0]))
    point2 = tuple(eval(outer_rect[2]))
    rect = (point1[1],point1[0],point2[1]-point1[1],point2[0]-point1[0])

    cv2.grabCut(im2arr,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img_1 = im2arr*mask2[:,:,np.newaxis]
    #path = os.path.splitext(img)
    #cv2.imwrite(path[0]+"_cut"+path[1],img_1)
    return img_1

def matching(lost_img, warehouse_list):
    '''
    This function will match the given lost_image to all the baggages in our warehouse
    and find the top three matched baggages.
    @para: lost_img is the lost image we want to match
    @para: warehouse_list is the images we have in our warehouse
    @return: a list of top three possible images that this image is similiar with
    '''
    cvwarehouse_list = []
    warehouse_hash = []
    for img in warehouse_list:
        file_path = os.path.join(settings.MEDIA_ROOT, img)
        img_1 = cut(file_path)
        cvimg = Image.fromarray(img_1)
        cvwarehouse_list.append(cvimg)
        cvhash = imagehash.phash(cvimg)
        warehouse_hash.append(cvhash)

    file_path = os.path.join(settings.MEDIA_ROOT, lost_img)
    img_1 = cut(file_path)
    cvimg = Image.fromarray(img_1)
    lost_hash = imagehash.phash(cvimg)

    q = queue.PriorityQueue()
    for j in range(len(warehouse_list)):
        q.put((lost_hash-warehouse_hash[j],warehouse_list[j]))

    res = []
    count = 0
    while q.qsize():
        if count == 3:
            break
        tmp = q.get()
        res.append(tmp[1])
        count += 1

    return res

sizeMap = {
    15 : "Carry on or cabin",
    16 : "Small",
    18 : "Small",
    20 : "Medium",
    22 : "Medium",
    24 : "Medium",
    26 : "Large",
    28 : "Large",
    30 : "Large",
    31 : "Oversize",
}

def contentMatchByBag(bagid, threshold):
    '''
    This function is to find the potential reports for a specific bag in warehoouse.
    @para: bagid is the bag id in WAREHOUSE stands for the bag want to find match
    @para: threshold is a number (<= 1) that set the similarity rate
    @return: a list of potential reports with content matched rate bigger than
             threshold
    '''
    description = WAREHOUSE_BAGGAGE_DESCRIPTION.objects.get(BAG_DESC_WAREHOUSE_BAG_ID=bagid)
    reports = REPORT.objects.all()
    potentialReports = []
    for report in reports:
        count = 0
        report_desc = report.REPO_BAG_DESC_ID
        if description.BAG_COLOR == report_desc.BAG_COLOR:
            count += 1.5
        if sizeMap[description.BAG_SIZE] == report_desc.BAG_SIZE:
            count += 1.5
        if description.BAG_BRAND.lower() == report_desc.BAG_BRAND.lower():
            count += 1.5
        if description.ITEM1 == report_desc.ITEM1:
            count += 1
        if description.ITEM2 == report_desc.ITEM2:
            count += 1
        if description.ITEM3 == report_desc.ITEM3:
            count += 1
        if description.ITEM4 == report_desc.ITEM4:
            count += 1
        if description.ITEM5 == report_desc.ITEM5:
            count += 1
        if description.ITEM6 == report_desc.ITEM6:
            count += 1
        if description.ITEM7 == report_desc.ITEM7:
            count += 1
        if description.ITEM8 == report_desc.ITEM8:
            count += 1
        if description.ITEM9 == report_desc.ITEM9:
            count += 1
        if description.ITEM10 == report_desc.ITEM10:
            count += 1
        rate = count * 1.0 / 14.5
        if rate >= threshold:
            potentialReports.append(report.REPO_BAG_IMG_ID.CUST_IMG.name)
    return potentialReports

def contentMatchByReport(description, threshold):
    '''
    This function is to find the potential bags in warehouse for a specific report.
    @para: description is the report description stands for the report want to
           find match
    @para: threshold is a number (<= 1) that set the similarity rate
    @return: a list of potential bags in WAREHOUSE with content matched rate
             bigger than threshold
    '''
    warehouseBags = WAREHOUSE.objects.filter(WAREHOUSE_REPO_STAT=False)
    potentialBags = []
    for bag in warehouseBags:
        count = 0
        bag_desc = WAREHOUSE_BAGGAGE_DESCRIPTION.objects.get(BAG_DESC_WAREHOUSE_BAG_ID=bag.id)
        if description.BAG_COLOR == bag_desc.BAG_COLOR:
            count += 1.5
        if description.BAG_SIZE == sizeMap[bag_desc.BAG_SIZE]:
            count += 1.5
        if description.BAG_BRAND.lower() == bag_desc.BAG_BRAND.lower():
            count += 1.5
        if description.ITEM1 == bag_desc.ITEM1:
            count += 1
        if description.ITEM2 == bag_desc.ITEM2:
            count += 1
        if description.ITEM3 == bag_desc.ITEM3:
            count += 1
        if description.ITEM4 == bag_desc.ITEM4:
            count += 1
        if description.ITEM5 == bag_desc.ITEM5:
            count += 1
        if description.ITEM6 == bag_desc.ITEM6:
            count += 1
        if description.ITEM7 == bag_desc.ITEM7:
            count += 1
        if description.ITEM8 == bag_desc.ITEM8:
            count += 1
        if description.ITEM9 == bag_desc.ITEM9:
            count += 1
        if description.ITEM10 == bag_desc.ITEM10:
            count += 1
        rate = count * 1.0 / 14.5
        if rate >= threshold:
            potentialBags.append(WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG_BAG_ID=bag.id).WAREHOUSE_IMG.name)
    return potentialBags
