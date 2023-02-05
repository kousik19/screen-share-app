let socket = io.connect('http://localhost:3000');

window.onload = function() {
    window. addEventListener("contextmenu", e => e. preventDefault());
    /////////////
    const resizer = document.getElementById('dragMe');
    const leftSide = resizer.previousElementSibling;
    const rightSide = resizer.nextElementSibling;

    let x = 0;
    let y = 0;
    let leftWidth = 0;

    const mouseDownHandler = function (e) {
        // Get the current mouse position
        x = e.clientX;
        y = e.clientY;
        leftWidth = leftSide.getBoundingClientRect().width;

        // Attach the listeners to `document`
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };
    resizer.addEventListener('mousedown', mouseDownHandler);

    const mouseMoveHandler = function (e) {
        // How far the mouse has been moved
        const dx = e.clientX - x;
        const dy = e.clientY - y;

        const newLeftWidth = ((leftWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
        leftSide.style.width = `${newLeftWidth}%`;
        resizer.style.cursor = 'col-resize';
        document.body.style.cursor = 'col-resize';

        leftSide.style.userSelect = 'none';
        leftSide.style.pointerEvents = 'none';

        rightSide.style.userSelect = 'none';
        rightSide.style.pointerEvents = 'none';
    };

    const mouseUpHandler = function () {
        resizer.style.removeProperty('cursor');
        document.body.style.removeProperty('cursor');

        leftSide.style.removeProperty('user-select');
        leftSide.style.removeProperty('pointer-events');

        rightSide.style.removeProperty('user-select');
        rightSide.style.removeProperty('pointer-events');

        // Remove the handlers of `mousemove` and `mouseup`
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };
    //////////
    socket.emit("AppListRequest", "")
    shareScreen()

    socket.on('RenderScreen', function(message){
        $("#screen").attr("src", "data:image/png;base64," + message);
        setTimeout(function(){
            socket.emit("RequestScreen", $("#appList").val())
        }, 10)
    })

    socket.on('AppList', function(message){
        let html = ""
        for(let i=0; i< message.length; i++) html += "<option value='" + message[i] + "'>" + message[i].substring(0, 40) + "</option>"
        $("#appList").html(html)
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

    $("body").mousemove(function(event){
        let elemOffset = $(".right").offset();
        console.log(event.pageX + " & " + parseFloat((elemOffset.left) + parseFloat($(".right").width())))
        if(event.pageX + 5 >= parseFloat(elemOffset.left) + parseFloat($(".right").width())) {
            socket.emit("MoveMouseBackToBrowserRequest", Math.floor(parseFloat($(".right").width())) + "&" + event.pageY)
        }
    })
}

function requestForAppChange() {
    socket.emit("AppChangeRequest", $("#appList").val())
    setTimeout(function(){
        shareScreen()
    }, 500)
}

function shareScreen() {
    socket.emit("RequestScreen", $("#appList").val())
}