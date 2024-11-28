const fieldClient = document.getElementById("field-client");
const select = document.getElementById("selection");
select.style.display = "none";
const options = select.querySelectorAll("option");

fieldClient.addEventListener("input", () => {
    const filterValue = fieldClient.value.toLowerCase(); 

    console.log(filterValue);
    options.forEach(option => {
        var contentText = option.textContent.toLowerCase();
        
        const contentTextLoc = contentText.indexOf("-")
        
        contentText = contentText.slice(contentTextLoc+2);
     
        console.log(contentText);
        if (filterValue.length > 0) {
            select.style.display = "block";
            if (contentText.startsWith(filterValue)) {
                option.style.display = "block";

            } else {
                
                option.style.display = "none";
            }
        } else {
            select.style.display = "none";
        }
    });
});



