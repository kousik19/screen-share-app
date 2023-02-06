let socket = io.connect('http://localhost:3000');
let curX
let curY
window.onload = function() {
    window. addEventListener("contextmenu", e => e. preventDefault());
    shareScreen()

    socket.on('RenderScreen', function(message){
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
        socket.emit("Click", relX + "&" + relY)
    })

    $(document).mousemove(function(event) {
        curX = event.pageX;
        curY = event.pageY;
        socket.emit("MoveMouseBackToBrowserRequest", curX + "&" + curY)
    });
}

function requestForSizeChange() {
    $("#screen").width($("#appList").val() + "%")
}

function shareScreen() {
    socket.emit("RequestScreen", $("#appList").val())
}