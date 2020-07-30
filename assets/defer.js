function loadExtras() {
	setTimeout(function(){
		#document.getElementById('folder_list').size=10;
		
		let script = document.createElement('script');
	  	script.src = 'https://code.getmdl.io/1.3.0/material.min.js';
	  	script.id = 'ml_code';
		script.defer = true;
	  	document.body.append(script);
}, 1000);
}

window.addEventListener('load', loadExtras());

