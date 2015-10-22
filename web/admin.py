from django.contrib import admin

from . models import Member_Farmer,Member_Farmer_meta,Member_Seed,Member_Seed_meta,Produce,Produce_meta,shopping_cart,Member_Farmer_token,Member_Seed_token
# Register your models here.
admin.site.register(Member_Farmer)
admin.site.register(Member_Farmer_meta)
admin.site.register(Member_Seed)
admin.site.register(Member_Seed_meta)
admin.site.register(Produce)
admin.site.register(Produce_meta)
admin.site.register(shopping_cart)
admin.site.register(Member_Seed_token)
admin.site.register(Member_Farmer_token)


