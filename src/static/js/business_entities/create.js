document.addEventListener('DOMContentLoaded', function() {
    const tovChoice = document.getElementById('tovChoice');
    const fopChoice = document.getElementById('fopChoice');
    const submitButton = document.getElementById('submitButton')

    const inputEdrpou = document.querySelector('div #id_edrpou');
    const inputFopName = document.querySelector('div #id_fop_name');
    const inputDirectorName= document.querySelector('div #id_director_name');
    const inputCompanyName= document.querySelector('div #id_company_name');

    function toggleForms() {
        inputEdrpou.value = inputEdrpou.value.substring(0, 8);
        inputFopName.value = "";
        inputDirectorName.value = "";
        inputCompanyName.value = "";

        if (tovChoice.checked) {
            submitButton.textContent = 'Створити ТОВ'
            inputEdrpou.setAttribute('minlength', '10')
            inputEdrpou.setAttribute('maxlength', '10')
            inputFopName.parentElement.style.display = 'none'
            inputDirectorName.parentElement.style.display = 'block';
            inputCompanyName.parentElement.style.display = 'block';
        } else if (fopChoice.checked) {
            submitButton.textContent = 'Створити ФОП'
            inputEdrpou.setAttribute('minlength', '8')
            inputEdrpou.setAttribute('maxlength', '8')
            inputFopName.parentElement.style.display = 'block'
            inputDirectorName.parentElement.style.display = 'none';
            inputCompanyName.parentElement.style.display = 'none';
        }
    }

    tovChoice.addEventListener('change', toggleForms);
    fopChoice.addEventListener('change', toggleForms);

    toggleForms();
});
