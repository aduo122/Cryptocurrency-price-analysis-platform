var argv = require('minimist')(process.argv.slice(2));
var port = argv['port'];
var redis_host = argv['redis_host'];
var redis_port = argv['redis_port'];
var redis_channel = argv['redis_channel'];

// Setup dependency instances.
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

// Setup redis client.
var redis = require('redis');
console.log('Creating a redis client');
var redisClient = redis.createClient(redis_port, redis_host);
console.log('Subscribing to redis topic: %s', redis_channel);
redisClient.subscribe(redis_channel)
redisClient.on('message', function(channel, message) {
	if (channel == redis_channel) {
		console.log('message received %s', message);
		io.sockets.emit('data', message)
	}
});

// Setup webapp routing.
app.use(express.static(__dirname + '/public'));
app.use('/jquery', express.static(__dirname + '/node_modules/jquery/dist/'))
app.use('/d3', express.static(__dirname + '/node_modules/d3/'));
app.use('/nvd3', express.static(__dirname + '/node_modules/nvd3/build/'));
app.use('/bootstrap', express.static(__dirname + '/node_modules/bootstrap/dist/'));

server.listen(port, function() {
	console.log('Server started at port %d', port);
})

var shutdown_hook = function () {
    console.log('Quitting redis client');
    redisClient.quit();
    console.log('Shutting down app');
    process.exit();
};

process.on('SIGTERM', shutdown_hook)
process.on('SIGINT', shutdown_hook)
process.on('exit', shutdown_hook)
