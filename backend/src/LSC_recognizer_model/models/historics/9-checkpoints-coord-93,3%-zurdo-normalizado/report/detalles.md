# Cambios
- Se hizo un sistema con las coordenadas de la pose y las manos con una red neuronal descrita abajo.
- Se descartaron las imagenes en las que mediapipe no detectaba ninguna mano (si se elegia si detectaba si quiera una mano).
- Se agrego un módulo de data augmentation en donde se aplico una rotación aleatoria de 10 grados a las fotos y a todas las fotos se les generó un flip horizontal para simular las señas zurdas.
- Se ejecutó el modelo con 2000 epochs y se obtuvo un accuracy de 0.933).
- Se hizo cambios en las coordenadas quitando algunos parámetros de visibilidad innecesarios (en left y rigth hand).
- Se normalizó las coordenadas de 0 a 1 para que tengan mejor rendimiento en la función de activación relu.
- Por los cambios de las coordenadas el input cambió de 300 (sin face) a 226 (sin face).
- Se cambió la función de pérdida de mean_squared_error a categorical_crossentropy. (Probar con sparse_categorical_crossentropy)
## Modelo
```python
INPUT_SHAPE_FIX = (226,)

def get_model_coord_dense_2(input_shape, num_classes):
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
## Configuraciones
```python
modelo = SignModel(
    model = get_model_coord_dense_2(INPUT_SHAPE_FIX, len(classes)),
    X_train = X_train,
    Y_train = Y_train,
    X_validation = X_validation,
    Y_validation = Y_validation
)

modelo.train_model(
    epochs = 1000,
    optimizer = "Adam",
    loss = "categorical_crossentropy",
    metrics = ["accuracy"],
    callbacks = callbacks_list,
    steps_per_epoch = steps_per_epoch,
)
```