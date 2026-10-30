import sender_stand_request
import data


# Cambia el valor de "firstName" en una copia del cuerpo de solicitud
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Función auxiliar para las pruebas positivas
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1


# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Función auxiliar para pruebas negativas por nombre inválido
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert (response.json()["message"] == "Has introducido un nombre de usuario no válido. "
                                          "El nombre solo puede contener letras del alfabeto latino, "
                                          "la longitud debe ser de 2 a 15 caracteres.")
# Función auxiliar para pruebas negativas por parámetro ausente o vacío
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

# Prueba 3. El parámetro "firstName" contiene 1 carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# Prueba 4. El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


# Prueba 5. El parámetro "firstName" contiene un espacio
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")


# Prueba 6. El parámetro "firstName" contiene caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")


# Prueba 7. El parámetro "firstName" contiene números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Prueba 8. La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)


# Prueba 9. El parámetro "firstName" es un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

# Prueba 10. El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400