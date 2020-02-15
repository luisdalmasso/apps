odoo.define('odoo_auto_register.registrarse', function (require) {
    "use strict";
    
    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var core = require('web.core');
    //var rpc = require('web.rpc');
    //var model = require('web.Model');
    //var users = new  model('res.users');

    if (!$('.register-container').length) {
        return $.Deferred().reject("DOM doesn't contain '.register-container'");
    }

  
    $('input[name="email"]').change(function () {
        var input = $(this);
        if (validarEmail(input.val()) != true)
        {
            input.parent().parent().addClass('has-error');
            input.parent().find('.help-block').removeClass('hidden'); 
        }else{
            input.parent().parent().removeClass('has-error');
            input.parent().find('.help-block').addClass('hidden');
        }
    });


    $('input[name="email2"]').change(function () {
        var input = $(this);
        if (input.val() != $('input[name="email"]').val()) {
            input.parent().parent().addClass('has-error');
            input.parent().find('.help-block').removeClass('hidden');
        }
        else {
            input.parent().find('.help-block').addClass('hidden');
            input.parent().parent().removeClass('has-error');
        }
    });

    $('input, select').change(function () {
        
        if (_.all($('input, select'), function (item) {
            var value = $(item)[0].type == 'select-one' ? $(item).children('option:selected').val() : $(item).val();
            return value != '';
        }) && !$('input[name="email2"]').parent().parent().hasClass('has-error')) {
            $('#submit').removeAttr('disabled');
        }
        //else {
            //$('#submit').attr('disabled', '');
        //}
    });


    function validarEmail(valor) {
        
        if (/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(valor)){
            return true
        } 
        return false
    }



});