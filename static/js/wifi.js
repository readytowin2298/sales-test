const $wifiOptions = [
    $("#need_router_ship").parent(),
    $("#wifi_ssid").parent(),
    $("#wifi_pw").parent()
    // $("label[for=need_router_ship]"),
    // $("label[for=wifi_ssid]"),
    // $("label[for=wifi_pw")
]

for(let option of $wifiOptions){
    option.hide()
}

$("#cx_wants_router").on('click', function(){
    if ($("#cx_wants_router").val() == 1){
        for(let option of $wifiOptions){
            option.show()
        }  
    }
})