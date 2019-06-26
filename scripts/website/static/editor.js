NUM_PANELS = 3;

selectedColor = "black";
current_project = null;

frames = [];
current_frame = 0;


const COLORS = ["black", "blue", "green", "red", "cyan", "magenta", "yellow", "white"];


function init_editor(project){
	var project = JSON.parse(project);
	frames = project.frames;
	name = project.name;
	fps = project.fps;

	// load the first frame of the project
	loadFrame(0);
	document.getElementById("frame0").classList.add("active");

	// display the saves fps of the project
	console.log(fps);
	document.getElementById("fps-input").value = fps.toString();
}

function addNewFrame(){
	// // create an multidimensional array (2x3x8x8) (panel_row x panel x row x column) and add it to the frames
	var frame = [];
	for (var i=0; i<Math.floor(NUM_PANELS / 3); i++){
		frame[i] = new Array(3);
		for (var j=0; j<frame[i].length; j++){
			frame[i][j] = new Array(8);
			for (var k=0; k<frame[i][j].length; k++){
				frame[i][j][k] = [0, 0, 0, 0, 0, 0, 0, 0];
			}
		}
	}
	frames.push(frame);

	// create new Frame button
	var button = document.createElement("button");
	button.innerHTML = "Frame " + frames.length;
	button.setAttribute("id", "frame" + (frames.length - 1));
	button.setAttribute("type", "button");
	button.setAttribute("class", "btn btn-secondary btn-md");
	button.setAttribute("onclick", "changeFrame(this);");

	var framesDiv = document.getElementById("frames");
	framesDiv.insertBefore(button, document.getElementById("new-frame-button"));

	// change to the newly added frame
	changeFrame(button);
}

function changeFrame(button){
	// id is like frame12
	index = parseInt(button.id.substring(5));
	document.getElementById("frame" + current_frame).classList.remove("active");
	button.classList.add("active");
	current_frame = index;
	loadFrame(index);
}

function loadFrame(index){
	frames[index].forEach(function (panel_row, panel_row_index){
		panel_row.forEach(function (panel, panel_index){
			panel.forEach(function (row, row_index){
				row.forEach(function (color, led_index){
					// id of a button: panel_row_index  panel_index  row_index  half_row_index  column_index 
					document.getElementById("" + panel_row_index + panel_index + row_index + Math.floor(led_index / 4) + led_index % 4).style.background = COLORS[color];
				});
			});
		});
	});
}

function changeButtonColor(button){
	button.style.background = selectedColor;
	
	var id = button.id;
	var panel_row = parseInt(id[0]);
	var panel = parseInt(id[1]);
	var row = parseInt(id[2]);
	var column = parseInt(id[3]) * 4 + parseInt(id[4]);
	/*
	console.log(frames);
	console.log(current_frame);
	console.log(panel_row);
	console.log(panel);
	console.log(row);
	console.log(column);
	*/
	frames[current_frame][panel_row][panel][row][column] = COLORS.indexOf(selectedColor);
}

function changeSelectedColor(button, color){
	selectedColor = color;
}

function saveProject(){
	var fps = parseFloat(document.getElementById('fps-input').value);
	var data = {frames: frames,
		name: name,
		fps: fps};

	fetch('/save-project', {
		method: 'POST',
		body: JSON.stringify(data),
		headers:{
			'Content-Type': 'application/json'
		}
	}).then(res => res.json())
	// redirect to project-selection
	.then(response => window.location.replace(response.url))
	.catch(error => console.error('Error:', error));
}

