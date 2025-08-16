// Comentario: Este es el punto de entrada para conectar con tu backend en GCP.
// No puedes conectar JavaScript directamente a tu base de datos por razones de seguridad.
// En su lugar, el formulario enviará los datos a un backend (servidor) que tú crearás.
// El backend es el que se conectará a la base de datos de Cloud SQL.

document.getElementById('customerForm').addEventListener('submit', function(event) {
    // Evita que el formulario se envíe de la manera tradicional
    event.preventDefault();

    // Obtiene los datos del formulario
    const customerData = {
        customerName: document.getElementById('customerName').value,
        contactLastName: document.getElementById('contactLastName').value,
        contactFirstName: document.getElementById('contactFirstName').value,
        phone: document.getElementById('phone').value,
        addressLine1: document.getElementById('addressLine1').value,
        city: document.getElementById('city').value,
        country: document.getElementById('country').value,
        creditLimit: document.getElementById('creditLimit').value
    };

    // Comentario: Aquí se haría la llamada a la API de tu backend.
    // Reemplaza 'http://tu-backend-en-gcp.com/api/clientes' con la URL real de tu servicio.
    // Este servicio debería ser una API REST que reciba los datos y los inserte en la base de datos.

  fetch('https://api-registrar-clientes-670780568233.southamerica-west1.run.app/registrar-cliente', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(customerData)
})
    .then(response => {
        // Maneja la respuesta del servidor
        if (response.ok) {
            return response.json();
        }
        throw new Error('Algo salió mal en el servidor.');
    })
    .then(data => {
        // Muestra un mensaje de éxito o error
        const messageElement = document.getElementById('message');
        if (data.success) {
            messageElement.textContent = 'Cliente registrado con éxito.';
            messageElement.style.color = 'green';
            document.getElementById('customerForm').reset(); // Limpia el formulario
        } else {
            messageElement.textContent = 'Error: ' + data.error;
            messageElement.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'Error de conexión o de red.';
        document.getElementById('message').style.color = 'red';
    });
});