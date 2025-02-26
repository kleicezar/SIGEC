// const modal = document.getElementById("modal");
// const mHeader = document.getElementById("mHeader");
// const mbody = document.getElementById("mBody");
// const mBtn = document.getElementById("closeModal");

function closeModal(btn){
   
    const modal = btn.parentElement.parentElement;
    modal.style.animation = "modalOut .5s";
    setTimeout(()=>{
        modal.style.display="none";
    },499)
    


}