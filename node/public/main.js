$(function() {
	var data_points = [];
	data_points.push({values: [], key: 'BTC-USD'});

	$('#chart').height($(window).height() - $('#header').height() * 2);

	var chart = nv.models.lineChart()
		.interpolate('monotone')
		.margin({botton:100})
		.useInteractiveGuideline(true)
		.showLegend(true)
		.color(d3.scale.category10().range());

	chart.xAxis
		.axisLabel('Time')
		.tickFormat(formatDateTick);

	chart.yAxis
		.axisLabel('Price');

	nv.addGraph(loadGraph);


	function loadGraph() {
		d3.select('#chart svg')
			.datum(data_points)
			.transition()
			.duration(5)
			.call(chart);

		nv.utils.windowResize(chart.update);
		return chart;
	}

	function formatDateTick(time) {
		var date = new Date(time);
		console.log(time);
		return d3.time.format('%H:%M:%S')(date);
	}

	function newDataCallback(message) {
		var parsed = JSON.parse(message);
		var timestamp = parsed['Timestamp'];
		var price = parsed['Average'];
		var pmax = parsed['Max'];
		var pmin = parsed['Min'];
		var pstart = parsed['Start_price'];
		var pend = parsed['End_price'];
		var symbol = parsed['Symbol'];

		var point1 = {};
		point1.x = timestamp;
		point1.y = price;

		var point2 = {};
		point2.x = timestamp;
		point2.y = pmax;

        var point3 = {};
        point3.x = timestamp;
        point3.y = pmin;

        var point4 = {};
        point4.x = timestamp;
        point4.y = pstart;

        var point5 = {};
        point5.x = timestamp;
        point5.y = pend;

		var i = getSymbolIndex(symbol, data_points);
		data_points[i].values.push(point1);
		data_points[i].values.push(point2);
		data_points[i].values.push(point3);
		data_points[i].values.push(point4);
		data_points[i].values.push(point5);
		data_points[i].values.push(point1);
		if (data_points[i].values.length > 100) {
			data_point[i].values.shift();
		}
		loadGraph();
	}

	function getSymbolIndex(symbol, array) {
		for (var i = 0; i < array.length; i++) {
			if (array[i].key == symbol) {
				return i;
			}
		}
		return -1;
	}

	var socket = io();

	socket.on('data', function(data) {
		newDataCallback(data);
	})
});