     // enter logic
    $(document).keyup(function(event) {
    if ($(".input").is(":focus") && event.key == "Enter") {
        // Do work
        variousInput()
         }
    });

	function ajaxTest()
	{
		output=[]
		var tempParams =
		{
			"value": $("#textBox").val(),
			"name": name,
			"location": current_location
		}

		$.ajax({
        type: 'GET',
        url: "/the_alley/various",
        data: JSON.stringify(tempParams),
        async: false,
        beforeSend: function (xhr)
        {
        	if (xhr && xhr.overrideMimeType) {
        		xhr.overrideMimeType('application/jsoncharset=utf-8')
        	}
		},
       	dataType: 'json',
       	success: function (data)
		{
			output = data
    	   	alert(output['value'])
    	   	alert(output['msg'])
    	   	alert(output['location'])

       }
	})}

	function variousInput()
	{
			var output = []
			var textBox = $('#input').val()
				$.ajax({
				    //data:JSON.stringify(textBox)
					contentType : 'application/json',
					url: encodeURI("/variousInput" + "?name=" + name + "&value=" + textBox),
					}).then(function(data)
						{
						output = data
						alert(output)
						$("#mapInfo").append(output['mapinfo'])
						$("#npcInfo").append(output['npcinfo'])
						//$("#npcInfo").append(JSON.stringify(output))
						$( "#output" ).fadeIn( 4000, function() {})
						})
	}

	function createNewUser(url)
    {
			var name = $('#createUser').val()
			$.ajax({
			//data: JSON.stringify(jsonParams),
			url: encodeURI(url + "?name=" + name),
			}).then(function(data)
			{
				$('#output').append(data)
				Redirect(encodeURI("/the_alley/home?name=" + name))
			})
	}
	function init(url)
    {
			var output = []
			$.ajax({
			url: encodeURI(url),
			}).then(function(data)
			{
				output = data
				//alert(output)
				$("#output").append(output + " <br />")
				$( "#output" ).fadeIn( 5000, function() {})

			})
	}

	function initMap(url)
    {
			var output = []
			$.ajax({
			url: encodeURI(url),
			}).then(function(data)
			{
				output = data
				alert(output)
				$("#output").append(output + " ")
				$( "#output" ).fadeIn( 4000, function() {})
			})
	}
	function Redirect(url)
	{
		var ua = navigator.userAgent.toLowerCase(), verOffset = ua.indexOf('msie') !== -1, version = parseInt(ua.substr(4, 2), 10)
		// IE8 and lower fix
		if (navigator.userAgent.match(/MSIE\s(?!9.0)/))
		{
			// IE8 and lower
			// if (verOffset && version < 9) {
			var link = document.createElement('a')
			link.href = url
			document.body.appendChild(link)
			link.click()
		}
		// All other browsers
		else
		{
			window.location.href = url
		}
	}