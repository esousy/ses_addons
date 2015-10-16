openerp.ses_client_password = function(instance) {
	var _t = instance.web._t,
	   _lt = instance.web._lt;
	var QWeb = instance.web.qweb;

	instance.web.form.PasswordReveal = instance.web.form.FieldChar.extend({
	    template: 'PasswordReveal',
	    initialize_content: function() {
	        this._super();
	        this.$button = this.$el.find('.odoo-password-reveal button');
	        this.$button.click(this.on_button_clicked);
	    },
	    render_value: function() {
	        var show_value = this.format_value(this.get('value'), '');
	        if (!this.get("effective_readonly")) {
	            this.$el.find('input').val(show_value);
	        } else {
	        	this.password = true;
	            show_value = new Array(show_value.length + 1).join('*');
	            this.$(".oe_form_char_content").text(show_value);
	        }
	    },
	    on_button_clicked: function(ev) {
	        this.password = !this.password; 
	        if (!this.password) {
	        	this.$('.odoo-password-reveal input').replaceWith(this.$('.odoo-password-reveal input').clone().attr('type', 'text'));
	        	this.$('.odoo-password-reveal button i').removeClass().addClass('fa fa-eye-slash');
	        } else {
	        	this.$('.odoo-password-reveal input').replaceWith(this.$('.odoo-password-reveal input').clone().attr('type', 'password'));
	        	this.$('.odoo-password-reveal button i').removeClass().addClass('fa fa-eye');
	        }
	    },
	});

	instance.web.form.widgets = instance.web.form.widgets.extend({
	    'password_reveal': 'instance.web.form.PasswordReveal',
	});

};
