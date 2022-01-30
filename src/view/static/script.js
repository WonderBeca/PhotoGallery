function openRegister() {
    // Open register form
    $('#SelectButton').hide();
    $('#LoginForm').hide();  
    $('#AdminForm').hide();  
    $('#RegisterForm').show();
    
    $('#R-Username').val('');
    $('#R-Email').val('');
    $('#R-Password').val('');
    $('#AcceptRelogin').prop('checked', false);
}

function openAdmin() {
    // Open register form
    $('#SelectButton').hide();
    $('#LoginForm').hide();  
    $('#AdminForm').show();  
    $('#RegisterForm').hide();
    
    $('#RA-Username').val('');
    $('#RA-Email').val('');
    $('#RA-Password').val('');
    $('#AcceptRelogin').prop('checked', false);
}

function openLogin() {
    // Open login form
    $('#SelectButton').hide();
    $('#RegisterForm').hide();  
    $('#AdminForm').hide();  
    $('#LoginForm').show();
    
    $('#Username').val('');
    $('#Email').val('');
    $('#Password').val('');
    $('#AcceptNewsletter').prop('checked', false);
    $('#AcceptPolicy').prop('checked', false);
}

function backBegin() {
    $('#SelectButton').show();
    $('#RegisterForm').hide();
    $('#AdminForm').hide();
    $('#LoginForm').hide();
    
    $('#Username').val('');
    $('#Email').val('');
    $('#Password').val('');
    $('#AcceptNewsletter').prop('checked', false);
    $('#AcceptPolicy').prop('checked', false);
    $('#L-Username').val('');
    $('#L-Email').val('');
    $('#L-Password').val('');
    $('#AcceptRelogin').prop('checked', false);
}

function postRegister(role) {
    if (role == 'admin'){
        var data = {
            'username' : $('#RA-Username').val(),
            'login' : $('#RA-Email').val(),
            'password' : $('#RA-Password').val(),
            'role': role }
    } else {
        var data = {
            'username' : $('#R-Username').val(),
            'login' : $('#R-Email').val(),
            'password' : $('#R-Password').val(),
            'role': role }
    }
    
    $.ajax({
        type: "POST",
        url: '/register',
        data: JSON.stringify(data),
        success: function (data) {
            if (data.redirect) {
                window.location.href = data.redirect
            }
        },
        contentType: "application/json; charset=utf-8"
      });
}

function postLogin() {
    var data = {
        'login' : $('#L-Email').val(),
        'password' : $('#L-Password').val()
    }
    
    $.ajax({
        type: "POST",
        url: '/login',
        data: JSON.stringify(data),
        success: function (data) {
            if (data.redirect) {
                window.location.href = data.redirect
            }
        },
        contentType: "application/json; charset=utf-8"
      });
}