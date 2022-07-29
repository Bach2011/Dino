document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input.ans').forEach(
        element => {
            element.addEventListener('click', () => {
                document.querySelector('input[name="answer"]').value = element.value
            })
        }
    )
    document.querySelectorAll("input[type='checkbox']").forEach(element => {
        element.addEventListener('click', function() {
            document.querySelector('input[name="correct"]').value = element.value
        })
    })
    document.querySelector('.edit_name').style.display = 'none'
    document.querySelector('.edit_quiz_name').addEventListener('click', function() {
        document.querySelector('form').style.display = 'block';
        document.querySelector('h3').style.display = 'none'
    })
    })
    
