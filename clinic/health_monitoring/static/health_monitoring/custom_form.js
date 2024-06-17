document.addEventListener('DOMContentLoaded', function () {
    const addSymptomButton = document.getElementById('add-symptom');
    const form = document.querySelector('form');

    addSymptomButton.addEventListener('click', function () {
        const medicationId = form.querySelector('#id_medication').value;
        fetch(`/get-symptoms/${medicationId}/`)
            .then(response => response.json())
            .then(data => {
                const symptomDiv = document.createElement('div');
                symptomDiv.classList.add('form-group');
                data.forEach(symptom => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'symptom';
                    checkbox.value = symptom.id;

                    const label = document.createElement('label');
                    label.textContent = symptom.name;

                    symptomDiv.appendChild(checkbox);
                    symptomDiv.appendChild(label);
                    symptomDiv.appendChild(document.createElement('br'));
                });
                form.insertBefore(symptomDiv, addSymptomButton);
            });
    });
});
