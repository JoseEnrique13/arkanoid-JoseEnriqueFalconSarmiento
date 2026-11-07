# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido y nivel inexistente;

Con el nivel válido se abre la ventana con los bloques, la pala y la bola.
Con el inexistente: salta "FileNotFoundError: El fichero no es válido", y no se abre la ventana..

- nivel con filas de distinta longitud;

Salta "ValueError: Las líneas deben tener el mismo ancho", y no se abre la ventana.

- paleta en ambos límites de la pantalla;

La pala se para justo en el borde izquierdo sin salirse, lo mismo con el derecho.



- rebote contra pared, paleta y cada tipo de bloque;

En paredes y techo la bola cambia su dirección y rebota y  en la pala la bola rebota hacia arriba.
Cada bloque desaparece al golpearlo y suma puntos: # = 50, @ = 75, % = 120 (se ve en la ventana del juego).

- pérdida de una vida y reinicio de la bola;

La bola vuelve a aparecer encima de la pala y la puntuación se mantiene.

- victoria al eliminar el último bloque y derrota al agotar vidas;

Victoria: aparece "¡Has ganado!" en el centro y la ventana se cierra sola a los ~2 segundos.
Derrota: aparece "Game Over" en el centro y la ventana se cierra sola a los ~2 segundos.

- salida limpia con Escape y al cerrar la ventana.

La ventana se cierra correctamente a los segundos y se regresa a la terminal.

Una mejora opcional no debe romper ninguno de estos casos.
