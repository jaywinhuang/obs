// var accounts = JSON.parse(sessionStorage.accounts);


//Refresh accounts from server, save it to "sessionStorage.accounts"
function refreshAccounts() {
    $.ajax({
        type: "GET",
        url: "/api/user/accounts",
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                sessionStorage.accounts = JSON.stringify(data.data);
            } else {
                alert(data.msg);
            }
        }
    });
    console.log(sessionStorage.accounts);
}

// Fill select options with account numbers
function fillSelectAccounts(id) {
    $.each(JSON.parse(sessionStorage.accounts), function (index, value) {
        var stringContent = value['type'] + "  ***" + String(value['accountNumber']).substr(-4) + " | " + accounting.formatMoney(value['balance'])
        $("#" + id).append("<option value=" + value['accountNumber'] + ">" + stringContent + "</option>");
        console.log("<option>" + value['accountNumber'] + "</option>");
    })
}

// Refresh user profile
function refreshProfile() {
    $.ajax({
        type: "GET",
        url: "/api/user/profile",
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                sessionStorage.profile = JSON.stringify(data.data);
            } else {
                alert(data.msg);
            }
        }
    });
    console.log(sessionStorage.profile);
}

function updateTransactionHistory() {
    $.ajax({
        type: "POST",
        url: "/api/user/account-activities",
        data: {"accountNumber": $("#select-account :selected").val()},
        dataType: "json",
        success: function (d) {
            $("#history-table").html('');
            $.each(d.data, function (index, value) {
                renderTransactionHistory(JSON.stringify(value));
            });
            $('#transaction-history-table').DataTable();
        }
    });
}


$(function () {
    $.ajax({
        type: "GET",
        url: "/api/user/profile",
        dataType: "json",
        success: function (data) {
            if (data.status == 0) {
                sessionStorage.profile = JSON.stringify(data.data);
            } else {
                alert(data.msg);
            }
        }
    }).done(function () {
        fillProfile(JSON.parse(sessionStorage.profile));
    });

    $("#profile-form").submit(function (event) {
        event.preventDefault();
        var form_data = $(this).serialize();

        $.ajax({
            url: "/api/user/profile",
            type: "POST",
            data: form_data,
            dataType: "json",
            success: function (d) {
                if (d.status == 0) {
                    $("#alertMessage").html("Update profile success.")
                } else {
                    $("#alertMessage").html(d.message)
                    console.log(d.message)
                }
                $("#alertBlock").show()
            }
        });
    });
});

function fillProfile(json_data) {
    $("#profile-form input[name=username]").val(json_data["username"])
    $("#profile-form input[name=ssn]").val(json_data["ssn"])
    $("#profile-form input[name=firstname]").val(json_data["firstname"])
    $("#profile-form input[name=lastname]").val(json_data["lastname"])
    $("#profile-form input[name=email]").val(json_data["email"])
    $("#profile-form input[name=phone]").val(json_data["phone"])
    $("#profile-form input[name=address]").val(json_data["address"])
    $("#profile-form input[name=securityQuestion]").val(json_data["securityQuestion"])
    $("#profile-form input[name=securityAnswer]").val(json_data["securityAnswer"])
}