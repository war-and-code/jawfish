var tooltips = true;

function tooltip_toggle() {
    
    if (tooltips == true) {
        
        tooltips = false;
        document.getElementById("tooltip_toggle").innerHTML 
            = "Turn tooltips on";
            
        $("span.tooltip").toggleClass("on");
        $("span.tooltip").toggleClass("off");
        
    } else {
        
        tooltips = true;
        document.getElementById("tooltip_toggle").innerHTML 
            = "Turn tooltips off";
            
        $("span.tooltip").toggleClass("on");
        $("span.tooltip").toggleClass("off");
        
    }
}