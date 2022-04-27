   
const URL_dataEEG = './dataH3/';
const URL_MASTR_BASE = 'https://www.marktstammdatenregister.de'
const NR_FOLDERS  = 50;

var color_scale = chroma.scale(['white', 'green', 'yellow', 'red']);

var datatables = {
    "power_units_wind"   : "Power Wind Units",
	"power_units_solar" : "Power Photovoltaics",
    "power_units_biomass" : "Power Biomass",
    "power_units_geo_soltherm_other" : "Power Geothermal, Solarthermal, other",
    "power_units_hydro" : "Power Hydro Units",
    "power_units_nuclear" : "Power Nuclear",
    "power_units_consumer" : "Power Consumer",
    "power_units_storage" : "Power Storage",
    "power_units_thermal" : "Power Thermal Units",
    "gas_units_consumer" : "Gas consumers",
    "gas_units_generator" : "Gas generators",
    "gas_units_storage" : "Gas storage"
}

var checkState = {};
var scale_bars = 1;

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
	
	scale_bars = document.getElementById("scale_slide").value;
}

function loadUnit(idMastr) {
	/*  
	// Not allowed due to CORS
	
	$.get(URL_MASTR_BASE+"/MaStR/Schnellsuche/Schnellsuche",
                        {
                           praefix:     String(idMastr).substring(0,3),
                           mastrNummer: String(idMastr).substring(3)
                       })
                       .done(function(data) {
                           if (data.url) {
                               if (data.fragment){
								   window.open(
									  URL_MASTR_BASE+decodeURIComponent(data.url) + "#"+data.fragment,
									  '_blank' // <- This is what makes it open in a new window.
									);
                                   
                               }else{
								   window.open(
									  URL_MASTR_BASE+decodeURIComponent(data.url),
									  '_blank' // <- This is what makes it open in a new window.
									);
                               }
                           }
                        })
						
	*/
}


function updateTable(idH3) {
	console.log(idH3);
	var folder = String(BigInt('0x' + idH3) % BigInt(NR_FOLDERS))
	var url = URL_dataEEG+folder+'/h3_'+String(idH3)+'.json?'+Math.random();
	console.log("Fetching "+url)
				
	var response = fetch(url).then(response => response.json()).then(
			data => {
				var dat = [];
				for (var t in datatables) {
					if (checkState[t]) {
						for(var unit in data["units"][t]) {
							uD = data["units"][t][unit];
							var value = "/";
							if 		  (uD.hasOwnProperty("power_netto")) { value = Math.round(uD.power_netto,2); }
							else if   (uD.hasOwnProperty("max_inject_power")) { value = Math.round(uD.max_inject_power,2); }
							else if   (uD.hasOwnProperty("max_withdrawal_power")) { value = Math.round(uD.max_withdrawal_power,2); }
							else if   (uD.hasOwnProperty("controllable_load")) { value = Math.round(uD.controllable_load,2); }
							 	 
							dat.push([   //"<a href=\"javascript:loadUnit('"+uD.id_mastr_unit+"')\">"+uD.id_mastr_unit+"</a>",
									  uD.id_mastr_unit,
									  datatables[t],
									  uD.name,
									  uD.street+" "+uD.street_nr,
									  uD.zipcode,
									  uD.city,
									  uD.region,
									  value
									 ]);
						}
					}
				}
				
				$('#powertable').DataTable( {
					"destroy": true,
					 "paging": false,
					"scrollY": "300px",
					data: dat,
					columns: [
							{ title: "ID" },
							{ title: "Type" },
							{ title: "Name" },
							{ title: "Street" },
							{ title: "Zipcode" },
							{ title: "City" },
							{ title: "Region" },
							{ title: "Power [kW]" }
					]
				} );
				document.getElementById("powertablediv").style.visibility = "visible";
			}
	);

}



async function initialize() {
  

	var dataStatistics = {};
	
    var n = 0;
	for(var t in datatables) {
	    document.getElementById("myBar").style.width = Math.round(n/10*100) + "%";
		n = n+1;
		var url = URL_dataEEG+'statistics_t_'+t+'.json?'+Math.random();
		console.log("Fetching "+url)
		var response = await fetch(url).then(response => response.json()).then(
			data => {
				for(var i = 0; i < data.length; i++) {
					var dat = data[i];
					var idH3 = dat.id_H3;
					if (idH3 in dataStatistics) {
						dataStatistics[idH3][t] = dat;
					} else {
						dataStatistics[idH3] = {};
						dataStatistics[idH3][t] = dat;
					}
				}
			}
		);
	}
	
	var dataStatisticsArray = [];
	for(var idH3 in dataStatistics) {
		
		var installedCapacity = {};
		
		for(var t in datatables) {
			installedCapacity[t] = 0;
		
			if (dataStatistics[idH3].hasOwnProperty(t)) { 
				if (dataStatistics[idH3][t].hasOwnProperty("power_netto")) { 
					installedCapacity[t] = dataStatistics[idH3][t]["power_netto"] 
				} 
				else if (dataStatistics[idH3][t].hasOwnProperty("max_inject_power")) { 
					installedCapacity[t] = dataStatistics[idH3][t]["max_inject_power"] 
				}
				else if (dataStatistics[idH3][t].hasOwnProperty("max_withdrawal_power")) { 
					installedCapacity[t] = dataStatistics[idH3][t]["max_withdrawal_power"] 
				}
				else if (dataStatistics[idH3][t].hasOwnProperty("controllable_load")) { 
					installedCapacity[t] = dataStatistics[idH3][t]["controllable_load"] 
				};
			}
		}
		
		dataStatisticsArray.push(
		{
			"idH3" : idH3,
			"installedCapacity" : installedCapacity
		}
		)
	}
	
	document.getElementById("myBar").style.width = Math.round(100) + "%";
	

	function getHex(d) {
		//console.log(d.id_H3)
		return(d.id_H3)
	}
	
	function getPower(d) {
		p = 0;
		for(var t in datatables) {
		  if (checkState[t]) {
			  p = p + d.installedCapacity[t];
		  }
		}
		return(p)
	}
	
	function getColor(d) {
		p = getPower(d);
		return(color_scale(p/10000).rgb());
	}
	
	function getTooltip(d) {
		ttip = '<table><tr><th>Type</th><th>Capacity [kW]</th></tr>';
		for(var t in datatables) {
		  if (checkState[t]) {
			 ttip = ttip + '<tr><td>'+datatables[t]+'</td><td class="text-right">'+Math.round(d.installedCapacity[t],2)+"</td></tr>";
		  }
		}
		ttip = ttip + "</table>";
		return(ttip);
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
					getFillColor: d => (getColor(d)),
					getElevation: d=> (getPower(d)*scale_bars/1000),
					onClick: (info, event) => updateTable(info.object.idH3),
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
	});
	
	
	const onClick = ({ x, y, object }) => {
		setSelectedPoint(object);
		setX(x);
		setY(y);
	};
	
	document.getElementById("loading").style.display = "none";
		    
}