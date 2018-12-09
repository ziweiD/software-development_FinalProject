from django.http import HttpResponse, request, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from Baggage_Recovery_App.models import *
from Baggage_Recovery_App.matching import *
from django.utils import timezone
import random

##########################
#   Adjustable variable  #
##########################
THRESHOLD = 0.5

#===============================================================================
# load page for customer side
def index(request):
    '''
    This function is to render the index.html (customer side)
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/index.html')
    return HttpResponse(template.render({}, request))

def log_in(request):
    '''
    This function is to render the log-in.html for customer log in.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/log-in.html')
    return HttpResponse(template.render({}, request))

def my_baggage(request):
    '''
    This function is to render the my-baggage.html to show all the baggages that
    registered by the customer.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/baggage-management/my-baggage.html')
    return HttpResponse(template.render({}, request))

def add_new_bag(request):
    '''
    This function is to render the add-new-bag.html to enable the customer add
    a new bag.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/baggage-management/add-new-bag.html')
    return HttpResponse(template.render({}, request))

def edit_bag(request):
    '''
    This function is to render the edit-bag.html to enable the customer edit a
    registered bag.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/baggage-management/edit-bag.html')
    return HttpResponse(template.render({}, request))

def report_missing_bag(request):
    '''
    This function is to render the report-missing-bag.html to enable the customer
    process a missing report.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with showing all registered bags
    '''
    template = loader.get_template('Baggage_Recovery_App/missing-report/report-missing-bag.html')
    items = {}
    contents = CONTENT_DETAIL.objects.all()
    for content in contents:
        items["item"+str(content.ITEM_NUM)] = content.NAME
    return HttpResponse(template.render(items, request))

def report_submission_finished(request):
    '''
    This function is to render the report-submission-finished.html to show a
    success page if the report is submitted successfully.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/missing-report/report-submission-finished.html')
    return HttpResponse(template.render({}, request))

def all_reports_customer(request):
    '''
    This function is to render the all-reports.html for displaying all reports
    that the customer has.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of reports.
    '''
    pid = request.GET.get("pid")
    reports = []
    rawReports = REPORT.objects.filter(REPO_MILEAGEPLS_NUM=pid)
    for report in rawReports:
        reports.append({
            "reportId" : report.id,
            "bagImage" : "../../../static/uploads/" + str(report.REPO_BAG_IMG_ID.CUST_IMG),
            "date" : report.REPO_DATE,
            "status" : report.REPO_STATUS,
        })
    print(reports)
    template = loader.get_template('Baggage_Recovery_App/check-report-status/all-reports.html')
    return HttpResponse(template.render({"reports" : reports}, request))

def confirm_bag_image(request):
    '''
    This function is to render the confirm-bag-image.html for customer to confirm
    the ownership of this bag by bag appearance.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of bag images. It
            must include a right bag that confirmed by warehouse employees.
    '''
    reportId = request.GET.get("reportId")
    bag = REPORT.objects.get(id=reportId).REPO_WAREHOUSE_BAG_ID
    last = WAREHOUSE.objects.filter().last().id
    first = WAREHOUSE.objects.filter().first().id
    presentBagId = []
    count = 0
    for i in range(0,4):
        if i + bag.id <= last:
            presentBagId.append(i + bag.id)
        else:
            presentBagId.append(first + count)
            count += 1
    random.shuffle(presentBagId)
    print(presentBagId)
    bags = []
    for id in presentBagId:
        imagePath = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG_BAG_ID=id).WAREHOUSE_IMG.name
        bag = {
            "bagid" : id,
            "bagImage" : "../../../static/uploads/" + imagePath,
        }
        bags.append(bag)
    print(bags)
    template = loader.get_template('Baggage_Recovery_App/check-report-status/confirm-bag-image.html')
    return HttpResponse(template.render({"bags" : bags}, request))

def confirm_bag_content(request):
    '''
    This function is to render the contact-information.html for customer to
    confirm their ownership of this bag by choosing the right content images.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of content images. It
            must include two right contnets which is corresponding to the right bag
            confirmed by warehouse employees.
    '''
    reportId = request.GET.get("reportId")
    bag = REPORT.objects.get(id=reportId).REPO_WAREHOUSE_BAG_ID
    last = WAREHOUSE.objects.filter().last().id
    first = WAREHOUSE.objects.filter().first().id
    presentBagId = []
    count = 0
    for i in range(0,4):
        if i + bag.id <= last:
            presentBagId.append(i + bag.id)
        else:
            presentBagId.append(first + count)
            count += 1
    print(presentBagId)
    contents = []
    for id in presentBagId:
        images = BAGGAGE_CONTENT_IMAGE.objects.filter(CONTENT_WAREHOUSE_BAG_ID=id)
        for image in images:
            contents.append({
                "contentId" : image.id,
                "contentImage" : "../../../static/uploads/" + image.CONTENT_IMG.name,
            })
    random.shuffle(contents)
    print(contents)
    template = loader.get_template('Baggage_Recovery_App/check-report-status/confirm-bag-content.html')
    return HttpResponse(template.render({"contents" : contents}, request))

def contact_information(request):
    '''
    This function is to render the contact-information.html for customer to
    provide their contact information including the email, phone and their
    avaliable time/date.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/check-report-status/contact-information.html')
    return HttpResponse(template.render({}, request))

def error_matching(request):
    '''
    This function is to render the error-matching.html for showing a error page
    when customer think none of the bag shown is his/her bag.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template.
    '''
    template = loader.get_template('Baggage_Recovery_App/check-report-status/error-matching.html')
    return HttpResponse(template.render({}, request))

#===============================================================================
# functionality for customer side
def submitPassengerId(request):
    '''
    Get the MileagePlus number that the customer entered. If the MileagePlus
    number exists, redirect to index.html. Otherwise return a error message.
    @para: request is a HTTP request, use GET method to get the MileagePlus number
    @return: redirect to index.html or a JsonResponse showing error message
    '''
    pid = request.GET.get("pid")
    if CUSTOMER.objects.filter(MILEAGEPLS_NUM=pid).exists():
        return redirect(to="index.html")
    else:
        return JsonResponse({"No matching MileagePlus Member found."})

def addNewBag(request):
    '''
    Save new bag appearance and bag name to a corresponding MileagePlus number.
    @para: request is a HTTP request, use POST method to get the MileagePlus
          number, bag image and bag name.
    @return: redirect to getSavedBags.html
    '''
    if request.method == "POST":
        saveBag = CUSTOMER_BAGGAGE_IMAGE()
        saveBag.CUST_IMG_MILEAGEPLS_NUM = CUSTOMER.objects.get(MILEAGEPLS_NUM = request.POST.get("pid"))
        saveBag.CUST_IMG = request.FILES.get("bagImage")
        saveBag.BAG_NAME = request.POST.get("bagName")
        saveBag.save()
    else:
        return redirect(to='add-new-bag.html')
    url = 'getSavedBags.html?pid=' + saveBag.CUST_IMG_MILEAGEPLS_NUM.MILEAGEPLS_NUM
    return redirect(to=url)

def getSavedBags(request):
    '''
    Showing all saved bags for a specific MileagePlus number.
    @para: request is a HTTP request, use GET method to get the MileagePlus
          number(pid)
    @return: a HttpResponse of a template with a list of bags
    '''
    pid = request.GET.get("pid")
    reportMissingBag = request.GET.get("reportMissingBag")
    bags = CUSTOMER_BAGGAGE_IMAGE.objects.filter(CUST_IMG_MILEAGEPLS_NUM=pid)
    data = []
    for bag in bags:
        data.append({
            'bagID' : bag.id,
            'bagName' : bag.BAG_NAME,
            'time' : bag.ADD_DATE,
            'url' : "../../../static/uploads/" + str(bag.CUST_IMG)
        })
    if reportMissingBag == "true":
        return JsonResponse({ "data" : data })
    else:
        template = loader.get_template('Baggage_Recovery_App/baggage-management/my-baggage.html')
        return HttpResponse(template.render({ "bags" : data}, request))

def getSavedBag(request):
    '''
    Showing a saved bag for a specific bag id.
    @para: request is a HTTP request, use GET method to get the bagid
    @return: a JsonResponse with the details of that bag
    '''
    bagid = request.GET.get("bagid")
    bag = CUSTOMER_BAGGAGE_IMAGE.objects.get(id=bagid)
    data = {
        'bagName' : bag.BAG_NAME,
        'url' : "../../../static/uploads/" + str(bag.CUST_IMG),
        'bagID' : bag.id
    }
    return JsonResponse(data)

def editBag(request):
    '''
    Save the change to a saved bag. Custoemr can change the bag image and the bag
    name.
    @para: request is a HTTP request, use POST method to get the bagID, bagName
           and bagImage.
    @return: redirect to my-baggage.html
    '''
    if request.method == "POST":
        bagID = request.POST.get("bagID")
        bagName = request.POST.get("bagName")
        bagImage = request.FILES.get("bagImage")
        bag = CUSTOMER_BAGGAGE_IMAGE.objects.get(id=bagID)
        if bagName:
            bag.BAG_NAME = bagName
        if bagImage != None:
            bag.CUST_IMG.delete(save=False)
            bag.CUST_IMG = bagImage
        bag.save()
    else:
        return redirect(to='my-baggage.html')
    url = 'getSavedBags.html?pid=' + bag.CUST_IMG_MILEAGEPLS_NUM.MILEAGEPLS_NUM
    return redirect(to=url)

def deleteBag(request):
    '''
    Delete a saved bag.
    @para: request is a HTTP request, use GET method to get the bagid
    @return: redirect to my-baggage.html
    '''
    bagid = request.GET.get("bagid")
    if REPORT.objects.filter(REPO_BAG_IMG_ID=bagid).exists():
        # template = loader.get_template('Baggage_Recovery_App/baggage-management/error-delete-bag.html')
        # return HttpResponse(template.render({}, request))
        return JsonResponse({"error": "There still exists unresolved missing baggage report related to this bag."})
    bag = CUSTOMER_BAGGAGE_IMAGE.objects.get(id=bagid)
    url = 'getSavedBags.html?pid=' + bag.CUST_IMG_MILEAGEPLS_NUM.MILEAGEPLS_NUM
    bag.delete()
    return redirect(to=url)
    #return redirect(to="my-baggage.html")

def getMatchResultByReport(report, description):
    '''
    Find all bags in WAREHOUSE that match the given report and save the matching
    result in the database.
    @para: report is the given report (an REPORT object)
           description is the description of the given report (a
           CUSTOMER_BAGGAGE_DESCRIPTION object)
    '''
    potentialBags = contentMatchByReport(description, THRESHOLD)
    print("content match by report: ")
    print(potentialBags)
    lost_img = report.REPO_BAG_IMG_ID.CUST_IMG
    finalBags = matching(lost_img.name, potentialBags)
    print("image match by report: ")
    print(finalBags)
    matchedResult = None
    if REPORT_POTENTIAL_BAG.objects.filter(REPORT_ID=report).exists():
        matchedResult = REPORT_POTENTIAL_BAG.objects.get(REPORT_ID=report)
    else:
        matchedResult = REPORT_POTENTIAL_BAG()
        matchedResult.REPORT_ID = report
    matchedResult.NUM = len(finalBags)
    if len(finalBags) >= 1:
        matchedResult.BAG_ID1 = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG=finalBags[0]).WAREHOUSE_IMG_BAG_ID
    if len(finalBags) >= 2:
        matchedResult.BAG_ID2 = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG=finalBags[1]).WAREHOUSE_IMG_BAG_ID
    if len(finalBags) >= 3:
        matchedResult.BAG_ID3 = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG=finalBags[2]).WAREHOUSE_IMG_BAG_ID
    matchedResult.save()

def saveReport(request):
    '''
    Save all the details of a new report and call getMatchResultByReport() to
    save the matching result in the database.
    @para: request is a HTTP request, use POST method to get all the details of
           the report
    @return: redirect to report-submission-finished.html
    '''
    if request.method == "POST":
        bagid = request.POST.get("missingBag")
        if REPORT.objects.filter(REPO_BAG_IMG_ID=bagid).exists():
            template = loader.get_template('Baggage_Recovery_App/baggage-management/error-report-duplicate-bag.html')
            return HttpResponse(template.render({}, request))
        description = CUSTOMER_BAGGAGE_DESCRIPTION()
        description.BAG_SIZE = request.POST.get("size")
        description.BAG_COLOR = request.POST.get("color")
        description.BAG_BRAND = request.POST.get("brand")
        if request.POST.get("item1"):
            description.ITEM1 = True
        if request.POST.get("item2"):
            description.ITEM2 = True
        if request.POST.get("item3"):
            description.ITEM3 = True
        if request.POST.get("item4"):
            description.ITEM4 = True
        if request.POST.get("item5"):
            description.ITEM5 = True
        if request.POST.get("item6"):
            description.ITEM6 = True
        if request.POST.get("item7"):
            description.ITEM7 = True
        if request.POST.get("item8"):
            description.ITEM8 = True
        if request.POST.get("item9"):
            description.ITEM9 = True
        if request.POST.get("item10"):
            description.ITEM10 = True
        description.DETAILS = request.POST.get("details")
        description.save()
        report = REPORT()
        report.REPO_MILEAGEPLS_NUM = CUSTOMER.objects.get(MILEAGEPLS_NUM = request.POST.get("pid"))
        report.REPO_BAG_DESC_ID = CUSTOMER_BAGGAGE_DESCRIPTION.objects.get(id=description.id)
        report.REPO_BAG_IMG_ID = CUSTOMER_BAGGAGE_IMAGE.objects.get(id=bagid)
        report.CUST_PERM_ADDR = request.POST.get("permanantAddress")
        report.CUST_TEMP_ADDR = request.POST.get("temporaryAddress")
        report.TEMP_ADDR_VALID_DATE = request.POST.get("validBefore")
        report.save()
        getMatchResultByReport(report, description)
    else:
        return redirect(to='report-missing-bag.html')
    return redirect(to='report-submission-finished.html')

def saveConfirmationId(request):
    '''
    Save the bag image and bag content images that chosen by customer.
    @para: request is a HTTP request, use POST method to get the reportId, bagId,
           contentId1 and contentId2
    @return: redirect to contact-information.html
    '''
    #print("Save confirmation details")
    if request.method == "POST":
        reportId = request.POST.get("reportId")
        bagId = request.POST.get("bagId")
        contentId1 = request.POST.get("contentId1")
        contentId2 = request.POST.get("contentId2")
        confirmation = None
        if CONFIRMATION_DETAIL.objects.filter(REPO_ID=reportId):
            confirmation = CONFIRMATION_DETAIL.objects.get(REPO_ID=reportId)
        else:
            confirmation = CONFIRMATION_DETAIL()
        confirmation.REPO_ID = REPORT.objects.get(id=reportId)
        confirmation.CONFRIM_BAG_ID = WAREHOUSE.objects.get(id=bagId)
        confirmation.CONFRIM_CONTENT_ID1 = BAGGAGE_CONTENT_IMAGE.objects.get(id=contentId1)
        confirmation.CONFRIM_CONTENT_ID2 = BAGGAGE_CONTENT_IMAGE.objects.get(id=contentId2)
        confirmation.save()
    else:
        return redirect(to='all-reports.html')
    #print("Redirecting...")
    url = 'contact-information.html?reportId=' + reportId
    return redirect(to=url)

def saveContactInformation(request):
    '''
    Save the contact information provided by customer.
    @para: request is a HTTP request, use POST method to get the reportId, email,
           phone and date
    @return: a HttpResponse of appointment-made.html with the date/time provided
             by customer
    '''
    if request.method == "POST":
        reportId = request.POST.get("reportId")
        confirmation = CONFIRMATION_DETAIL.objects.get(REPO_ID=reportId)
        confirmation.CUST_EMAIL = request.POST.get("email")
        confirmation.CUST_PHONE = request.POST.get("phone")
        confirmation.CONFIRMATION_DATE = request.POST.get("date")
        confirmation.save()
        report = REPORT.objects.get(id=reportId)
        report.REPO_STATUS = 2
        report.save()
        #print("\nContact Information Saved")
    else:
        return redirect(to='all-reports.html')
    template = loader.get_template('Baggage_Recovery_App/check-report-status/appointment-made.html')
    return HttpResponse(template.render({ "time" : confirmation.CONFIRMATION_DATE }, request))

def submitErrorMatching(request):
    '''
    When customer thinks none of the bags shown is his/her bag, clear the matching
    result in the warehouse and find the right bag again.
    @para: request is a HTTP request, use GET method to get the reportId
    @return: redirect to error-matching.html
    '''
    reportId = request.GET.get("reportId")
    report = REPORT.objects.get(id=reportId)
    report.REPO_STATUS = 0
    report.REPO_WAREHOUSE_BAG_ID = None
    report.save()
    description = report.REPO_BAG_DESC_ID
    getMatchResultByReport(report, description)
    return redirect(to='error-matching.html')

#===============================================================================
# load page for warehouse side
def warehouse(request):
    '''
    This function is to render the warehouse.html to show the index page for warehouse.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/warehouse.html')
    WAREHOUSE.objects.exclude(id__in =
        WAREHOUSE_BAGGAGE_IMAGE.objects.all().values_list('WAREHOUSE_IMG_BAG_ID_id', flat=True)).delete()
    return HttpResponse(template.render({}, request))

def employee_log_in(request):
    '''
    This function is to render the employee-login.html to enable the warehouse
    employees log in.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template
    '''
    template = loader.get_template('Baggage_Recovery_App/employee-login.html')
    return HttpResponse(template.render({}, request))

def baggage_appearance(request):
    '''
    This function is to render the baggage-appearance.html for the warehouse
    employees to register a new bag.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with an assigned bagid
    '''
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/baggage-appearance.html')
    w = WAREHOUSE()
    w.save()
    return HttpResponse(template.render({'bagid' : w.id}, request))

def baggage_content(request):
    '''
    This function is to render the baggage-content.html for the warehouse
    employees to fill in the content details form.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with 10 given items' name.
    '''
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/baggage-content.html')
    items = {}
    contents = CONTENT_DETAIL.objects.all()
    for content in contents:
        items["item"+str(content.ITEM_NUM)] = content.NAME
    return HttpResponse(template.render(items, request))

def content_one(request):
    '''
    This function is to render the content-one.html for the warehouse employees
    to upload the first content image.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template.
    '''
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/content-one.html')
    return HttpResponse(template.render({}, request))

def content_two(request):
    '''
    This function is to render the content-two.html for the warehouse employees
    to upload the second content image.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template.
    '''
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/content-two.html')
    return HttpResponse(template.render({}, request))

def registration_finished(request):
    '''
    This function is to render the registration-finished.html.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template.
    '''
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/registration-finished.html')
    return HttpResponse(template.render({}, request))

def process_all_reports(request):
    '''
    This function is to render the all-reports.html for displaying all reports which
    don't confirm a right match.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of reports.
    '''
    reports = []
    rawReports = REPORT.objects.exclude(REPO_WAREHOUSE_BAG_ID__isnull=False)
    for report in rawReports:
        reports.append({
            "reportId" : report.id,
            "bagImage" : "../../../static/uploads/" + str(report.REPO_BAG_IMG_ID.CUST_IMG),
            "date" : report.REPO_DATE,
            "numMatched" : REPORT_POTENTIAL_BAG.objects.get(REPORT_ID=report.id).NUM,
        })
    print(reports)
    template = loader.get_template('Baggage_Recovery_App/wh-process-report/all-reports.html')
    return HttpResponse(template.render({"reports" : reports}, request))

def matching_result_by_report(request):
    '''
    This function is to render the matching-result-by-report.html for displaying
    all matched result for a specific report.
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of matched result.
    '''
    reportId = request.GET.get("reportId")
    report = REPORT.objects.get(id=reportId)
    description = report.REPO_BAG_DESC_ID
    items = CONTENT_DETAIL.objects.all()
    data = {}
    data["report"] = {
        "reportId" : reportId,
        "bagImage" : "../../../static/uploads/" + report.REPO_BAG_IMG_ID.CUST_IMG.name,
        "bagColor" : description.BAG_COLOR,
        "bagSize" : description.BAG_SIZE,
        "bagBrand" : description.BAG_BRAND,
        "ITEM1NAME" : items[0].NAME,
        "ITEM2NAME" : items[1].NAME,
        "ITEM3NAME" : items[2].NAME,
        "ITEM4NAME" : items[3].NAME,
        "ITEM5NAME" : items[4].NAME,
        "ITEM6NAME" : items[5].NAME,
        "ITEM7NAME" : items[6].NAME,
        "ITEM8NAME" : items[7].NAME,
        "ITEM9NAME" : items[8].NAME,
        "ITEM10NAME" : items[9].NAME,
        "ITEM1" : description.ITEM1,
        "ITEM2" : description.ITEM2,
        "ITEM3" : description.ITEM3,
        "ITEM4" : description.ITEM4,
        "ITEM5" : description.ITEM5,
        "ITEM6" : description.ITEM6,
        "ITEM7" : description.ITEM7,
        "ITEM8" : description.ITEM8,
        "ITEM9" : description.ITEM9,
        "ITEM10" : description.ITEM10,
        "details" : description.DETAILS,
    }
    potentialBags = REPORT_POTENTIAL_BAG.objects.get(REPORT_ID=reportId)
    warehouseBags = []
    if potentialBags.NUM >= 1:
        warehouseBags.append(potentialBags.BAG_ID1)
    if potentialBags.NUM >= 2:
        warehouseBags.append(potentialBags.BAG_ID2)
    if potentialBags.NUM >= 3:
        warehouseBags.append(potentialBags.BAG_ID3)
    if len(warehouseBags) != 0:
        data["bags"] = []
        for b in warehouseBags:
            image = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG_BAG_ID=b.id)
            description = WAREHOUSE_BAGGAGE_DESCRIPTION.objects.get(BAG_DESC_WAREHOUSE_BAG_ID=b.id)
            bag = {
                "bagId" : b.id,
                "bagImage" : "../../../static/uploads/" + image.WAREHOUSE_IMG.name,
                "bagColor" : description.BAG_COLOR,
                "bagSize" : description.BAG_SIZE,
                "bagBrand" : description.BAG_BRAND,
                "ITEM1" : description.ITEM1,
                "ITEM2" : description.ITEM2,
                "ITEM3" : description.ITEM3,
                "ITEM4" : description.ITEM4,
                "ITEM5" : description.ITEM5,
                "ITEM6" : description.ITEM6,
                "ITEM7" : description.ITEM7,
                "ITEM8" : description.ITEM8,
                "ITEM9" : description.ITEM9,
                "ITEM10" : description.ITEM10,
                "details" : description.DETAILS,
            }
            data["bags"].append(bag)
    template = loader.get_template('Baggage_Recovery_App/wh-process-report/matching-result-by-report.html')
    return HttpResponse(template.render(data, request))

def process_resolved_report(request):
    '''
    This function is to render the all-resolved-reports.html for displaying
    all reports waiting for a phone call (after customer confirming).
    @para: request is a HTTP request
    @return: a HttpResponse of rendered template with a list of reports.
    '''
    reports = []
    rawReports = REPORT.objects.filter(REPO_STATUS=2)
    for report in rawReports:
        confirmation = CONFIRMATION_DETAIL.objects.get(REPO_ID=report.id)
        rightBag = report.REPO_WAREHOUSE_BAG_ID
        bagCount = 0
        contentCount = 0
        if confirmation.CONFRIM_BAG_ID == rightBag:
            bagCount = 1
        for content in BAGGAGE_CONTENT_IMAGE.objects.filter(CONTENT_WAREHOUSE_BAG_ID=rightBag.id):
            if confirmation.CONFRIM_CONTENT_ID1.id == content.id or confirmation.CONFRIM_CONTENT_ID2.id == content.id:
                contentCount += 1
        reports.append({
            "reportId" : report.id,
            "bagImage" : "../../../static/uploads/" + str(report.REPO_BAG_IMG_ID.CUST_IMG),
            "date" : report.REPO_DATE,
            "rightBagNum" : bagCount,
            "rightContentNum" : contentCount,
            "email" : confirmation.CUST_EMAIL,
            "phone" : confirmation.CUST_PHONE,
            "cofirmationDate" : confirmation.CONFIRMATION_DATE
        })
    print(reports)
    template = loader.get_template('Baggage_Recovery_App/wh-check-resolved-report/all-resolved-reports.html')
    return HttpResponse(template.render({"reports" : reports}, request))

#===============================================================================
# functionality for warehouse side
def saveBagAppearance(request):
    '''
    Save the new coming bag's image, size, color, brand to the database when the
    warehosue employees register a new bag.
    @para: request is a HTTP request, use POST method to get the details of
           the bag
    @return: redirect to baggage-content.html
    '''
    if request.method == "POST":
        bagid = request.POST.get("currentBagId")
        image = WAREHOUSE_BAGGAGE_IMAGE()
        image.WAREHOUSE_IMG_BAG_ID = WAREHOUSE.objects.get(id=bagid)
        image.WAREHOUSE_IMG = request.FILES.get("bagImage")
        image.save()
        description = WAREHOUSE_BAGGAGE_DESCRIPTION()
        description.BAG_DESC_WAREHOUSE_BAG_ID = WAREHOUSE.objects.get(id=bagid)
        description.BAG_SIZE = request.POST.get("size")
        description.BAG_COLOR = request.POST.get("color")
        description.BAG_BRAND = request.POST.get("brand")
        description.save()
    else:
        return redirect(to='baggage-appearance.html')
    return redirect(to='baggage-content.html')

def saveContentAndDetails(request):
    '''
    Save the new coming bag's content details to the database after the warehouse
    employees complete saving bag appearance.
    @para: request is a HTTP request, use POST method to get the details of
           the content in that bag
    @return: redirect to content-one.html
    '''
    if request.method == "POST":
        bagid = request.POST.get("currentBagId")
        description = WAREHOUSE_BAGGAGE_DESCRIPTION.objects.get(BAG_DESC_WAREHOUSE_BAG_ID=bagid)
        if request.POST.get("item1"):
            description.ITEM1 = True
        if request.POST.get("item2"):
            description.ITEM2 = True
        if request.POST.get("item3"):
            description.ITEM3 = True
        if request.POST.get("item4"):
            description.ITEM4 = True
        if request.POST.get("item5"):
            description.ITEM5 = True
        if request.POST.get("item6"):
            description.ITEM6 = True
        if request.POST.get("item7"):
            description.ITEM7 = True
        if request.POST.get("item8"):
            description.ITEM8 = True
        if request.POST.get("item9"):
            description.ITEM9 = True
        if request.POST.get("item10"):
            description.ITEM10 = True
        description.DETAILS = request.POST.get("details")
        description.save()
    else:
        return redirect(to='baggage_content.html')
    return redirect(to='content-one.html')

def saveContentHelper(request):
    '''
    A helper function that save the bag's content image in warehouse side.
    @para: request is a HTTP request, use POST method to get the bag id and bag image
    '''
    bagid = request.POST.get("currentBagId")
    image = BAGGAGE_CONTENT_IMAGE()
    image.CONTENT_WAREHOUSE_BAG_ID = WAREHOUSE.objects.get(id=bagid)
    image.CONTENT_IMG = request.FILES.get("bagImage")
    image.save()

def saveContentImageOne(request):
    '''
    Save the bag's first content image.
    @para: request is a HTTP request
    @return: redirect to content-two.html
    '''
    if request.method == "POST":
        saveContentHelper(request)
    else:
        return redirect(to='content-one.html')
    return redirect(to='content-two.html')

def saveContentImageTwo(request):
    '''
    Save the bag's second content image.
    @para: request is a HTTP request
    @return: redirect to registration-finished.html
    '''
    if request.method == "POST":
        saveContentHelper(request)
    else:
        return redirect(to='content-two.html')
    return redirect(to='registration-finished.html')

def getMatchResultByBag(request):
    '''
    Find all reports in REPORT that match the given bag and showing the matching
    result in the matching-result-by-bag.html.
    @para: request is a HTTP request, use GET method to get the bag id
    @return: a HttpResponse for a template with a list of potential reports
    '''
    bagid = request.GET.get("currentBagId")
    potentialReports = contentMatchByBag(bagid, THRESHOLD)
    print("content match by bag: ")
    print(potentialReports)
    lost_img = WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG_BAG_ID=bagid).WAREHOUSE_IMG
    finalReports = matching(lost_img.name, potentialReports)
    print("image match by bag: ")
    print(finalReports)
    description = WAREHOUSE_BAGGAGE_DESCRIPTION.objects.get(BAG_DESC_WAREHOUSE_BAG_ID=bagid)
    items = CONTENT_DETAIL.objects.all()
    data = {}
    data["bag"] = {
        "bagid" : bagid,
        "bagImage" : "../../../static/uploads/" + WAREHOUSE_BAGGAGE_IMAGE.objects.get(WAREHOUSE_IMG_BAG_ID=bagid).WAREHOUSE_IMG.name,
        "bagColor" : description.BAG_COLOR,
        "bagSize" : description.BAG_SIZE,
        "bagBrand" : description.BAG_BRAND,
        "ITEM1NAME" : items[0].NAME,
        "ITEM2NAME" : items[1].NAME,
        "ITEM3NAME" : items[2].NAME,
        "ITEM4NAME" : items[3].NAME,
        "ITEM5NAME" : items[4].NAME,
        "ITEM6NAME" : items[5].NAME,
        "ITEM7NAME" : items[6].NAME,
        "ITEM8NAME" : items[7].NAME,
        "ITEM9NAME" : items[8].NAME,
        "ITEM10NAME" : items[9].NAME,
        "ITEM1" : description.ITEM1,
        "ITEM2" : description.ITEM2,
        "ITEM3" : description.ITEM3,
        "ITEM4" : description.ITEM4,
        "ITEM5" : description.ITEM5,
        "ITEM6" : description.ITEM6,
        "ITEM7" : description.ITEM7,
        "ITEM8" : description.ITEM8,
        "ITEM9" : description.ITEM9,
        "ITEM10" : description.ITEM10,
        "details" : description.DETAILS,
    }
    if len(finalReports) != 0:
        data["reports"] = []
        i = 1
        for path in finalReports:
            image = CUSTOMER_BAGGAGE_IMAGE.objects.get(CUST_IMG=path)
            description = REPORT.objects.get(REPO_BAG_IMG_ID=image.id).REPO_BAG_DESC_ID
            report = {
                "reportId" : REPORT.objects.get(REPO_BAG_IMG_ID=image.id).id,
                "bagImage" : "../../../static/uploads/" + image.CUST_IMG.name,
                "bagColor" : description.BAG_COLOR,
                "bagSize" : description.BAG_SIZE,
                "bagBrand" : description.BAG_BRAND,
                "ITEM1" : description.ITEM1,
                "ITEM2" : description.ITEM2,
                "ITEM3" : description.ITEM3,
                "ITEM4" : description.ITEM4,
                "ITEM5" : description.ITEM5,
                "ITEM6" : description.ITEM6,
                "ITEM7" : description.ITEM7,
                "ITEM8" : description.ITEM8,
                "ITEM9" : description.ITEM9,
                "ITEM10" : description.ITEM10,
                "details" : description.DETAILS,
            }
            data["reports"].append(report)
    template = loader.get_template('Baggage_Recovery_App/wh-register-new-bag/matching-result-by-bag.html')
    return HttpResponse(template.render(data, request))

def saveMatchedReport(request):
    '''
    Save the confirmed bag id to the matched report by warehouse employees. Change
    the bag's WAREHOUSE_REPO_STAT to be true meaning warehuose confirmed a right
    match.
    @para: request is a HTTP request, use GET method to get the reportId and bagId
    @return: a JsonResponse with the bagId and reportId
    '''
    reportId = request.GET.get("reportId")
    bagId = request.GET.get("bagId")
    bag = WAREHOUSE.objects.get(id=bagId)
    bag.WAREHOUSE_REPO_STAT = True
    bag.save()
    report = REPORT.objects.get(id=reportId)
    report.REPO_WAREHOUSE_BAG_ID = bag
    report.REPO_STATUS = 1
    report.save()
    return JsonResponse({ "reportSaved" : "true", "bagId" : bagId, "reportId" : reportId })

def closeReport(request):
    '''
    Delete the report from database.
    @para: request is a HTTP request, use GET method to get the reportId
    @return: a JsonResponse
    '''
    #print("Close report mannually!")
    reportId = request.GET.get("reportId")
    if CONFIRMATION_DETAIL.objects.filter(REPO_ID=reportId).exists():
        CONFIRMATION_DETAIL.objects.filter(REPO_ID=reportId).delete()
    potentialBags = REPORT_POTENTIAL_BAG.objects.get(REPORT_ID=reportId)
    potentialBags.delete()
    report = REPORT.objects.get(id=reportId)
    description = report.REPO_BAG_DESC_ID
    description.delete()
    report.delete()
    #print("Success close report.")
    return JsonResponse({})
