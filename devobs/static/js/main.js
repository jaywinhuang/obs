var accounts = JSON.parse(sessionStorage.accounts);


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
        var stringContent = value['type'] + "  ******" + String(value['accountNumber']).substr(-4)
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


}

function refreshAccountActivities(accountActivities) {

}

$(function () {



});