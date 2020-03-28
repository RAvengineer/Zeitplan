// Datepicker's script
$('#end_date').datepicker({
    uiLibrary: 'bootstrap4'
});
$('#start_date').datepicker({
    uiLibrary: 'bootstrap4'
});

// Event Colors available in Google Calendars
var eventColors = ['#a4bdfc','#7ae7bf','#dbadff','#ff887c','#fbd75b','#ffb878','#46d6db','#e1e1e1','#5484ed','#51b749','#dc2127',]

// Add background colors for <td> color circles
for (let i = 1; i < 12; i++) {
    var cid = "#c"+i;
    $(cid).css("background-color",eventColors[i-1]);
}

// Add click listeners for <td> color circles
for (let i = 1; i < 12; i++) {
    var cid = "#c"+i;
    $(cid).on("click",function(){
        $('#eventColorDummy').css("background-color",eventColors[i-1]);
        $("#eventColor").attr("value",i);
    });
}