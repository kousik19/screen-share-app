let socket = io.connect('http://localhost:3000');
let isStopped = false
window.onload = function() {
    window. addEventListener("contextmenu", e => e. preventDefault());
    shareScreen()

    socket.on('RenderScreen', function(message){
        if(isStopped) return
        $("#screen").attr("src", "data:image/png;base64," + message);
        setTimeout(function(){
            socket.emit("RequestScreen", $("#appList").val())
        }, 10)
    })

    $("#screen").click(function(e){
        let elemOffset = $(this).offset();
        let elemWidth = $(this).width();
        let elemHeight = $(this).height();

        let factorX = 1942/elemWidth
        let factorY = 1042/elemHeight

        let relX = parseInt((e.pageX - 5 - (elemOffset.left)) * factorX) + 5
        let relY = parseInt((e.pageY - 5 - (elemOffset.top)) * factorY) + 15

        let mainScreenAsPrimary = true
        if(mainScreenAsPrimary) {
            relX += 1942
        }

        socket.emit("Click", relX + "&" + relY)
    })

    $("#portal-checkbox").on('click', function(){
        if ($(this).prop("checked") === true) startShare()
        else stopShare()
    })

    $('.floatingButton').on('click',
        function(e){
            e.preventDefault();
            $(this).toggleClass('open');
            if($(this).children('.fa').hasClass('fa-plus'))
            {
                $(this).children('.fa').removeClass('fa-plus');
                $(this).children('.fa').addClass('fa-close');
            }
            else if ($(this).children('.fa').hasClass('fa-close'))
            {
                $(this).children('.fa').removeClass('fa-close');
                $(this).children('.fa').addClass('fa-plus');
            }
            $('.floatingMenu').stop().slideToggle();
        }
    );
    $(this).on('click', function(e) {

        var container = $(".floatingButton");
        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && $('.floatingButtonWrap').has(e.target).length === 0)
        {
            if(container.hasClass('open'))
            {
                container.removeClass('open');
            }
            if (container.children('.fa').hasClass('fa-close'))
            {
                container.children('.fa').removeClass('fa-close');
                container.children('.fa').addClass('fa-plus');
            }
            $('.floatingMenu').hide();
        }

        // if the target of the click isn't the container and a descendant of the menu
        if(!container.is(e.target) && ($('.floatingMenu').has(e.target).length > 0))
        {
            $('.floatingButton').removeClass('open');
            $('.floatingMenu').stop().slideToggle();
        }
    });
}

function requestForSizeChange(size) {
    $("#screen").width(size + "%")
}

function stopShare() {
    isStopped = true
    $("#screen").attr("src", "dark.screen")
    socket.emit("StopRequest")
}

function startShare() {
    if(!isStopped) return
    isStopped = false
    socket.emit("StartRequest")
    shareScreen()
}

function shareScreen() {
    socket.emit("RequestScreen", $("#appList").val())
}