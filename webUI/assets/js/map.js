function showPosition(position) {
  var latlon = position.coords.latitude + "," + position.coords.longitude;

  var img_url = "https://maps.googleapis.com/maps/api/staticmap?center="+latlon+"&zoom=14&size=400x300&sensor=false&key=AIzaSyBRDxyphjOuTjf8tTmchDubiYlpmSyLG5Y";

  document.getElementById("mapholder").innerHTML = "<img src='"+img_url+"'>";
}
