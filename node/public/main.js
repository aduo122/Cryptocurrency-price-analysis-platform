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
		var symbol = parsed['Symbol'];
		var point = {};
		point.x = timestamp;
		point.y = price;

		var i = getSymbolIndex(symbol, data_points);
		data_points[i].values.push(point);
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