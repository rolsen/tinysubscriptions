/**
 * Controller for collecting subscription data from the view and posting it.
 */
var description_controller = {

    save_button: '#subscriptions-update-button',

    view_target: '#subscription-update-containter',

    subscription_el: '.list-object',

    name_el: '.list-name',

    is_managed_el: '.list-is-selected',

    description_el: '.list-description',

    update_status_el: '#update-status-container',

    update_message_el: '#update-message',

    select_all_toggle_el: "#is-selected-select-all",

    select_all_text_el: "#select-all-toggle-text",

    next_select_all_state: true,

    UPDATE_SUCCESS: 'Update successful',

    UPDATE_FAILURE: 'Update failed',

    /**
     * Create a closure function that will save the DOM description items.
     */
    create_update_items: function () {
        var self = this;
        return function () {
            var items = $(self.view_target).find(self.subscription_el);
            var update_data = {};
            $.each(items, function (index, item) {
                var name = $(item).find(self.name_el).val();
                var is_selected = $(item).find(self.is_managed_el).is(
                    ':checked'
                );
                var description = $(item).find(self.description_el).val();
                if (is_selected) {
                    update_data[name] = {
                        'description': description
                    };
                }
                else {
                    $(item).find(self.description_el).val("");
                }
            });

            self.post_data(self, update_data);
        }
    },

    /**
     * Post data to the server and notify the user of success/failure.
     * @param {Object} self The description_controller instance representing
     *     the object to update with success/failure.
     * @param {Object} update_data The data to be posted to the server.
     */
    post_data: function (self, update_data) {
        var data = {'descriptions': JSON.stringify(update_data)};
        $.post('', data=data, success=self.create_notify(self.UPDATE_SUCCESS))
            .fail(self.create_notify(self.UPDATE_FAILURE));
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
    create_toggle_all_is_selected: function () {
        var self = this;
        return function () {
            var is_selected_all = $(self.view_target).find(self.is_managed_el);
            is_selected_all.prop('checked', self.next_select_all_state);
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
        $(this.save_button).on('click', this.create_update_items());
        $(this.select_all_toggle_el).on(
            'change',
            this.create_toggle_all_is_selected()
        );
    }
};

$(function() {
    description_controller.update_select_all_text(this);
    description_controller.listen();
});