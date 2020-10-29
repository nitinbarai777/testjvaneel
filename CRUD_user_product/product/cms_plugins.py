from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from product.models import Hello as HelloPluginModel
from django.utils.translation import ugettext_lazy as _
from product.models import *


from product.models import Hello

class HelloPlugin(CMSPluginBase):
    model = Hello
    name = _("Hello Plugin")
    render_template = "product/hello_plugin.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


class Menu_Item_Plugin(CMSPluginBase):
    model = Menu_Item
    name = "Menu Item"
    render_template = "product/menu_item.html"

    def render(self, context, instance, placeholder):
        context.update({
            'name': instance.name,
            'image': instance.image,
            'price': instance.price,
            'description': instance.description,
            'url': instance.url
        })
        return context

class EmployeePlugin(CMSPluginBase):
    model = Employee
    name = "Employee"
    render_template = "product/employee_data.html"

    def render(self, context, instance, placeholder):
        context.update({
            'fname': instance.fname,
            'lname': instance.lname,
            'description': instance.description,
            'city': instance.city,

        })
        return context



class UserCustomPlugin(CMSPluginBase):
    model = User_Custom_Plugin
    name = _('User_Custom_Plugin')
    render_template = "product/hello_plugin.html"

    fieldsets = (
        (None, {
            'fields': (
                'items_per_page',
            )
        }),
    )
    def render(self, context, instance, placeholder):
        users = User.objects.all()[:instance.items_per_page]
        context['users'] = users
        context = super(UserCustomPlugin, self).render(context, instance, placeholder)
        return context

plugin_pool.register_plugin(HelloPlugin)
plugin_pool.register_plugin(Menu_Item_Plugin)
plugin_pool.register_plugin(EmployeePlugin)
plugin_pool.register_plugin(UserCustomPlugin)
