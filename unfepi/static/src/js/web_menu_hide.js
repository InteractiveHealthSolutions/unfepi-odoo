openerp.web_module = function (instance) {
    instance.web.client_actions.add('web_module.action', 'instance.odoo_web_module');
    instance.odoo_web_module = instance.web.Widget.extend({
        'template': 'odoo_web_module',
         events: {
             'click .o_hr_attendance_sign_in_out_icon': 'button_click',
         },
   button_click: function(){
    alert("Button Clicked!");
   },
   text_keypress: function(){
    alert("Entered Key in Text!");
   }

    });
 };
