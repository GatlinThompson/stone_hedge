from . import views
from django.urls import path

app_name = 'partsdatabase'
urlpatterns = [
    path('', views.parts_db, name='parts_db'),
    # Hardware CRUD
    path('hardware/', views.hardware, name='hardware'),
    path('hardware/add', views.create_hardware, name='create_hardware'),
    path('hardware/update/<int:hardware_id>', views.update_hardware, name='update_hardware'),
    path('hardware/delete/<int:hardware_id>', views.delete_hardware, name='delete_hardware'),
    # Part CRUD
    path('part/', views.part, name='part'),
    path('part/add', views.create_part, name='create_part'),
    path('part/update/<int:part_id>', views.update_part, name='update_part'),
    path('part/delete/<int:part_id>', views.delete_part, name='delete_part'),
    # Hardware Kit CRUD
    path('hardwarekit/', views.hardwarekit, name='hardwarekit'),
    path('hardwarekit/add', views.create_hardwarekit, name='create_harwarekit'),
    path('hardwarekit/<int:hardwarekit_id>', views.details_hardwarekit, name='details_hardwarekit'),
    path('hardwarekit/<int:hardwarekit_id>/update/', views.update_hardwarekit, name='update_hardwarekit'),
    path('hardwarekit/<int:hardwarekit_id>/delete/', views.delete_hardwarekit, name='delete_hardwarekit'),
    # HK Part and Hardware CRUD
    path('hardwarekit/<int:hardwarekit_id>/part_hk_form_submit/',
         views.part_hk_form_submit, name='part_hk_form_submit'),
    path('hardwarekit/<int:hardwarekit_id>/hardware_hk_form_submit/',
         views.hardware_hk_form_submit, name='hardware_hk_form_submit'),
    path('hardwarekit/<int:hardwarekit_id>/hardware_hk_delete/<int:hardware_id>',
         views.hardware_hk_form_delete, name='hardware_hk_form_delete'),
    path('hardwarekit/<int:hardwarekit_id>/hardware_hk_edit/<int:hardware_id>',
         views.hardware_hk_form_edit, name='hardware_hk_form_edit'),
    path('hardwarekit/<int:hardwarekit_id>/part_hk_delete/<int:part_id>',
         views.part_hk_form_delete, name='part_hk_form_delete'),
    path('hardwarekit/<int:hardwarekit_id>/part_hk_edit/<int:part_id>',
         views.part_hk_form_edit, name='part_hk_form_edit'),
    # Kit CRUD
    path('kit/', views.kit, name='kit'),
    path('kit/add', views.create_kit, name='create_kit'),
    path('kit/<int:kit_id>', views.details_kit, name='details_kit'),
    path('kit/<int:kit_id>/delete', views.delete_kit, name='delete_kit'),
    path('kit/<int:kit_id>/update', views.update_kit, name='update_kit'),
    # Kit HK CRUD
    path('kit/<int:kit_id>/kit_hk_form_submit/', views.kit_hk_form_submit, name='kit_hk_form_submit'),
    path('kit/<int:kit_id>/kit_hk_edit/<int:hk_id>', views.kit_hk_edit, name='kit_hk_edit'),
    path('kit/<int:kit_id>/kit_hk_delete/<int:hk_id>', views.kit_hk_delete, name='kit_hk_delete'),
    # Kit Hardware CRUD
    path('kit/<int:kit_id>/kit_hw_form_submit/', views.kit_hw_form_submit, name='kit_hw_form_submit'),
    path('kit/<int:kit_id>/kit_hw_delete/<int:hw_id>', views.kit_hw_delete, name='kit_hw_delete'),
    path('kit/<int:kit_id>/kit_hw_edit/<int:hw_id>', views.kit_hw_edit, name='kit_hw_edit'),
    # Kit Part CRUD
    path('kit/<int:kit_id>/kit_part_form_submit/', views.kit_part_form_submit, name='kit_part_form_submit'),
    path('kit/<int:kit_id>/kit_part_delete/<int:part_id>', views.kit_part_delete, name='kit_part_delete'),
    path('kit/<int:kit_id>/kit_part_edit/<int:part_id>', views.kit_part_edit, name='kit_part_edit'),


]
