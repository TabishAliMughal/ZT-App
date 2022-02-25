from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    using = 'blog'
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
    def get_queryset(self, request):
        return super(BlogAdmin, self).get_queryset(request).using(self.using)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(BlogAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super(BlogAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
blogsite = admin.AdminSite('blogsite')

class ShopAdmin(admin.ModelAdmin):
    using = 'shop'
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
    def get_queryset(self, request):
        return super(ShopAdmin, self).get_queryset(request).using(self.using)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(ShopAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super(ShopAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
shopsite = admin.AdminSite('shopsite')

class MatrinomialAdmin(admin.ModelAdmin):
    using = 'matrinomial'
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)
    def delete_model(self, request, obj):
        obj.delete(using=self.using)
    def get_queryset(self, request):
        return super(MatrinomialAdmin, self).get_queryset(request).using(self.using)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(MatrinomialAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super(MatrinomialAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
matrinomialsite = admin.AdminSite('matrinomialsite')