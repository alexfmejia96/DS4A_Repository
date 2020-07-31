function loadExtras() {
	setTimeout(function(){
		//document.getElementById('folder_list').size=10;
		
		let script = document.createElement('script');
	  	script.src = 'https://code.getmdl.io/1.3.0/material.min.js';
	  	script.id = 'ml_code';
		script.defer = true;
	  	document.body.append(script);
}, 1000);
}

//window.addEventListener('load', loadExtras());

new MutationObserver(function() {
	if (document.title == 'Dash'){
		bar="<div id='p2' class='mdl-progress'>\
		    <div class='bufferbar bar bar2' style='width: 100%;''></div>\
		  	</div>";
		bar = ''
			
		img_list = document.getElementById('img_list');
		if(img_list != null){
			
			if(img_list.name != 'updated'){
				img_list.name = 'updated';
				console.log('>img_list: Updated!')
				for (option of img_list.children){
					if (option.text.includes('+')){
						option.text = option.text.replace('+','  ');
						option.className = 'good';
					}else if(option.text.includes('-')){
						option.text = option.text.replace('-','  ');
						option.className = 'bad';
					}else if(option.text.includes('>')){
						option.text = option.text.replace('>','');
						option.style = 'font-size:18px';
					}else{
						option.className = 'default';
					}
				}
			}
		}

		let meta_map =document.getElementById('meta_frame');
		if(meta_map != null){
			meta_map.onload = function(){
				this.contentDocument.open();
				this.contentDocument.write(atob(this.getAttribute('data-html')));
				this.contentDocument.close();
				alert('dsf');
			}
		}
		
	}else{
	bar="<div id='p2' class='mdl-progress mdl-js-progress mdl-progress__indeterminate is-upgraded' data-upgraded=',MaterialProgress'>\
	    <div class='progressbar bar bar1' style='width: 0%;'></div>\
	    <div class='bufferbar bar bar2' style='width: 100%;'></div>\
	    <div class='auxbar bar bar3' style='width: 0%;'></div>\
	  	</div>";
	}

	document.getElementById('dw_result').innerHTML = bar;
	console.log(document.title);

}).observe(document.querySelector('title'),{ childList: true });