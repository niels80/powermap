   
const URL_dataEEG = './dataH3/';
const URL_MASTR_BASE = 'https://www.marktstammdatenregister.de'
const NR_FOLDERS  = 50;

var color_scale = chroma.scale(['white', 'green', 'yellow', 'red']);

var datatables = {
    "power_units_wind"   : "Wind",
	"power_units_solar" : "Photovoltaics",
    "power_units_biomass" : "Biomass",
    "power_units_geo_soltherm_other" : "Geothermal, Solarthermal, other",
    "power_units_hydro" : "Hydro",
    "power_units_nuclear" : "Nuclear",
    "power_units_consumer" : "Power Consumer",
    "power_units_storage" : "Power Storage",
    "power_units_thermal" : "Power Thermal Units",
    "gas_units_consumer" : "Gas consumers",
    "gas_units_generator" : "Gas generators",
    "gas_units_storage" : "Gas storage"
}

var checkState = {};
var scale_bars = 1;
var year_from  = 1990;
var year_to    = 2030;
var include_null = 0;

function updateCheckState() {
	for(var t in datatables) {
		checkState[t] = false;
	}
	if ($('#check-gen-solar').is(':checked')) { checkState["power_units_solar"] = true}
	if ($('#check-gen-wind').is(':checked')) { checkState["power_units_wind"] = true }
	if ($('#check-gen-biomass').is(':checked')) { checkState["power_units_biomass"] = true }
	if ($('#check-gen-hydro').is(':checked')) { checkState["power_units_hydro"] = true }
	if ($('#check-gen-nuclear').is(':checked')) { checkState["power_units_nuclear"] = true }
	if ($('#check-gen-thermal').is(':checked')) { checkState["power_units_thermal"] = true }
	if ($('#check-gen-geothermal').is(':checked')) { checkState["power_units_geo_soltherm_other"] = true }
	if ($('#check-consumer').is(':checked')) { checkState["power_units_consumer"] = true }
	if ($('#check-storage').is(':checked')) { checkState["power_units_storage"] = true }
	if ($('#check-gas-consumer').is(':checked')) { checkState["gas_units_consumer"] = true }
	if ($('#check-gas-storage').is(':checked')) { checkState["gas_units_storage"] = true }
	if ($('#check-gas-generation').is(':checked')) { checkState["gas_units_generator"] = true }
	
	include_null = $('#check-include-null').is(':checked');
	scale_bars = document.getElementById("scale_slide").value;
	year_from  = document.getElementById("year_from").value;
	year_to  = document.getElementById("year_to").value;
}

async function initialize() {
  

	var dataStatistics = {};
	var dataStatisticsArray = [];
    var n = 0;
	
	document.getElementById("myBar").style.width = Math.round(n/10*100) + "%";
	n = n+1;
	var url = URL_dataEEG+'statistics_yearly.json?'+Math.random();
	console.log("Fetching "+url)
	var response = await fetch(url).then(response => response.json()).then(
		data => {
			  Object.keys(data).forEach(function (idH3) { 
					dataStatisticsArray.push(
					{
						"idH3" : idH3,
						"data" : data[idH3]
					})
				})
			}
	);
	
	
	document.getElementById("myBar").style.width = Math.round(100) + "%";
	

	function getHex(d) {
		//console.log(d.id_H3)
		return(d.id_H3)
	}
	
	function getPower(d) {
		p = 0;
		Object.keys(d).forEach(function (year) { 	
			if (
				(year=="null" && include_null) ||
				(year>=year_from && year<=year_to) ||
				(year_from==1990 && year<1990)
				)
				{
					Object.keys(d[year]).forEach(function (t) { 	
					  if (checkState[t]) {
						  p = p + d[year][t].P;
					  }
					});
				}
		});
		return(p)
	}
	
	function getColor(d) {
		p = getPower(d);
		return(color_scale(p/10000).rgb());
	}
	
	function getTooltip(d) {
		p = 0;
		var ttip = '<table><tr><td>Year</td>';
		for(var t in datatables) {
		  if (checkState[t]) {
			 ttip = ttip + '<td class="text-right">'+datatables[t]+'</td>';
		  }
		}
		ttip = ttip+'</tr>';
		
		Object.keys(d.data).forEach(function (year) { 	
			if (
				(year=="null" && include_null) ||
				(year>=year_from && year<=year_to) ||
				(year_from==1990 && year<1990)
				)
				{
					 P_total = 0;
					 var row = '<td>'+year+'</td>';
					 for(var t in datatables) {
					  if (checkState[t]) {
						 row = row + '<td class="text-right">';
						 if (t in d.data[year]) {
							 row = row + Math.round(P_total+d.data[year][t].P/10)/100+ " MW";
							 P_total = P_total+d.data[year][t].P ;
						 }
						 row = row + '</td>';
					  }
					}
					if (P_total > 0) {
						ttip = ttip+'<tr>'+row+'</tr>';
					}
				
				}
			
		});
		ttip = ttip+'</table>';
		return(ttip)
		//

		
	}
	

	
	const ambientLight = new deck.AmbientLight({
	  color: [255, 255, 255],
	  intensity: 2
	});
	
	const directionalLight= new deck.DirectionalLight({
	  color: [255,255,255],
	  intensity: 5.0,
	  direction: [0, 0, 90]
	});
	
	
	// Create Deck.GL map
	const deckgl = new deck.DeckGL({
		container: 'powermap',
		initialViewState: {
		  longitude: 10,
		  latitude: 50,
		  zoom: 6,
		  pitch: 60,
		  minZoom: 2,
		  maxZoom: 16
		},
		controller: true,

		mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',  //'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json', //
		//getTooltip: ({object}) => object && `${object.tip}`,
		getTooltip: ({object}) => object && {
									html: getTooltip(object),
									style: {
									  backgroundColor: '#fefefe',
									  fontSize: '0.8em'
									}
								},
		layers: [
																  
		]
	});

	
	var updateTrigger=0;
	
	function render() {
		const layer = new deck.H3HexagonLayer({
					id: 'h3-hexagon-layer',
					data: dataStatisticsArray,
					pickable: true,
					wireframe: false,
					filled: true,
					opacity : 0.2,
					extruded: true,
					elevationScale: 10,
					getHexagon: d => d.idH3,
					getFillColor: d => (getColor(d.data)),
					getElevation: d=> (getPower(d.data)*scale_bars/1000),
					updateTriggers: {
					  getElevation: updateTrigger,
					  getFillColor: updateTrigger
					},
			})		
		deckgl.setProps({layers: [layer]});
		
	}
	updateCheckState();
	render();
	
	$('.update_on_change').change(function(){ 
		updateCheckState();
		updateTrigger = updateTrigger+1;
		render();
		 document.getElementById("year_from_output").value=year_from;
		 document.getElementById("year_to_output").value=year_to;
	});
	
	
	const onClick = ({ x, y, object }) => {
		setSelectedPoint(object);
		setX(x);
		setY(y);
	};
	
	document.getElementById("loading").style.display = "none";
		    
}