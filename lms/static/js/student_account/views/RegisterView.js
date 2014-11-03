var edx = edx || {};

// (function($, _, URI, gettext) {
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
            // var enrollment = edx.student.account.EnrollmentInterface,
            //     query = new URI(window.location.search),
            //     url = '/dashboard',
            //     query_map = query.search(true),
            //     next = '';

            // // Check for forwarding url
            // if ("next" in query_map) {
            //     next = query_map['next'];

            //     if (!window.isExternal(next)) {
            //         url = next;
            //     }
            // }

            // // If we need to enroll in the course, mark as enrolled
            // if ('enrollment_action' in query_map && query_map['enrollment_action'] === 'enroll'){
            //     enrollment.enroll( query_map['course_id'], url );
            // } else {
            //     this.redirect(url);
            // }
            this.redirect('/dashboard');
        },

        redirect: function( url ) {
            // window.location.href = url;
            return true;
        }
    });

// })(jQuery, _, URI, gettext);
})(jQuery, _, gettext);
