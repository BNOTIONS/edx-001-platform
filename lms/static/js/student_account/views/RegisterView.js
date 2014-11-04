var edx = edx || {};

(function($, _, gettext) {
    'use strict';

    edx.student = edx.student || {};
    edx.student.account = edx.student.account || {};

    edx.student.account.RegisterView = edx.student.account.FormView.extend({
        el: '#register-form',

        tpl: '#register-tpl',

        events: {
            'click .js-register': 'submitForm',
            'click .login-provider': 'thirdPartyAuth'
        },

        formType: 'register',

        preRender: function( data ) {
            this.providers = data.thirdPartyAuth.providers || [];
            this.currentProvider = data.thirdPartyAuth.currentProvider || '';
            this.platformName = data.platformName;
        },

        render: function( html ) {
            var fields = html || '';

            $(this.el).html( _.template( this.tpl, {
                // We pass the context object to the template so that
                // we can perform variable interpolation using sprintf
                context: {
                    fields: fields,
                    currentProvider: this.currentProvider,
                    providers: this.providers,
                    platformName: this.platformName
                }
            }));

            this.postRender();

            return this;
        },

        postRender: function() {
            var $container = $(this.el);

            this.$form = $container.find('form');
            this.$errors = $container.find('.submission-error');

            this.listenTo( this.model, 'sync', this.saveSuccess );
        },

        thirdPartyAuth: function( event ) {
            var providerUrl = $(event.target).data('provider-url') || '';

            if (providerUrl) {
                window.location.href = providerUrl;
            } else {
                // TODO -- error handling here
                console.log('No URL available for third party auth provider');
            }
        },

        saveSuccess: function() {
            var enrollment = edx.student.account.EnrollmentInterface,
                redirectUrl = '/dashboard',
                next = null;

            // Check for forwarding url
            if ( !_.isNull( $.url('?next') ) ) {
                next = decodeURIComponent( $.url('?next') );

                if ( !window.isExternal(next) ) {
                    redirectUrl = next;
                }
            }

            // If we need to enroll in a course, mark as enrolled
            if ( $.url('?enrollment_action') === 'enroll' ) {
                enrollment.enroll( decodeURIComponent( $.url('?course_id') ), redirectUrl );
            } else {
                this.redirect(redirectUrl);
            }
        },

        redirect: function( url ) {
            window.location.href = url;
        }
    });
})(jQuery, _, gettext);
