window.addEventListener('DOMContentLoaded',init,false);
            
function init() {
    alert('The page loaded!');
    var buttons = document.getElementsByTagName("button")/* since there is more than one button */

buttons[0].addEventListener('click', changeWidth,false)
    
}

/* function changeWidth() {
    {document.getElementsByID("MyPosts").className= "post2";}
    
} */

function changeWidth() {
  var width = document.getElementById("MyPosts");
  {
    width.className = "post2";
  } 
}
/* I'm not sure how to change the class="post" to class="post2"  
 * The only thing different between the two classes is the width.
 * Sorry, functions are my mortal enemies
 * 
 * 
 * */
/* My train of thought:
 * The window loads, activating function init()
 * var buttons is equal to any HTML element called "button"
 * the first of the var buttons is made to listen for a 'click'
 * when there is a 'click,' the function changeWidth is called
 * changeWidth is suposed to find the class="post" in HTML and change the class to class="post2" 
 * */