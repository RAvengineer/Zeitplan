// Datepicker's script
$('#end_date').datepicker({
    uiLibrary: 'bootstrap4'
});
$('#start_date').datepicker({
    uiLibrary: 'bootstrap4'
});

// Event Colors available in Google Calendars
var eventColors = ['#a4bdfc','#7ae7bf','#dbadff','#ff887c','#fbd75b','#ffb878','#46d6db','#e1e1e1','#5484ed','#51b749','#dc2127',]

function main(){
    
    // Default fields
    $('#recurringEndDate').attr("hidden",'');
    $('#end_date').attr("disabled",'');

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

    // Toggle end_date field with respect to the status of the switch
    $('#recurringEvent').on("click",function(){
        if($(this).is(':checked')){
            $('#recurringEndDate').removeAttr("hidden");
            $('#end_date').removeAttr("disabled");
        }else{
            $('#recurringEndDate').attr("hidden",'');
            $('#end_date').attr("disabled",'');
        }
    });

    // Show spinner and disable the submit button, when submitting the form
    $('#getDataForm').submit(function () {
        $('#spinner').removeAttr('hidden');
        $('#addEventsButtonText').text('Adding...');
        $('#addEventsButton').attr('disabled', '');
    });
}

main();