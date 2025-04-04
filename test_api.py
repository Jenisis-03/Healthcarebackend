import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_auth_endpoints():
    # Test patient registration
    patient_register_data = {
        'username': 'testpatient',
        'password': 'test123',
        'confirm_password': 'test123',
        'email': 'patient@example.com',
        'first_name': 'Test',
        'last_name': 'Patient',
        'phone_number': '1234567890',
        'address': '123 Test St',
        'date_of_birth': '1990-01-01',
        'user_type': 'PATIENT'
    }
    
    print('\n1. Testing Patient Registration:')
    response = requests.post(f'{BASE_URL}/auth/register/', json=patient_register_data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Test doctor registration
    doctor_register_data = {
        'username': 'testdoctor',
        'password': 'test123',
        'confirm_password': 'test123',
        'email': 'doctor@example.com',
        'first_name': 'Test',
        'last_name': 'Doctor',
        'phone_number': '0987654321',
        'address': '456 Test St',
        'date_of_birth': '1985-01-01',
        'user_type': 'DOCTOR'
    }
    
    print('\n2. Testing Doctor Registration:')
    response = requests.post(f'{BASE_URL}/auth/register/', json=doctor_register_data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Test patient login
    patient_login_data = {
        'username': 'testpatient',
        'password': 'test123'
    }
    
    print('\n3. Testing Patient Login:')
    response = requests.post(f'{BASE_URL}/auth/login/', json=patient_login_data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    patient_token = response.json().get('access')
    
    # Test doctor login
    doctor_login_data = {
        'username': 'testdoctor',
        'password': 'test123'
    }
    
    print('\n4. Testing Doctor Login:')
    response = requests.post(f'{BASE_URL}/auth/login/', json=doctor_login_data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    doctor_token = response.json().get('access')
    
    return patient_token, doctor_token

def test_patient_endpoints(token):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create patient
    patient_data = {
        'blood_group': 'A+',
        'allergies': 'None',
        'medical_conditions': 'None',
        'emergency_contact_name': 'Emergency Contact',
        'emergency_contact_number': '9876543210'
    }
    
    print('\n3. Testing Patient Creation:')
    response = requests.post(f'{BASE_URL}/patients/', json=patient_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    patient_id = response.json().get('id')
    
    # Get all patients
    print('\n4. Testing Get All Patients:')
    response = requests.get(f'{BASE_URL}/patients/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Get specific patient
    print(f'\n5. Testing Get Patient {patient_id}:')
    response = requests.get(f'{BASE_URL}/patients/{patient_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Update patient
    update_data = {
        'blood_group': 'B+',
        'allergies': 'Penicillin',
        'medical_conditions': 'Hypertension'
    }
    
    print(f'\n6. Testing Update Patient {patient_id}:')
    response = requests.put(f'{BASE_URL}/patients/{patient_id}/', json=update_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    return patient_id

def test_doctor_endpoints(token):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create doctor
    doctor_data = {
        'specialization': 'Cardiology',  # Using specialization name instead of ID
        'license_number': 'DOC123',
        'experience_years': 5,
        'consultation_fee': 100.00,
        'available_days': 'Monday,Tuesday,Wednesday',
        'available_time_start': '09:00:00',
        'available_time_end': '17:00:00'
    }
    
    print('\n7. Testing Doctor Creation:')
    response = requests.post(f'{BASE_URL}/doctors/', json=doctor_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    doctor_id = response.json().get('id')
    
    # Get all doctors
    print('\n8. Testing Get All Doctors:')
    response = requests.get(f'{BASE_URL}/doctors/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Get specific doctor
    print(f'\n9. Testing Get Doctor {doctor_id}:')
    response = requests.get(f'{BASE_URL}/doctors/{doctor_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Update doctor
    update_data = {
        'specialization': 'Cardiology',
        'consultation_fee': 150.00,
        'available_days': 'Monday,Wednesday,Friday'
    }
    
    print(f'\n10. Testing Update Doctor {doctor_id}:')
    response = requests.put(f'{BASE_URL}/doctors/{doctor_id}/', json=update_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    return doctor_id

def test_mapping_endpoints(token, patient_id, doctor_id):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create mapping
    mapping_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id
    }
    
    print('\n11. Testing Create Patient-Doctor Mapping:')
    response = requests.post(f'{BASE_URL}/mappings/', json=mapping_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    mapping_id = response.json().get('id')
    
    # Get all mappings
    print('\n12. Testing Get All Mappings:')
    response = requests.get(f'{BASE_URL}/mappings/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Get mappings for specific patient
    print(f'\n13. Testing Get Mappings for Patient {patient_id}:')
    response = requests.get(f'{BASE_URL}/mappings/patient/{patient_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Delete mapping
    print(f'\n14. Testing Delete Mapping {mapping_id}:')
    response = requests.delete(f'{BASE_URL}/mappings/{mapping_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    if response.status_code != 204:
        print(f'Response: {json.dumps(response.json(), indent=2)}')

def cleanup_test_data(token, patient_id, doctor_id):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Delete patient
    print(f'\n15. Testing Delete Patient {patient_id}:')
    response = requests.delete(f'{BASE_URL}/patients/{patient_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    if response.status_code != 204:
        print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Delete doctor
    print(f'\n16. Testing Delete Doctor {doctor_id}:')
    response = requests.delete(f'{BASE_URL}/doctors/{doctor_id}/', headers=headers)
    print(f'Status Code: {response.status_code}')
    if response.status_code != 204:
        print(f'Response: {json.dumps(response.json(), indent=2)}')

def test_error_handling(token):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test non-existent patient
    print('\n17. Testing Get Non-existent Patient:')
    response = requests.get(f'{BASE_URL}/patients/999/', headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Test invalid doctor data
    invalid_doctor_data = {
        'specialization': '',  # Empty specialization
        'license_number': '',  # Empty license number
        'experience_years': -1,  # Invalid years
        'consultation_fee': -100.00,  # Invalid fee
        'available_days': 'InvalidDay',
        'available_time_start': '25:00:00',  # Invalid time
        'available_time_end': '17:00:00'
    }
    
    print('\n18. Testing Invalid Doctor Creation:')
    response = requests.post(f'{BASE_URL}/doctors/', json=invalid_doctor_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    
    # Test invalid mapping
    invalid_mapping_data = {
        'patient_id': 999,  # Non-existent patient
        'doctor_id': 999  # Non-existent doctor
    }
    
    print('\n19. Testing Invalid Mapping Creation:')
    response = requests.post(f'{BASE_URL}/mappings/', json=invalid_mapping_data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')

def main():
    try:
        # Test authentication endpoints and get tokens
        patient_token, doctor_token = test_auth_endpoints()
        
        # Test patient endpoints with patient token
        patient_id = test_patient_endpoints(patient_token)
        
        # Test doctor endpoints with doctor token
        doctor_id = test_doctor_endpoints(doctor_token)
        
        # Test mapping endpoints with patient token
        test_mapping_endpoints(patient_token, patient_id, doctor_id)
        
        # Test error handling scenarios
        test_error_handling(patient_token)
        
        # Cleanup test data with respective tokens
        cleanup_test_data(patient_token, patient_id, doctor_id)
        
    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {e}')
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON response: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    main()