from django.urls import path,include
from .views import ( sellerUserView,
                    BuyerUserView,
                    DonarUserView,
                    UpdateProfileView,
                    sellerUpdateView,
                    BuyerUpdateView,
                    DonarUpdateView,
                    adminProfileView,
                    UserCrateView,
                    ProductView,
                    ProductUpdateView,
                    sellerUploadView,
                    BoughtView,
                    BookListView,
                    AddProductsView,
                    ExportCSVView,
                    ReviewProductView,
                    SalesView)


urlpatterns = [
    
    #Admin profile and update
    path('profile/',adminProfileView.as_view()),
    path('user-create/',UserCrateView.as_view()),
    
    #sellerProfileAPI
    path('seller-profile/',sellerUserView.as_view(),name='sellerview'),
    path('seller-profile/<int:pk>/',sellerUpdateView.as_view()),
    path('seller-profile/uploads/',sellerUploadView.as_view(),name='selleruploads'),
    path('seller-profile/uploads/<int:pk>/',ReviewProductView.as_view(),name='Review'),
    
    
    #BuyerProfileAPI
    path('buyer-profile/',BuyerUserView.as_view(),name='BuyerView'),
    path('buyer-profile/<int:pk>/',BuyerUpdateView.as_view(),name='BuyerUpdateView'),
    path('buyer-profile/boughts/',BoughtView.as_view(),name='boughtView'),
    
    #DonarProfileAPI
    path('donar-profile/',DonarUserView.as_view(),name='sellerview'),
    path('donar-profile/<int:pk>/',DonarUpdateView.as_view(),name='sellerview'),
    
    #productAPI
    path('products/',ProductView.as_view(),name='productview'),
    path('products/<int:pk>/',ProductUpdateView.as_view(),name='productupdate'),
    path('products/add/',AddProductsView.as_view(),name='AddProducts'),
    path('products-list/',BookListView.as_view(),name='Product List'),
    
    #path('product/inventry/',ProductInventry.as_view()),
    # path('products/rating/<int:pk>/')
    path('csv/',ExportCSVView.as_view()),
    
    #SalesAPI
    path('sales/',SalesView.as_view()),
    
    
    
    
    
    
]
