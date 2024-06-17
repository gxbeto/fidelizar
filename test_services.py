import requests

BASE_URL = "http://127.0.0.1:9092/api"

def test_get_clientes():
    try:
        response = requests.get(f"{BASE_URL}/clientes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_clientes: PASSED")
    except Exception as e:
        print(f"test_get_clientes: FAILED with error {e}")

def test_get_conceptos():
    try:
        response = requests.get(f"{BASE_URL}/conceptos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_conceptos: PASSED")
    except Exception as e:
        print(f"test_get_conceptos: FAILED with error {e}")

def test_get_reglas():
    try:
        response = requests.get(f"{BASE_URL}/reglas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_reglas: PASSED")
    except Exception as e:
        print(f"test_get_reglas: FAILED with error {e}")

def test_get_vencimientos():
    try:
        response = requests.get(f"{BASE_URL}/vencimientos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_vencimientos: PASSED")
    except Exception as e:
        print(f"test_get_vencimientos: FAILED with error {e}")

def test_get_bolsas():
    try:
        response = requests.get(f"{BASE_URL}/bolsas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_bolsas: PASSED")
    except Exception as e:
        print(f"test_get_bolsas: FAILED with error {e}")

def test_get_uso_puntos():
    try:
        response = requests.get(f"{BASE_URL}/uso_puntos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_get_uso_puntos: PASSED")
    except Exception as e:
        print(f"test_get_uso_puntos: FAILED with error {e}")

def test_consultas_uso_puntos():
    try:
        response = requests.get(f"{BASE_URL}/consultas/uso_puntos")
        assert response.status_code == 200
        assert 'uso_puntos_id' in response.text or isinstance(response.json(), list)
        print("test_consultas_uso_puntos: PASSED")
    except Exception as e:
        print(f"test_consultas_uso_puntos: FAILED with error {e}")

def test_consultas_uso_puntos_json():
    try:
        response = requests.get(f"{BASE_URL}/consultas/uso_puntos?Formato=JSON")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_consultas_uso_puntos_json: PASSED")
    except Exception as e:
        print(f"test_consultas_uso_puntos_json: FAILED with error {e}")

def test_consultas_bolsas():
    try:
        response = requests.get(f"{BASE_URL}/consultas/bolsas")
        assert response.status_code == 200
        assert 'bolsa_id' in response.text or isinstance(response.json(), list)
        print("test_consultas_bolsas: PASSED")
    except Exception as e:
        print(f"test_consultas_bolsas: FAILED with error {e}")

def test_consultas_bolsas_json():
    try:
        response = requests.get(f"{BASE_URL}/consultas/bolsas?Formato=JSON")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_consultas_bolsas_json: PASSED")
    except Exception as e:
        print(f"test_consultas_bolsas_json: FAILED with error {e}")

def test_consultas_clientes():
    try:
        response = requests.get(f"{BASE_URL}/consultas/clientes")
        assert response.status_code == 200
        assert 'cliente_id' in response.text or isinstance(response.json(), list)
        print("test_consultas_clientes: PASSED")
    except Exception as e:
        print(f"test_consultas_clientes: FAILED with error {e}")

def test_consultas_clientes_json():
    try:
        response = requests.get(f"{BASE_URL}/consultas/clientes?Formato=JSON")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_consultas_clientes_json: PASSED")
    except Exception as e:
        print(f"test_consultas_clientes_json: FAILED with error {e}")

def test_consultas_puntos_a_vencer():
    try:
        response = requests.get(f"{BASE_URL}/consultas/puntos_a_vencer")
        assert response.status_code == 200
        assert 'cliente_id' in response.text or isinstance(response.json(), list)
        print("test_consultas_puntos_a_vencer: PASSED")
    except Exception as e:
        print(f"test_consultas_puntos_a_vencer: FAILED with error {e}")

def test_consultas_puntos_a_vencer_json():
    try:
        response = requests.get(f"{BASE_URL}/consultas/puntos_a_vencer?Formato=JSON")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_consultas_puntos_a_vencer_json: PASSED")
    except Exception as e:
        print(f"test_consultas_puntos_a_vencer_json: FAILED with error {e}")

def test_consultas_puntos_a_vencer_dias():
    try:
        response = requests.get(f"{BASE_URL}/consultas/puntos_a_vencer?dias=30")
        assert response.status_code == 200
        assert 'cliente_id' in response.text or isinstance(response.json(), list)
        print("test_consultas_puntos_a_vencer_dias: PASSED")
    except Exception as e:
        print(f"test_consultas_puntos_a_vencer_dias: FAILED with error {e}")

def test_consultas_puntos_a_vencer_dias_json():
    try:
        response = requests.get(f"{BASE_URL}/consultas/puntos_a_vencer?dias=30&Formato=JSON")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("test_consultas_puntos_a_vencer_dias_json: PASSED")
    except Exception as e:
        print(f"test_consultas_puntos_a_vencer_dias_json: FAILED with error {e}")

if __name__ == "__main__":
    tests = [
        test_get_clientes,
        test_get_conceptos,
        test_get_reglas,
        test_get_vencimientos,
        test_get_bolsas,
        test_get_uso_puntos,
        test_consultas_uso_puntos,
        test_consultas_uso_puntos_json,
        test_consultas_bolsas,
        test_consultas_bolsas_json,
        test_consultas_clientes,
        test_consultas_clientes_json,
        test_consultas_puntos_a_vencer,
        test_consultas_puntos_a_vencer_json,
        test_consultas_puntos_a_vencer_dias,
        test_consultas_puntos_a_vencer_dias_json,
    ]

    for test in tests:
        test()
