document.addEventListener('DOMContentLoaded', function() {
    let a = document.querySelectorAll('.type')
    a.forEach(element => {
        element.addEventListener('change', function() {
            let id = element.id
            id = id.replace('type','')
            if(element.value == "select"){
                document.querySelector(`.options${id}`).style.display = 'block'
                document.getElementById(`text${id}`).style.display = 'none'
            }if (element.value == "text") {
                document.querySelector(`.options${id}`).style.display = 'none'
                document.getElementById(`text${id}`).style.display = 'block'
            }
    })
    })  
    document.querySelectorAll("input[type='checkbox']").forEach(element => {
        element.addEventListener('click', function() {
            document.querySelector('input[name="correct"]').value = element.value
        })
    })
})