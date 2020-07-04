$('span.dot').mouseover(function () {
    $(".room-info-panel").hide();
    $("#" + this.id + "-info").show();
});

$("#accordion").accordion({
    collapsible: true
});