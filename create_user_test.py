import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_user_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

    print(user_response.status_code)
    print(user_response.json())

def negative_assert(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, "\
                                         "la longitud debe ser de 2 a 15 caracteres."

    print(response.status_code)
    print(response.json())

def negative_assert_no_firstname(user_body):
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

    print(user_response.status_code)
    print(user_response.json())

#PRUEBAS DE EQUIVALENCIA
#Prueba 1. Usuario creado con exito
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. Usuario o usuaria creada con éxito. El parámetro firstName contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Prueba 3. Error. El parámetro firstName contiene 1 carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert("A")

# Prueba 4. Error. El parámetro firstName contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert("Aaaaaaaaaaaaaaaa")

# Prueba 5. Usuario o usuaria creada con éxito. El parámetro firstName contiene espacios
def test_create_user_english_letter_in_first_name_get_success_response():
    negative_assert("A Aa")

# Prueba 6. Error. El parámetro firstName contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("!Ñ$%&")

# Prueba 7. Error. El parámetro firstName contiene un string de dígitos
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert("123")

# Prueba 8. Error. Falta el parámetro firstName en la solicitud
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

# Prueba 9. Error. El parámetro contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

# Prueba 10. Error. El tipo del parámetro firstName: número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400