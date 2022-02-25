from django import forms
from .models import Product , Shops , Units , ProductImages , ProductVideos
from mapwidgets.widgets import GooglePointFieldWidget
from static.mapsettings import CUSTOM_MAP_SETTINGS



class ManageProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'shop',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'available',
            'unit',
            'condition',
        ]

class ManageShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shops
        fields = [
            'name' ,
            'user' ,
            'address' ,
            'active' ,
        ]

class ManageUnitCreateForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = [
            'name' ,
        ]

class ManageProductImageCreateForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = [
            'product',
            'image',
        ]    
    
class ManageProductVideoCreateForm(forms.ModelForm):
    class Meta:
        model = ProductVideos
        fields = [
            'product',
            'video',
        ]    

    