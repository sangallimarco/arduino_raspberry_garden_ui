function GaugesManager(){
	this.gauges = {};
}
GaugesManager.prototype = {
	init:function(){

	},
	render:function(){
		$.each(this.gauges,function(){
			//render
			this.chart.draw(this.data,this.options);
		});
	},
	add:function(label,id,value,pvalue,from,to,min,max){
		var data = google.visualization.arrayToDataTable([
				['Label', 'Value'],
				[label, value],
			]);
		//normalize
		if(to > max){
			to = max;
		}
		if(from < min){
			from = min;
		}
		var options = {
			width: 200, height: 300,
			//redFrom: pvalue, redTo: pvalue+1,
			greenFrom:from,greenTo:to,
			minorTicks: 5,
			min:min,
			max:max
		};
		var chart = new google.visualization.Gauge(document.getElementById(id));
		//store data
		this.gauges[id] = ({data:data, chart:chart, options:options});
	},
	data:function(key,val){
		this.gauges[key].data.setValue(0, 1, val);
	}


}
