document.getElementById('encodeBtn').addEventListener('click', ()=>{
    document.getElementById('pickerForm').setAttribute("action", "/encode");
})

document.getElementById('encodeWithSplitBtn').addEventListener('click', ()=>{
    document.getElementById('pickerForm').setAttribute("action", "/encodeWithSplit");
})