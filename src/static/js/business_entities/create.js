document.addEventListener('DOMContentLoaded', function() {
    const tovChoice = document.getElementById('id_business_entity_0');
    const fopChoice = document.getElementById('id_business_entity_1');
    const submitButton = document.getElementById('submitButton')

    const inputEdrpou = document.querySelector('div #id_edrpou');
    const directorName= document.querySelector('div #id_director_name').parentElement;
    const companyName= document.querySelector('div #id_company_name').parentElement;
    const companyNameInput = document.getElementById('id_company_name');
    const companyNameLabel = companyName.parentElement.querySelector('label');
    const labelDirectorName = directorName.parentElement.querySelector('label');

    function toggleForms() {

        if (tovChoice.checked) {
            submitButton.textContent = 'Створити ТОВ';
            inputEdrpou.setAttribute('minlength', '10');
            inputEdrpou.setAttribute('maxlength', '10');
            labelDirectorName.textContent = 'ПІБ директора';
            companyNameLabel.style.display = 'block';
            companyNameInput.style.display = 'block';
        } else if (fopChoice.checked) {
            inputEdrpou.value = inputEdrpou.value.substring(0, 8);
            submitButton.textContent = 'Створити ФОП'
            inputEdrpou.setAttribute('minlength', '8');
            inputEdrpou.setAttribute('maxlength', '8');
            labelDirectorName.textContent = 'ПІБ ФОПа';
            companyNameLabel.style.display = 'none';
            companyNameInput.style.display = 'none';
        }
    }

    tovChoice.addEventListener('change', toggleForms);
    fopChoice.addEventListener('change', toggleForms);

    toggleForms();
});
