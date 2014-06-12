/**
 * Controller for collecting subscription data from the view and posting it.
 */
var subscription_controller = {

    save_button: '#subscriptions-update-button',

    view_target: '#subscription-update-containter',

    subscription_el: '.list-object',

    name_el: '.list-name',

    is_subscribed_el: '.list-is-subscribed',

    update_status_el: '#update-status-container',

    update_message_el: '#update-message',

    select_all_toggle_el: "#is-subscribed-select-all",

    select_all_text_el: "#select-all-toggle-text",

    next_select_all_state: true,

    /**
     * Create a closure function that will save the DOM subscriptions.
     */
    create_update_subscriptions: function () {
        var self = this;
        return function () {
            var subscriptions = $(self.view_target).find(self.subscription_el);
            var update_data = {};
            $.each(subscriptions, function (index, subscription) {
                var name = $(subscription).find(self.name_el).val();
                var is_subscribed = $(subscription).find(self.is_subscribed_el).is(':checked');
                update_data[name] = {'subscribed': is_subscribed};
            });

            self.post_data(self, update_data);
        }
    },

    /**
     * Post data to the server and notify the user of success/failure.
     * @param {obj} subscription_data The data to be posted to the server.
     */
    post_data: function (self, subscription_data) {
        var data = {'subscriptions': JSON.stringify(subscription_data)};
        $.post('', data=data, success=self.create_notify('Subscription update successful'))
            .fail(self.create_notify('Subscription update failed.'))
            .fail(function(xhr, textStatus, errorThrown) {
                console.log('xhr.responseText');
                console.log(xhr.responseText);
            });
    },

    /**
     * Create a closure function that will notify the user of a message.
     * @param {string} message The message to be presented to the user.
     */
    create_notify: function (message) {
        var self = this;
        return function () {
            $(self.update_message_el).text(message);
            $(self.update_status_el)
                .stop(true) // Clear any queued previous animation
                .hide()     // set up for fadeTo
                .fadeTo('fast', 1)
                .delay(1000)
                .fadeTo(2000, 0.5)
            ;
        };
    },

    /**
     * Create a closure function that will select all or deselect all subscriptions.
     */
    create_toggle_all_is_subscribed: function () {
        var self = this;
        return function () {
            var is_subscribed_all = $(self.view_target).find(self.is_subscribed_el);
            is_subscribed_all.prop('checked', self.next_select_all_state);
            self.next_select_all_state = !self.next_select_all_state;
            self.update_select_all_text(self);
        };
    },

    update_select_all_text: function (self) {
        if (self.next_select_all_state) {
            $(self.select_all_text_el).html('Select All');
        }
        else {
            $(self.select_all_text_el).html('Deselect All');
        }
    },

    listen: function () {
        $(this.save_button).on('click', this.create_update_subscriptions());
        $(this.select_all_toggle_el).on('change', this.create_toggle_all_is_subscribed());
    }
};

$(function() {
    subscription_controller.update_select_all_text(this);
    subscription_controller.listen();
});