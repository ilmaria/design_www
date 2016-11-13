$(document).ready(function() {
    $('#datePicker')
        .datepicker({
            autoclose: true,
            format: 'dd/mm/yyyy',
            todayBtn: 'linked'
        })

    $('#logtimeForm').formValidation({
        framework: 'bootstrap',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            date: {
                validators: {
                    notEmpty: {
                        message: 'The date is required'
                    },
                    date: {
                        format: 'DD/MM/YYYY',
                        message: 'The date is not a valid'
                    }
                }
            }
        }
    });
});
