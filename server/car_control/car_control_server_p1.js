var fs = require('fs');
var app = require('express')();
var https = require('https');

var server = https.createServer({
    key: fs.readFileSync('/etc/ssl/private/selfsign.key'),
    cert: fs.readFileSync('/etc/ssl/certs/selfsign.crt')
},app);

var io = require('socket.io').listen(server)
var port = process.env.PORT || 3000;

app.get('/', function(req, res){
  res.send('<h1>Car Control Server P1</h1>');
});

io.on('connection', function(socket){
	var username = socket.handshake.query.username
	console.log("User Connected: " +username)

	 socket.on('disconnect', function(reason){
	 	var delete_username = socket.handshake.query.username
	 	console.log("User disconnected: " +delete_username + " - " +reason)
  	});

	 socket.on('error', function(error){
	 	var error_username = socket.handshake.query.username
	 	console.log("User Error: " +delete_username +" - " +error)
  	});

  	socket.on('check_rpi_connectivity_ping', function(msg){
    	console.log("Received Ping: " +msg)
    	socket.broadcast.emit('check_rpi_connectivity_ping', msg);
  	});

  	socket.on('check_rpi_connectivity_pong', function(msg){
    	console.log("Received Pong: " +msg)
    	socket.broadcast.emit('check_rpi_connectivity_pong',msg);
  	});

  	socket.on('rpi_car_control', function(msg){
    	console.log("rpi_car_control: " +msg)
    	socket.broadcast.emit('rpi_car_control',msg);
  	});

});

server.listen(port, function(){
  console.log('Car Control Server P1 listening on 0.0.0.0:' + port);
});
