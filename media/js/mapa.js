var map;
var markers = [];
var marker;
var infowindow;
var iconos = {};
var categorias = {};
var ultima;
var lugares;
var pk;

var Input_Direccion = "id_direccion"; //Input donde se trae la direccion
var Input_Longitud = "id_longitud"; //Input de la latitud donde se mostrara
var Input_Latitud = "id_latitud"; //Input de la longitu donde se mostrara
         
var mapOptions = {
	center: new google.maps.LatLng(19.440694, -99.20469800000001),
	zoom: 4,
	mapTypeId: google.maps.MapTypeId.ROADMAP,
	mapTypeControl:false
};

// Deletes all markers in the array by removing references to them.
function deleteOverlays() {
	clearOverlays();
	markers = [];
}

// Sets the map on all markers in the array.
function setAllMap(map) {
	for (i in markers) {
		markers[i].setMap(map);
	}
}

// Removes the overlays from the map, but keeps them in the array.
function clearOverlays() {
	setAllMap(null);
}

function agregarLugar(l){
	for (x in categorias) {
		if (x == l.categoria) {
			categorias[x].push(l);
			return;
		}
	}
	categorias[l.categoria] = new Array();
	iconos[l.categoria] = l.categoria_img;
	categorias[l.categoria].push(l);
}

function cargarLugaresyCategorias(){
	obtenerLugaresyCategorias(null);
}

function obtenerLugaresyCategorias(ul){
	$.get("/building/json/", function(data){
		eval('lugares = '+data);
		for (l in lugares) {
			//alert(lugares[l].categoria_img);
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(lugares[l].latitud, lugares[l].longitud),
				draggable: false,
				//icon: lugares[l].categoria_img,
				title: lugares[l].nombre,
				obj : lugares[l]
			});
			marker.setIcon(new google.maps.MarkerImage(lugares[l].categoria_img));
			markers[lugares[l].pk] = marker;
			google.maps.event.addListener(marker, 'click', function() {
				if(infowindow == null){
					infowindow = new google.maps.InfoWindow();
				}
				infowindow.close();
				var content= '<style> img.infow{ float:left; width:100px; height:100px; margin: auto 20px auto auto;} #link{ position:absolute; right:0;bottom:0;} span.lnombre, span.ldireccion{font-family: "Eurostile", Eurostile, "Myriad Pro", Arial, "sans-serif;";} </style>'+
						'<div style="width:350px;"><img class="infow" src=\''+this.obj.foto_url+' \'/>'+
						'<span class="lnombre"><strong>'+this.obj.nombre+'</strong></span><br/>'+
						'<span class="ldireccion">'+this.obj.direccion+'</span><br/>'+
						'<a id="link" href=\'/building/view/'+this.obj.pk+'\'>Ver más</a></div>';
				infowindow.setContent(content);
				infowindow.open(map, this);
			});
			agregarLugar(lugares[l]);
		}
		if (ul != null) {
			ponerMenuCategorias(ul);
		}
		if(pk == null){
			ponerTodos();
		}
		else{
			for(m in markers){
				if(m == pk){
					markers[m].setMap(map);
					map.setZoom(17);
					map.panTo(markers[m].getPosition());
				}
			}
		}
	});
}

function ponerMenuCategorias(ul){
	var liT = document.createElement('li');

	var aT = document.createElement('a');
	aT.setAttribute("href","#");

	aT.appendChild(document.createTextNode("Todos"));
	aT.onclick = function() {
		ponerTodos();
		return false;
	};
	liT.appendChild(aT);
	ul.appendChild(liT);
	for (x in categorias) {
		var li = document.createElement('li');

		var a = document.createElement('a');
		a.setAttribute("href","#");
		a.value = x;

		a.appendChild(document.createTextNode(x));

		var sm = document.createElement('small');
		var icono = document.createElement('img');
		icono.setAttribute('src', iconos[x]);
		icono.style.height = "18px";
		sm.appendChild(icono);

		a.appendChild(sm);

		a.onclick = function() {
			for(c in categorias){
				if(this.value == c){
					if(ultima != null){
						for(l in categorias[ultima]){
							markers[categorias[ultima][l].pk].setMap(null);
						}
					}
					else{
						for(c2 in categorias){
							for(l2 in categorias[c2]){
								markers[categorias[c2][l2].pk].setMap(null);
							}
						}
					}
					for(l in categorias[c]){
						markers[categorias[c][l].pk].setMap(map);
					}
					ultima = c;
					break;
				}
			}
			return false;
		};
		li.appendChild(a);
		ul.appendChild(li);
	}
}
	
function initialize() {
	var m = document.getElementById('mapa');
	if(m != null){
		map = new google.maps.Map(m, mapOptions);
		obtenerLugaresyCategorias(document.getElementById('listapin'));
		var inputDireccion = document.getElementById(Input_Direccion);
		if(inputDireccion != null){
			autocompletado(inputDireccion);
			google.maps.event.addListener(map, 'click', function(event) {
	      		addMarker(event.latLng);
		    });
		}
		var lb = document.getElementById('cpin');
		if(lb != null){
			lb.onclick = function(){ localizar(); return false;}
		}
	}
}

function autocompletado(input){
	var opciones = {
	    componentRestrictions: {country: 'mx'}
	};
	var autocomplete = new google.maps.places.Autocomplete(input,opciones);

	autocomplete.bindTo('bounds', map);

	if(infowindow == null) {
		infowindow = new google.maps.InfoWindow();
	}

	google.maps.event.addListener(autocomplete, 'place_changed', function() {
		infowindow.close();
		input.className = '';
		var place = autocomplete.getPlace();

		if (!place.geometry) {
			// Inform the user that the place was not found and return.
			input.className = 'notfound';
			return;
		}
		// If the place has a geometry, then present it on a map.
		if (place.geometry.viewport) {
			map.fitBounds(place.geometry.viewport);
		}
		else {
			map.panTo(place.geometry.location);
			map.setZoom(17);  // Why 17? Because it looks good.
		}

		//LLamada a la funcion para obtener Latitud y Longitud
		addMarker(place.geometry.location);

		var address = '';
		if (place.address_components) {
			address = [
				(place.address_components[0] && place.address_components[0].short_name || ''),
				(place.address_components[1] && place.address_components[1].short_name || ''),
				(place.address_components[2] && place.address_components[2].short_name || '')
			].join(' ');
		}

		infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address+'</div>');
		infowindow.open(map, marker);
	});
}

function addMarker(location) {
	if(marker == null){
		marker = new google.maps.Marker({
			map: map,
			draggable:true
		});
		markers.push(marker);
		google.maps.event.addListener(marker, 'dragend', function() {
			infowindow.close();
			obtenerLL(event.latLng);
		});
	}
	marker.setPosition(location);
	obtenerLL(location);
}


function obtenerLL(coordenada){
  
	var str = " "+coordenada;
	str=str.replace("(",'');
	str=str.replace(")",'');
	var ll=str.split(",");

	document.getElementById(Input_Latitud).value = ll[0];
	document.getElementById(Input_Longitud).value = ll[1];

}

function ponerTodos(){
	for(m in markers){
		markers[m].setMap(map);
	}
	ultima = null;
}

function localizar() {
	// Try HTML5 geolocation
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function (position) {
				var pos = new google.maps.LatLng(position.coords.latitude,
					position.coords.longitude);
				
				if(infowindow == null){
					infowindow = new google.maps.InfoWindow();
				}
				infowindow.close();
				infowindow.setContent('<b>Aquí estás.</b>');
				if(marker == null){
					marker = new google.maps.Marker({
						draggable: false,
						title: "Aquí estás",
						map:map
					});
				}
				marker.setPosition(pos);
				//infowindow.open(map,marker);
				
				map.panTo(pos);
				//map.setCenter(pos);
				
				ponerTodos();
				map.setZoom(15);
			}, 
			function() {
				handleNoGeolocation(true);
			}
		);
	} else {
		// Browser doesn't support Geolocation
		handleNoGeolocation(false);
	}
}
 function handleNoGeolocation(errorFlag) {
	var content = (errorFlag)
		?'Error: El servicio de geolocalización ha fallado, \nasegurate de tener activar la localización.'
		:'Error: Tu navegador no soporta geolocalización.';

	var options = {
		map: map,
		position: new google.maps.LatLng( 19.432702332316158,  -99.13311964270179),
		content: content
	};

	var infowindow = new google.maps.InfoWindow(options);
	map.setCenter(options.position);
	map.setZoom(5);
}