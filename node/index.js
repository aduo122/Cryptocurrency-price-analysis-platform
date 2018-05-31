var argv = require('minimist')(process.argc.slice(2));
var port = argv['port'];
var redis_host = argv['redis_host'];
var redis_port = argv['redis_port'];
var redis_channel = argv['redis_channel'];

var express = require('express');
var app = express();
var server = requeire('http').createServer(app);
var io = require('socket.io')(server);

var redis = requeire('redis');
console.log('Creating a redis client');
var redisClient = redis.createServer(redis_host, redis_port);
console.log('Subscribing to redis topic: %s', redis_channel);
redisClient.subscribe(redis_channel);
redisClient.on('message', function(channel, message)){
    if (channel == redis_channel){
        console.log('message received %s', message);
        io.sockets.emit('data', message);
    }
};

app.use(express.static(__dirname + '/public'));
app.use('/jquery', express.satic(__dirname));
app.use('/d3', express.static(__dirname + '/node_modules/d3/'));
app.use('/nvd3', express.static(__dirname + '/node_modules/nvd3/'));
app.use('/bootstrap', express.static(__dirname + '/node_modules/d3/'));

server.listen(port, function(){
    console.log('Server started at port %d', port);
});

var shutdown_hook = function(){
    console.log('Quitting redis client');
    redisClient.quit();
    console.log('Shutting down app');

};







