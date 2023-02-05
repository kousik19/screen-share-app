const app = require('express')();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.get('/ui/:path', (req, res) => {
    res.sendFile(__dirname + '/view/' + req.params.path);
});

app.get('/ui/style/:path', (req, res) => {
    res.sendFile(__dirname + '/view/style/' + req.params.path);
});

app.get('/ui/js/:path', (req, res) => {
    res.sendFile(__dirname + '/view/js/' + req.params.path);
});

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on("RequestScreen", (arg) => {
        socket.broadcast.emit("ShareScreen", arg)
    });

    socket.on("Type", (arg) => {
        socket.broadcast.emit("TypeRequest", arg)
    });

    socket.on("Click", (arg) => {
        socket.broadcast.emit("ClickRequest", arg)
    });

    socket.on("Rightclick", (arg) => {
        socket.broadcast.emit("RightClickRequest", arg)
    });

    socket.on("CurrentScreen", (arg) => {
        socket.broadcast.emit("RenderScreen", arg)
    });

    socket.on("AppListRequest", (arg) => {
        socket.broadcast.emit("GetAppList", arg)
    });

    socket.on("AppListResponse", (arg) => {
        socket.broadcast.emit("AppList", arg)
    });

    socket.on("AppChangeRequest", (arg) => {
        socket.broadcast.emit("ChangeApp", arg)
    });

    socket.on("MoveMouseBackToBrowserRequest", (arg) => {
        socket.broadcast.emit("MoveMouseBackToBrowser", arg)
    });
});

http.listen(3000, () => {
    console.log('listening on *:3000');
});