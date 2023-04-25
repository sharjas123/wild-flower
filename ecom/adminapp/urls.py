from .import views
from django.urls import path

urlpatterns = [
    
    path('',views.adminlogin,name="adminlogin"),
    # path('dash_page/',views.dashboard,name="dashboard"),    
    path('logout_admin/',views.logout_admin, name='logout_admin'),
    path('admindash',views.dashboard, name="dashboard"),
    path('viewcategory/',views.viewcategory, name="viewcategory"),
    path('addcategory/',views.addcategory, name="addcategory"),
    path('editcategory/<int:pid>/',views.editcategory, name="editcategory"),
    path('deletecategory/<int:pid>/',views.delete_category,name="deletecategory"),
    
    
    path('addproduct/',views.addproduct,name="addproduct"),
    path('viewproduct/',views.viewproduct,name="viewproduct"),
    path('editproduct/<int:pid>/',views.editproduct,name="editproduct"),
    path('delete-image/<int:iid>/', views.delete_image, name='deleteimage'),
    path('deleteproduct/<int:pid>/',views.deleteproduct,name="deleteproduct"),
    
    
    path('manageuser',views.manageuser,name="manageuser"),
    path('blockuser/<int:id>/',views.blockuser,name="blockuser"),
    
    path('manageorder/',views.manage_order,name="manageorder"),
    path('updateorder/<int:id>/',views.update_order,name='updateorder'),

    path('banner/',views.add_banner,name="banner"),
    path('salesreport',views.sales_report,name="salesreport"),

]