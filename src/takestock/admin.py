from django.contrib import admin

from takestock.models import Club, Member, MemberInstance, Stock, StockInstance

class StockAdmin(admin.ModelAdmin):
    pass

class StockInstanceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Information',       {'fields': ['owner', 'stock']}),
        ('Numerical Information',   {'fields': ['shares']}),
        ('Purchase Information',    {'fields': ['purchase_date', 'purchase_price']}),
        ('Closed Information',      {'fields': ['is_open', 'sell_date', 'sell_price'], 'classes': ['collapse']}),
    ]
    readonly_fields = ['current_price']
    
class StockInstanceInline(admin.TabularInline):
    model = StockInstance
    extra = 1
    
class MemberAdmin(admin.ModelAdmin):
    pass

class MemberInstanceAdmin(admin.ModelAdmin):
    pass
    
class MemberInstanceInline(admin.TabularInline):
    model = MemberInstance
    extra = 1

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'current_value')
    fieldsets = [
        ('Basic Information',         {'fields': ['name']}),
        ('Monetary Information',         {'fields': ['cash']}),
    ]
    inlines=[StockInstanceInline, MemberInstanceInline]

admin.site.register(Stock, StockAdmin)
admin.site.register(StockInstance, StockInstanceAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberInstance, MemberInstanceAdmin)
admin.site.register(Club, ClubAdmin)
