


$("form").on('submit', function(e){
    e.preventDefault()
    const $rows = $("tr")
    $rows.hide()
    const input = $("input").val()
    if($(`#${input}`)){
        $(`#${input}`).show()
    }
    else{
        $rows.show()
    }
})