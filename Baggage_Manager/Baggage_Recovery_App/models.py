from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_delete

class CUSTOMER(models.Model):
    #CNF_NUM = models.IntegerField(unique=True)  # customer confirmation number
    MILEAGEPLS_NUM = models.CharField(primary_key=True,unique=True, max_length=8)  # customer mileage plus number
    FIRST_NAME = models.CharField(max_length=30)  # Customer first name
    MIDDLE_NAME = models.CharField(max_length=30, blank = True, null = True)  # Customer middle name
    LAST_NAME = models.CharField(max_length=30)  # Customer last name

    def __str__(self):
        return str(self.MILEAGEPLS_NUM) + ' - ' + self.FIRST_NAME + ' - ' + self.LAST_NAME


class WAREHOUSE(models.Model):
    #WAREHOUSE_BAG_ID = models.IntegerField(primary_key=True)  # warehouse bagsgage id
    WAREHOUSE_REPO_STAT = models.BooleanField(default=False)  # Report status for warehouse bag

    def __unicode__(self):
        return u'%s' % (self.name)

class CONTENT_DETAIL(models.Model):
    ITEM_NUM = models.IntegerField(primary_key=True) # content item number
    NAME = models.CharField(max_length=50) # item name

    def __unicode__(self):
        return u'%s' % (self.name)

class CUSTOMER_BAGGAGE_IMAGE(models.Model):
    #CUST_IMG_CNF_NUM = models.ForeignKey(CUSTOMER, related_name='BAG_IMG_CNF_NUM',
    #                                     on_delete=models.CASCADE)  # customer confirmation number
    CUST_IMG_MILEAGEPLS_NUM = models.ForeignKey(CUSTOMER, related_name='BAG_IMG_MILEAGE_NUM',
                                                on_delete=models.CASCADE)  # customer mileage number
    CUST_IMG = models.ImageField(upload_to='customer_img')  # customer baggage image address
    BAG_NAME = models.CharField(max_length=20) # customer baggage name
    ADD_DATE = models.DateTimeField(default=timezone.now) # date that add this baggage

    def __unicode__(self):
        return u'%s' % (self.name)

@receiver(pre_delete, sender=CUSTOMER_BAGGAGE_IMAGE)
def delete_customer_image(sender, instance, **kwargs):
    instance.CUST_IMG.delete(save=False)
    print ("Delete old customer image.")

class CUSTOMER_BAGGAGE_DESCRIPTION(models.Model):
    #BAG_ID = models.IntegerField(primary_key=True, unique=True)  # Baggage id
    #BAG_CNF_NUM = models.ForeignKey(CUSTOMER, related_name='BAG_DESC_CNF_NUM',
    #                                on_delete=models.CASCADE)  # customer confirmation number
    # BAG_MILEAGEPLS_NUM = models.ForeignKey(CUSTOMER, related_name='BAG_DESC_MILEAGEPLS_NUM',
    #                                             on_delete=models.CASCADE)  # customer mileage number
    BAG_COLOR = models.CharField(max_length=10)  # bag's color
    BAG_SIZE = models.CharField(max_length=20)  # bag's size
    BAG_BRAND = models.CharField(max_length=20)  # bag's brand
    ITEM1 = models.BooleanField(default=False) # key identifying item in the bag
    ITEM2 = models.BooleanField(default=False)
    ITEM3 = models.BooleanField(default=False)
    ITEM4 = models.BooleanField(default=False)
    ITEM5 = models.BooleanField(default=False)
    ITEM6 = models.BooleanField(default=False)
    ITEM7 = models.BooleanField(default=False)
    ITEM8 = models.BooleanField(default=False)
    ITEM9 = models.BooleanField(default=False)
    ITEM10 = models.BooleanField(default=False)
    DETAILS = models.CharField(max_length=1000, null=True) # details provided by customer

    def __unicode__(self):
        return u'%s' % (self.name)

class WAREHOUSE_BAGGAGE_DESCRIPTION(models.Model):
    #BAG_ID = models.IntegerField(primary_key=True, unique=True)  # Baggage id
    BAG_DESC_WAREHOUSE_BAG_ID = models.ForeignKey(WAREHOUSE, default=None,
                                                  related_name='BAG_DESC_WAREHOUSE_BAG_ID',
                                                  on_delete=models.CASCADE)  # bag's warehouse id
    BAG_COLOR = models.CharField(max_length=10)  # bag's color
    BAG_SIZE = models.IntegerField()  # bag's size
    BAG_BRAND = models.CharField(max_length=20)  # bag's brand
    ITEM1 = models.BooleanField(default=False) # key identifying item in the bag
    ITEM2 = models.BooleanField(default=False)
    ITEM3 = models.BooleanField(default=False)
    ITEM4 = models.BooleanField(default=False)
    ITEM5 = models.BooleanField(default=False)
    ITEM6 = models.BooleanField(default=False)
    ITEM7 = models.BooleanField(default=False)
    ITEM8 = models.BooleanField(default=False)
    ITEM9 = models.BooleanField(default=False)
    ITEM10 = models.BooleanField(default=False)
    DETAILS = models.CharField(max_length=1000, null=True) # details provided by warehouse employees

    def __unicode__(self):
        return u'%s' % (self.name)


class REPORT(models.Model):
    #REPO_ID = models.IntegerField(primary_key=True, unique=True)  # report id
    # REPO_CNF_NUM = models.ForeignKey(CUSTOMER, related_name='REPO_CNF_NUM',
    #                                  on_delete=models.CASCADE)  # customer confirmation number
    REPO_MILEAGEPLS_NUM = models.ForeignKey(CUSTOMER, related_name='REPO_MILEAGE_NUM',
                                            on_delete=models.CASCADE)  # customer mileage plus number
    REPO_BAG_IMG_ID = models.ForeignKey(CUSTOMER_BAGGAGE_IMAGE, related_name='REPO_BAG_IMG_ID',
                                on_delete=models.CASCADE, null=True) # baggage image ID
    REPO_BAG_DESC_ID = models.ForeignKey(CUSTOMER_BAGGAGE_DESCRIPTION, related_name='REPO_BAG_DESC_ID',
                                         on_delete=models.CASCADE, null=True)  # Bag description id
    REPO_WAREHOUSE_BAG_ID = models.ForeignKey(WAREHOUSE, related_name='REPO_WAREHOUSE_BAG_ID',
                                              on_delete=models.CASCADE, null=True)  # Warehouse bag id
    CUST_PERM_ADDR = models.CharField(max_length=50)  # customer permanent address
    CUST_TEMP_ADDR = models.CharField(max_length=50)  # customer temporary address
    TEMP_ADDR_VALID_DATE = models.CharField(max_length=50) # temporary address valid date
    REPO_DATE = models.DateTimeField(default=timezone.now)  # Report submit date and time
    # 0 --> no match found yet, 1 --> waiting for customer confirmation, 2 --> waiting for warehouse contact customer
    REPO_STATUS = models.IntegerField(default=0) # Report status,

    def __unicode__(self):
        return u'%s' % (self.name)

class REPORT_POTENTIAL_BAG(models.Model):
    REPORT_ID = models.ForeignKey(REPORT, related_name="REPORT_ID",
                                  on_delete=models.CASCADE, null=True) # related report id
    NUM = models.IntegerField(null=True, default=0) # number of potential baggages found
    BAG_ID1 = models.ForeignKey(WAREHOUSE, related_name="BAG_ID1",
                                on_delete=models.CASCADE, null=True) # potential bag1 from warehouse
    BAG_ID2 = models.ForeignKey(WAREHOUSE, related_name="BAG_ID2",
                                on_delete=models.CASCADE, null=True) # potential bag2 from warehouse
    BAG_ID3 = models.ForeignKey(WAREHOUSE, related_name="BAG_ID3",
                                on_delete=models.CASCADE, null=True) # potential bag3 from warehouse

    def __unicode__(self):
        return u'%s' % (self.name)

class WAREHOUSE_BAGGAGE_IMAGE(models.Model):
    #WAREHOUSE_IMG_ID = models.IntegerField(primary_key=True, unique=True)  # warehouse baggage image id
    WAREHOUSE_IMG_BAG_ID = models.ForeignKey(WAREHOUSE, related_name='WAREHOUSE_IMG_BAG_ID',
                                             on_delete=models.CASCADE)  # warehouse baggage id
    WAREHOUSE_IMG = models.ImageField(upload_to='warehouse_img')  # Warehouse baggage image address

    def __unicode__(self):
        return u'%s' % (self.name)

@receiver(pre_delete, sender=WAREHOUSE_BAGGAGE_IMAGE)
def delete_warehouse_image(sender, instance, **kwargs):
    instance.WAREHOUSE_IMG.delete(save=False)
    print ("Delete old warehouse image.")

class BAGGAGE_CONTENT_IMAGE(models.Model):
    #CONTENT_IMG_ID = models.IntegerField(primary_key=True, unique=True)  # Content image id
    CONTENT_WAREHOUSE_BAG_ID = models.ForeignKey(WAREHOUSE, related_name='CONTENT_WAREHOUSE_BAG_ID',
                                                 on_delete=models.CASCADE)  # warehouse baggage id
    CONTENT_IMG = models.ImageField(upload_to='content_img')  # content image address on disk

    def __unicode__(self):
        return u'%s' % (self.name)

@receiver(pre_delete, sender=BAGGAGE_CONTENT_IMAGE)
def delete_content_image(sender, instance, **kwargs):
    instance.CONTENT_IMG.delete(save=False)
    print ("Delete old warehouse content image.")

class CONFIRMATION_DETAIL(models.Model):
    REPO_ID = models.ForeignKey(REPORT, related_name="REPO_ID", on_delete=models.CASCADE) # related report id
    CONFRIM_BAG_ID = models.ForeignKey(WAREHOUSE, related_name="CONFRIM_BAG_ID"
                                        , on_delete=models.CASCADE) # customer confirmed bag id
    CONFRIM_CONTENT_ID1 = models.ForeignKey(BAGGAGE_CONTENT_IMAGE
                                            , related_name="CONFRIM_CONTENT_ID1"
                                            , on_delete=models.CASCADE) # customer confirmed content1 id
    CONFRIM_CONTENT_ID2 = models.ForeignKey(BAGGAGE_CONTENT_IMAGE
                                            , related_name="CONFRIM_CONTENT_ID2"
                                            , on_delete=models.CASCADE) # customer confirmed content2 id
    CUST_EMAIL = models.CharField(max_length=20, null=True)  # customer email address
    CUST_PHONE = models.CharField(max_length=20, null=True)  # customer phone number
    CONFIRMATION_DATE = models.CharField(max_length=50, null=True) # mannually confirmation date

    def __unicode__(self):
        return u'%s' % (self.name)
