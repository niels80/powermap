   
const URL_dataEEG = './dataH3/';
const NR_FOLDERS  = 50;

var color_scale = chroma.scale(['green', 'yellow', 'red']);

var datatables = {
	"gas_units_consumer" : "Gas consumers",
    "gas_units_generator" : "Gas generators",
    "gas_units_storage" : "Gas storage",
    "power_units_biomass" : "Power Biomass",
    "power_units_consumer" : "Power Consumer",
    "power_units_geo_soltherm_other" : "Power Geothermal, Solarthermal, other",
    "power_units_hydro" : "Power Hydro Units",
    "power_units_nuclear" : "Power Nuclear",
    "power_units_solar" : "Power Photovoltaics",
    "power_units_storage" : "Power Storage",
    "power_units_thermal" : "Power Thermal Units",
    "power_units_wind"   : "Power Wind Units"
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
					for(var unit in data["units"][t]) {
					uD = data["units"][t][unit];
					var value = "/";
					if (uD.hasOwnProperty("power_netto")) { value = uD.power_netto; }
					dat.push([uD.id_mastr_unit,
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
				
				$('#powertable').DataTable( {
					"destroy": true,
					"scrollY" : "40vh",
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
		
		var bio = 0;
		if (dataStatistics[idH3].hasOwnProperty("power_units_biomass")) { bio = dataStatistics[idH3]["power_units_biomass"]["power_netto"] };
		
		var pv  = 0;
		if (dataStatistics[idH3].hasOwnProperty("power_units_solar")) { pv = dataStatistics[idH3]["power_units_solar"]["power_netto"] };
		
		var wind  = 0;
		if (dataStatistics[idH3].hasOwnProperty("power_units_wind")) { wind = dataStatistics[idH3]["power_units_wind"]["power_netto"]	};
		
		var tooltip  = ""; //" H3-Index : "+idH3+"\n";
			tooltip += " Photovoltaics : "+Math.round(pv)+" kW\n";
			tooltip += " Wind :  "+Math.round(wind)+" kW\n";
			tooltip += " Biomass :  "+Math.round(bio)+" kW\n";
			
		dataStatisticsArray.push(
		{
			"idH3" : idH3,
			"tip"  : tooltip,
			"power": wind+pv+bio,
		}
		)
	}
	
	document.getElementById("myBar").style.width = Math.round(100) + "%";
	
	const ambientLight = new deck.AmbientLight({
	  color: [255, 255, 255],
	  intensity: 2
	});
	
	const directionalLight= new deck.DirectionalLight({
	  color: [255,255,255],
	  intensity: 5.0,
	  direction: [0, 0, 90]
	});

	function getHex(d) {
		//console.log(d.id_H3)
		return(d.id_H3)
	}
	
	
	document.getElementById("loading").style.display = "none";
	
	// Create Deck.GL map
	const deckgl = new deck.DeckGL({
		container: 'powermap',
		initialViewState: {
		  longitude: 9,
		  latitude: 51,
		  zoom: 5,
		  pitch: 45,
		  minZoom: 2,
		  maxZoom: 16
		},
		controller: true,

		mapStyle: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',  //'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json', //
		getTooltip: ({object}) => object && `${object.tip}`,
						
		
		layers: [
			new deck.H3HexagonLayer({
					id: 'h3-hexagon-layer',
					data: dataStatisticsArray,
					pickable: true,
					wireframe: false,
					filled: true,
					opacity : 0.2,
					extruded: true,
					elevationScale: 10,
					getHexagon: d => d.idH3,
					getFillColor: d => color_scale(d.power/10000).rgb(),
					getElevation: d=> (d.power/50),
					onClick: (info, event) => updateTable(info.object.idH3)
			})															  
		]
	});


	const onClick = ({ x, y, object }) => {
		setSelectedPoint(object);
		setX(x);
		setY(y);
	};


    
}