# Cambios
- Se hizo un sistema con las coordenadas de la pose y las manos con una red neuronal descrita abajo.
- Se descartaron las imagenes en las que mediapipe no detectaba ninguna mano (si se elegia si detectaba si quiera una mano).
- Se agrego un módulo de data augmentation en donde se aplico una rotación aleatoria de 10 grados a las fotos y a todas las fotos se les generó un flip horizontal para simular las señas zurdas.
- A diferencia del resultado anterior se bajo el dropout de 0.4 a 0.3 para probar si se mejoraba el resultado.
- Se ejecutó el modelo con 1000 epochs y se obtuvo un accuracy de 0.90.
```python
INPUT_SHAPE_1 = (300,)

def get_model_coord_dense_1(input_shape, num_classes):
    MODEL_COORD_DENSE = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return MODEL_COORD_DENSE
```