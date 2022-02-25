from import_export.admin import ImportExportModelAdmin
from .models import ShopkeperPayment , ShopAdminShare , DeliveryPersonPayment , DeliveryAdminShare , PaymentProof
from MyApp.admin import shopsite

shopsite.register(ShopkeperPayment)
shopsite.register(ShopAdminShare)
shopsite.register(DeliveryPersonPayment)
shopsite.register(DeliveryAdminShare)
shopsite.register(PaymentProof)