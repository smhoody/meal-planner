/**
 * Functions for MealPlanner webpage
 * @author Steven Hoodikoff
 * @date 08-19-2024
 */

/**
 * Helper function to filter ingredients based on what user searches
 */
function searchFilter() {
	// Declare variables
	var input, filter, ul, li, a, i, txtValue;
	input = document.getElementById('search-field');
	filter = input.value.toUpperCase();
	ul = document.getElementById("ing-list");
	li = ul.getElementsByTagName('li');
  
	// Loop through all list items, and hide those who don't match the search query
	for (i = 0; i < li.length; i++) {
	  a = li[i].getElementsByTagName("a")[0];
	  txtValue = a.textContent || a.innerText;
	  if (txtValue.toUpperCase().indexOf(filter) > -1) {
		li[i].style.display = "";
	  } else {
		li[i].style.display = "none";
	  }
	}
  }

  function selectIngredient() {	
	var ingredientUl = document.getElementById('ing-list');
	
	ingredientUl.onclick = function(event) {
	    var target = getEventTarget(event);
		var searchUl = document.getElementById('search-list');
	    var li = document.createElement("li"); //create list element
		var a = document.createElement("a"); //create link
		a.appendChild(document.createTextNode(target.innerText)); //add ingredient name to link
		a.href = clearItem(target.innerText); //function to remove this ingredient goes here
		
		if (target.innerText.length < 30) { //clicking between elements returns all items, so dont let it
			li.appendChild(a); //add the link to the list element
			searchUl.appendChild(li); //add the element to the list
		}
	};
}


async function submit_name(event) {
  event.preventDefault();

  let recipeName = document.getElementById("recipe-name").value;
  let encodedName = encodeURIComponent(recipeName);

  const response = await fetch(`http://127.0.0.1:8000/recipe?query=${encodedName}`, {
  method: "GET", 
  headers: {"Content-type": "application/json; charset=UTF-8"}
  });
 
  const responseText = await response.text();
}


async function submit_ingredients() {
     // data sent from the POST request
     var formData = new FormData(document.forms[0])

     // get all form keys and values
     var obj = Object.fromEntries(Array.from(formData.keys())
         .map(key => [key, formData.getAll(key).length > 1 ?
             formData.getAll(key) : formData.get(key)]))
 
     var jsonreq = (`${JSON.stringify(obj)}`)
 
     const response = await fetch('http://127.0.0.1:8000/v1/search-ingredients/', {
     method: "POST",
     body: jsonreq,
     headers: {"Content-type": "application/json; charset=UTF-8"}
   })
 
   const responseText = await response.text();
   var index_page = document.getElementById("answer");
   index_page.style.color = "blue";
   if(JSON.stringify(responseText).indexOf('overlap') > -1){index_page.style.color = "red"};
   index_page.innerHTML = (responseText);
}

function getEventTarget(e) {
    e = e || window.event;
    return e.target || e.srcElement; 
}