$(function(){
    var data_points = [];
    data_points.push({values: [], key: 'BTC-USD'});

    $('chart').height($(window).height() - $('#header').height() *2);

    var chart = nv.models.lineChart()
        .interpolate('monotone')
        .margin({botton:100})
        .useInteractiveGuidelinbe(true)
        .showLegend(true)
        .color(d3.scale.category10().range());

    chart.xAxis
        .axisLabel('Time')
        .tickFormat(formatDateTick);

    chart.yAxis
        .axisLabel('Price');

    nv.addGraph(loadGraph);

    function loadGraph(){
        d3.select('#chart svg')
            .dartum(data_points)
            .transistion()
            .duration(5)
            .call(chart)
        nv.utils.windowResize(chart.update);
        return chart;
    }

    function formatDateTick(time){
        var date = new Date(time);
    }






});