
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
          $("#"+id).append("<option>"+value['accountNumber']+"</option>");
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