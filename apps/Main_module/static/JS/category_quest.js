function obtenerBalance() {
    // Limpiar los resultados anteriores en la página
    document.getElementById("resultados").innerHTML = '';
    document.getElementById("total_suma").innerHTML = '';

    // Obtener los valores seleccionados
    var categoriaSeleccionada = document.getElementById("categoria").value;
    var fechaDesde = document.getElementById("fechaDesde").value;
    var fechaHasta = document.getElementById("fechaHasta").value;
    console.log("fechas", fechaHasta, fechaDesde);

    // Enviar una solicitud Fetch al servidor con los filtros
    fetch(`/Busqueda_gastos_ingresos/?categoria=${categoriaSeleccionada}&fechadesde=${fechaDesde}&fechahasta=${fechaHasta}`)
        .then(response => response.json())
        .then(data => {
            console.log("aaaa hp", data);

            // Manejar los resultados de la búsqueda aquí
            console.log("Resultados de la búsqueda:", data);

            // Iterar sobre los resultados y agregarlos a la página
            for (var i = 0; i < data.length; i++) {
                var resultado = data[i];

                console.log("Descripciónfor:", resultado.descripcion);

                var nuevoResultadoHTML = `
                    <div class="resultado-item">
                        <p>Usuario: ${resultado.Usuario__username}</p>
                        <p>Descripcion: ${resultado.descripcion}</p>
                        <p>Fecha de Registro: ${resultado.fecha_registro}</p>
                        <p>Valor: ${resultado.valor}</p>
                    </div>`;

                // Agregar el nuevo resultado al contenedor en la página
                document.getElementById("resultados").innerHTML += nuevoResultadoHTML;
            }

            // Acceder a los totales de gastos e ingresos y agregarlos al contenedor
            var totalSumaHTML = '';

            if (categoriaSeleccionada === 'gastos') {
                var totalGastos = data.length > 0 ? data[0].total_gastos || 0.0 : 0.0;
                totalSumaHTML = `<p>Total de Gastos: $ ${totalGastos}</p>`;
            } else if (categoriaSeleccionada === 'ingresos') {
                var totalIngresos = data.length > 0 ? data[0].total_ingresos || 0.0 : 0.0;
                totalSumaHTML = `<p>Total de Ingresos: $ ${totalIngresos}</p>`;
            }

            // Agregar los totales al contenedor en la página
            document.getElementById("total_suma").innerHTML = totalSumaHTML;
        })
        .catch(error => {
            console.error("Error al realizar la búsqueda:", error);
        });
}
