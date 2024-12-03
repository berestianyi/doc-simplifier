document.addEventListener('DOMContentLoaded', function() {
    const tovChoice = document.getElementById('tovChoice');
    const fopChoice = document.getElementById('fopChoice');
    const submitButton = document.getElementById('submitButton')

    const inputEdrpou = document.querySelector('div #id_edrpou');
    const directorName= document.querySelector('div #id_director_name').parentElement;
    const companyName= document.querySelector('div #id_company_name').parentElement;
    const labelDirectorName = directorName.querySelector('label');

    function toggleForms() {
        inputEdrpou.value = inputEdrpou.value.substring(0, 8);

        if (tovChoice.checked) {
            submitButton.textContent = 'Створити ТОВ'
            inputEdrpou.setAttribute('minlength', '10')
            inputEdrpou.setAttribute('maxlength', '10')
            labelDirectorName.textContent = 'Імʼя директора ТОВа (ПІБ)'
            companyName.style.display = 'block';
        } else if (fopChoice.checked) {
            submitButton.textContent = 'Створити ФОП'
            inputEdrpou.setAttribute('minlength', '8')
            inputEdrpou.setAttribute('maxlength', '8')
            labelDirectorName.textContent = 'Імʼя ФОПа (ПІБ)'
            companyName.style.display = 'none';
        }
    }

    tovChoice.addEventListener('change', toggleForms);
    fopChoice.addEventListener('change', toggleForms);

    toggleForms();
});
